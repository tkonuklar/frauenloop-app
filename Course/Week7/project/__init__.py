from flask import Flask
from flask_sqlalchemy import SQLAlchemy # install this first!

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///side.db' # with pg_admin you can access tables from side.db
db = SQLAlchemy(app)

from project import controllers