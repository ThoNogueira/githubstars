import os

from flask import Blueprint, request, jsonify

# TODO: Tho: Verificar se é possível substituir por flask_sqlalchemy
from sqlalchemy import func, text, or_, any_

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from project import db
from project.models import sqlalchemy


bp = Blueprint('routes', __name__)

# Insere no banco todos os repositorios favoritados no git hub cujo user corresponde ao login recebido
@bp.route("/api/v1/repositories/<string:gitLogin>", methods=['POST'])
def load_all_repositories(gitLogin):

    # Função recursiva para navegar entre na paginação do graphQL
    def insert_all_stars_repositories(endCursor=''):
        # Define a query que será executada na API V4 (graphQL) do github
        query = ''
        if endCursor == '':
            query = '''
                    query {
                         user(login: "%s") {
                            id
                            name
                            starredRepositories(first: 100) {
                ''' % gitLogin
        else:
            query = '''
                    query starredRepositories($endCursor: String = "%s"){
                         user(login: "%s") {
                            id
                            name
                            starredRepositories(first: 100, after: $endCursor) {
                ''' % (endCursor, gitLogin)

        query += '''
                    totalCount
                    edges {
                        node {
                            id
                            name
                            url
                            description
                            languages(first: 10) {
                                edges {
                                    node {
                                    name
                                    }
                                }
                            }
                        }
                        cursor
                    }
                    pageInfo {
                        hasNextPage
                        hasPreviousPage
                        endCursor
                    }
                }
            }
        }'''

        headers = {
            # Autorização gerada no github. Para o deploy deve idealmente ser registrada no SO.
            'Authorization': 'bearer  8b67d06eb1e74a55ba8887cd388618bbb060461a'
        }
        url = 'https://api.github.com/graphql'
        transport = RequestsHTTPTransport(url, headers=headers, use_json=True)
        client = Client(transport=transport)

        # Executa a query
        data = client.execute(gql(query))
        user = data.get('user')
        starred_repositories = user.get('starredRepositories')

        repositoriesInfo = starred_repositories.get('edges')

        # Para cada repositório encontrado
        for repositoryInfo in repositoriesInfo:
            # Seleciona o nó
            node = repositoryInfo.get('node')

            # Resgata o nome do repositório
            repositoryName = node.get('name')

            # Seleciona o repositório pelo nome no banco de dados
            repository = sqlalchemy.Repository.query.filter_by(name=repositoryName).first()

            # Se o repositorio não existir
            if not repository:
                # Instancia um novo repositorio com as informações selecionadas
                repository = sqlalchemy.Repository(gitLogin, repositoryName, node.get('url'), node.get('description'))
                # Determina a inclusão do repositorio
                db.session.add(repository)

                # Seleciona a tag cujo nome seja o nome do usuario que favoritou o repositorio. Essa será sempre a primeira tag sugerida.
                tag_login = sqlalchemy.Tag.query.filter_by(name=gitLogin).first()

                # Se a tag não existir
                if not tag_login:
                    # Instancia a tag
                    tag_login = sqlalchemy.Tag(gitLogin)
                    # Determian a inclusão da tag
                    db.session.add(tag_login)

                # Define a primeira tag do repositorio como sendo o login do usuario que favoritou o repositório
                repository.tags.append(tag_login)

                # Seleciona as lista de linguagens que o repositório possui
                languages = node.get('languages')
                languages_info = languages.get('edges')

                # Para cada lnguagem que o repositório possui
                for language_info in languages_info:
                    # Seleciona o nó
                    node = language_info.get('node')
                    # Resgata o nome da linguagem
                    language_name = node.get('name')

                    # Seleciona a linguagem corrente pelo nome
                    language = sqlalchemy.Language.query.filter_by(name=language_name).first()

                    # Se a linguagem não existir
                    if not language:
                        # Instancia a linguagem
                        language = sqlalchemy.Language(node.get('name'))
                        # Determina a inclusão da linguagem
                        db.session.add(language)

                    # Adiciona a linguagem ao repositório
                    repository.languages.append(language)

                    # Seleciona a tag cujo nome seja o nome da linguagem
                    tag_language = sqlalchemy.Tag.query.filter_by(name=language_name).first()

                    # Se a tag não existir
                    if not tag_language:
                        # Instancia a tag
                        tag_language = sqlalchemy.Tag(language_name)
                        # Determian a inclusão da tag
                        db.session.add(tag_language)

                    # Define a linguagem como sendo uma tag do repositorio
                    repository.tags.append(tag_language)

                db.session.commit()

        # Se existir proxima página
        if starred_repositories.get('pageInfo').get('hasNextPage') == True:
            # Chama a função novamente passando o cursor
            insert_all_stars_repositories(starred_repositories.get('pageInfo').get('endCursor'))

    # Chamada inicial da função
    insert_all_stars_repositories()

    # Retorna o login recebido por parâmetro
    return jsonify({'result': gitLogin})


