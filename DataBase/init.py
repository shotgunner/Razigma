# initialize the database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_username = db.Column(db.String(80), unique=True, nullable=False)
    telegram_id = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_level = db.Column(db.Integer, default=1)
    total_score = db.Column(db.Integer, default=0)

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    media_type = db.Column(db.String(20), nullable=False)  # 'image', 'video', 'audio', etc.
    media_file = db.Column(db.LargeBinary, nullable=False)
    difficulty = db.Column(db.Integer, default=1)
    next_level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=True)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer)  # in seconds
    score = db.Column(db.Integer)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
