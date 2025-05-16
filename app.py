from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import date 

db = SQLAlchemy

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habits.db"
# disable SQLAlchemy from tracking every object change and sending warning signals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, default=date.today)
    completed = db.Column(db.Boolean, default=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