# Seleciona os repositórios
@bp.route("/api/v1/repositories", methods=['GET'])
def get_repositories():

    # Resgata o login do git recebido no request
    recived_git_login = request.args.get('git_login')
    
    # Resgata a lista com o nome das tags que o usuário deseja utilizar para filtrar a lista de repositórios
    recived_tags = request.args.get('tags')

    # print(request.query_string)
    print(recived_tags)

    recived_tags_names = None
    if recived_tags:
        recived_tags_names = request.args.get('tags').split(',') if request.args.get('tags') != '' else None

    # Variável qe irá guardar o resultado do select que selecionará os repositórios válidos de acordo com os parâmetros recebidos
    repositories = None

    # Se recebeu alguma tag
    if recived_tags_names:
        # Trata os valores de cada tag recebido de forma a utiliza-los no select
        recived_tags_names = [f'{tag.lower()}%' for tag in recived_tags_names]

        # Seleciona as os repositórios cujo git_login seja igual ao recebido e possua as tags recebidas 
        repositories = sqlalchemy.Repository.query \
            .join(sqlalchemy.repositories_tags_association) \
            .join(sqlalchemy.Tag) \
            .filter(func.lower(sqlalchemy.Repository.git_login) == func.lower(recived_git_login)) \
            .filter(or_(*[func.lower(sqlalchemy.Tag.name).like(name) for name in recived_tags_names])).all()
    # Se não recebeu a tag
    else:
        # Seleciona todos os repositórios cujo git_login seja igual ao recebido
        repositories = sqlalchemy.Repository.query.filter(func.lower(sqlalchemy.Repository.git_login) == func.lower(recived_git_login)).all()
    
    # Resgata o esquema dos repositório
    repository_schema = sqlalchemy.RepositorySchema(many=True)
    # Aplica o esquema aos repositórios selecionados
    output = repository_schema.dump(repositories).data

    return jsonify(output)

# Seleciona as tags do repositório
@bp.route("/api/v1/repositories/<int:id>/tags", methods=['GET'])
def get_repository_tags(id):

    # Selecionas as tags do repositório correspondente ao id recebido
    repository_tags = sqlalchemy.Repository.query.get(id).tags

    # Resgata o esquema dos repositório
    tag_schema = sqlalchemy.TagSchema(many=True)
    # Aplica o esquema às tags selecionadas
    output = tag_schema.dump(repository_tags).data

    return jsonify(output)


# Atualiza as tags do repositorio
@bp.route("/api/v1/repositories/<int:id>", methods=['PATCH'])
def update_repository(id):
    
    # Seleciona o repositorio por id
    repository = sqlalchemy.Repository.query.get(id)

    # Se o repositório não existir
    if not repository:
        return jsonify({'message': f'Repository with id ''{id}'' not found!'})

    # Seleciona as tags do repositório
    repository_tags_names = set(map((lambda tag: tag.name), repository.tags))

    # Seleciona as tags recebidas
    recived_tags_names = set(request.get_json()['tags'])

    # Se as tags recebidas for diferente das tags contidas no repositório
    if repository_tags_names != recived_tags_names:
        # Define as tags que devem ser incluidas
        tags_to_include = recived_tags_names - repository_tags_names

        # para cada tag que deve ser incluida
        for tag_name in tags_to_include:
            # Seleciona a tag pelo nome
            tag = sqlalchemy.Tag.query.filter_by(name=tag_name).first()
            # Se a tag não existir
            if not tag:
                # Instancia a tag
                tag = sqlalchemy.Tag(tag_name)
                # Determina a inclusão da tag
                db.session.add(tag)

            # Determina a associação da tag ao repositorio
            repository.tags.append(tag)
        
        # Define as tags que devem ser excluidas
        tags_to_exclude = repository_tags_names - recived_tags_names

        # Para cada tag que deve ser excluida
        for tag_name in tags_to_exclude:
            # Seleciona a tag pelo nome
            tag = sqlalchemy.Tag.query.filter_by(name=tag_name).first()
            # Se a tag não existir
            if tag:
                repository.tags.remove(tag)

    db.session.commit()

    return jsonify({'result': id})


# Controla as exceções
@bp.errorhandler(Exception)
def global_exception_handler(err):
    response = jsonify({'message': str(err)})
    response.status_code = 500
    return response
