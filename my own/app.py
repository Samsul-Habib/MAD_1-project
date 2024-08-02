from flask import Flask,render_template,request,redirect
import time,jinja2
from flask_sqlalchemy import SQLAlchemy

from routes import *

from tables import db

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sponsorship.sqlite3"

db.init_app(app)

#app.app_context().push()
with app.app_context():
    db.create_all()
if __name__ == "__main__" :
    app.run(debug=True)