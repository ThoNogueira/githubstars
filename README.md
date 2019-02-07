# githubstars - brainn-co/challenge-development

GitHub Stars é um projeto desenvolvido com o objetivo de aplicar para uma vaga na brainn.co

O projeto foi desenvolvido utilizando os seguintes conhecimentos:
* RESTful API
* Python (3.7)
* Flask
* GraphQL
* React JS
* Bootstrap
* HTML5
* CSS3
* pylint
* pylint_flask

Este projeto consiste em um gerenciador de tags de repositórios favoritos no Git Hub e possui as seguintes funcionalidades:

* Recupera repositórios "starred" do GitHub de determinado usuário.
* Gerencia tags dos repositórios recuperados (adicionar, editar, excluir).
* Filtra repositórios por tags.
* Oferece sugestões de tags para os repositórios.

## Instruções para execução

1. Descompacte o projeto em uma pasta.

1. Na linha de comando, dentro da pasta \githubstars, instale as dependências:

    `pipenv install`

1. Inicie o _virtual enviroment_:
    
    `pipenv shell`

1. Crie a base de dados:

    `flask db upgrade`

1. Execute o servidor:

    `flask run`

1. Em outro terminal, dentro da pasta \githubstars\project\views\app instale as dependências:

    `npm i`

1. Execute a aplicação:

    `npm start`
