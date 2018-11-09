from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import BaseConfig
from src.manager import Manager

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

import src.models as models

if __name__ == '__main__':
    Manager(db, models).run()
