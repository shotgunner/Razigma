from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from DataBase.init import User, Level, UserProgress, Badge, UserBadge

def setup_admin(app, db):
    admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap3')

    # Add views for each model
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Level, db.session))
    admin.add_view(ModelView(UserProgress, db.session))
    admin.add_view(ModelView(Badge, db.session))
    admin.add_view(ModelView(UserBadge, db.session))

    return admin  # Return the admin object