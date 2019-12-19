from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_login import current_user

#initializing app
app = Flask(__name__)

#importing configuration
app.config.from_pyfile('conf.py')

#initializing db
db = SQLAlchemy(app)

#initializing mail service
mail = Mail(app)

#importing views
from app import views, admin_view

#importing models
from app.models import Project, Blog, Subscribe, User, Contact, Hire, Logs

#creating admin model view
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def isaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

#initializing admin
admin = Admin(app, name='Database', template_mode='bootstrap3', index_view = MyAdminIndexView())

#registering models with admin
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Blog, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Subscribe, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(Hire, db.session))
admin.add_view(ModelView(Logs, db.session))

