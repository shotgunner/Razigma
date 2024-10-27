# initialize the database
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from config import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from werkzeug.utils import secure_filename
import os
from markupsafe import Markup

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the upload directory
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_username = db.Column(db.String(80), unique=True, nullable=False)
    telegram_id = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    current_level = db.Column(db.Integer, default=1)
    total_score = db.Column(db.Integer, default=1)

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    media_type = db.Column(db.String(20), nullable=False)  # 'image', 'video', 'audio', etc.
    media_file = db.Column(db.String(255), nullable=False)  # Store file path instead of binary data
    difficulty = db.Column(db.Integer, default=100)
    verification_type = db.Column(db.String(20), nullable=False)  # 'image', 'video', 'audio', etc.
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

class LevelModelView(ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.media_file:
            return ''
        return Markup('<img src="{model.media_file}" width="100">'.format(model=model))

    column_formatters = {
        'media_file': _list_thumbnail
    }
    form_extra_fields = {
        'media_file': FileUploadField('Media File', base_path=app.config['UPLOAD_FOLDER'])
    }

    def on_model_change(self, form, model, is_created):
        if form.media_file.data:
            filename = secure_filename(form.media_file.data.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.media_file.data.save(file_path)
            model.media_file = file_path

def setup_admin(app, db):
    admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap3')

    # Add views for each model
    admin.add_view(ModelView(User, db.session))
    admin.add_view(LevelModelView(Level, db.session))
    admin.add_view(ModelView(UserProgress, db.session))
    admin.add_view(ModelView(Badge, db.session))
    admin.add_view(ModelView(UserBadge, db.session))

    return admin  # Return the admin object

def init_db():
    with app.app_context():
        db.create_all()
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
