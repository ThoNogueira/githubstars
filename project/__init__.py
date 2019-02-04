import os

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_babel import Babel
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from project.config import configure_app

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    configure_app(app)
    babel = Babel(app)
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)

    from project.models import sqlalchemy
    app.register_blueprint(sqlalchemy.bp)

    from project.controllers import routes
    app.register_blueprint(routes.bp)

    return app
