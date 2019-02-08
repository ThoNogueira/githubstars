from flask import Blueprint
from project import db, ma

import marshmallow as marsh

bp = Blueprint('sqlalchemy', __name__)

# Define a associação entre repositorios e tags
repositories_tags_association = db.Table('repositories_tags',
                                         db.Column('repositories_id', db.Integer, db.ForeignKey(
                                             'repositories.id')),
                                         db.Column('tags_id', db.Integer, db.ForeignKey('tags.id')))

# Define a associação entre repositórios e linguagens
repositories_languages_association = db.Table('repositories_languages',
                                              db.Column('repositories_id', db.Integer, db.ForeignKey(
                                                  'repositories.id')),
                                              db.Column('languages_id', db.Integer, db.ForeignKey('languages.id')))


# Define a representação do repositório
class Repository(db.Model):
    __tablename__ = "repositories"

    id = db.Column(db.Integer, primary_key=True)
    
    git_login = db.Column(db.String)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(2000), unique=True)
    description = db.Column(db.Text)

    languages = db.relationship(
        "Language", secondary=repositories_languages_association)

    tags = db.relationship(
        "Tag", secondary=repositories_tags_association)

    def __init__(self, git_login, name, url, description):
        self.git_login = git_login
        self.name = name
        self.url = url
        self.description = description


# Define a representação da linguagem
class Language(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name


# Define a representação da tag
class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name


# Define os esquemas
class LanguageSchema(ma.ModelSchema):
    class Meta:
        model = Language


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag


class RepositorySchema(ma.ModelSchema):
    class Meta:
        ordered = True

    id = ma.Integer()

    name = ma.String(dump_to="Repository")
    description = ma.String(dump_to="Description")

    # Define como selecionar as tags do repositório
    def get_tags(self, repo_id):
        tags = Repository.query.get(repo_id).tags
        return tags

    # Define como selecionar as lingugens do repositório
    def get_languages(self, repo_id):
        languages = Repository.query.get(repo_id).languages
        return languages

    @marsh.post_dump(pass_many=True)
    def post_dump(self, data, many):
        if many:
            for repo in data:
                languages = self.get_languages(
                    repo['id']) if repo['id'] else []
                for language in languages:
                    repo['Languages'] = f"{repo['Languages']}, {language.name}" if 'Languages' in repo else language.name

                tags = self.get_tags(repo['id']) if repo['id'] else []
                for tag in tags:
                    repo['Tags'] = f"{repo['Tags']}, {tag.name}" if 'Tags' in repo else tag.name
        else:
            data['Languages'] = self.get_languages(data['id'])
            data['Tags'] = self.get_tags(data['id'])

        return data
