from flask import Flask
from app_package.keys import SECRET_KEY, PG_URI
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = PG_URI

db = SQLAlchemy(app)

from app_package import routes