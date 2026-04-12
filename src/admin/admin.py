from flask import Flask, redirect, url_for, request, session, views
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import sessionmaker
from src.db.db_conn import DBConn
from src.db.tables import *
from icecream import ic
import os

Session = sessionmaker(bind=DBConn().get_engine())
db_session = Session()

ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")


def is_authenticated():
    return session.get("authenticated")


class AuthAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not is_authenticated():
            return redirect(url_for(".login"))
        return super().index()

    @expose("/login", methods=["GET", "POST"])
    def login(self):
        if request.method == "POST":
            if (
                request.form["login"] == ADMIN_LOGIN
                and request.form["password"] == ADMIN_PASSWORD
            ):
                session["authenticated"] = True
                return redirect(url_for(".index"))
            return self.render("admin/login.html", error="Неверный логин или пароль")
        return self.render("admin/login.html")

    @expose("/logout")
    def logout(self):
        session.pop("authenticated", None)
        return redirect(url_for(".login"))


class SecureModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        return is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.login"))


class TestView(BaseView):
    @expose("/test")
    def index(self):
        return self.render("admin/test.html")


app = Flask(__name__, template_folder=os.path.abspath("./src/admin/templates/"))
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-change-me")


admin = Admin(app, name="TrueNews", index_view=AuthAdminIndexView())


admin.add_view(SecureModelView(NewsItemDBEntity, db_session, name="News"))
admin.add_view(SecureModelView(ParserDBEntity, db_session, name="Parsers"))
admin.add_view(
    SecureModelView(SourceProviderDBEntity, db_session, name="SourceProviders")
)
admin.add_view(SecureModelView(SourceDBEntity, db_session, name="Sources"))
admin.add_view(TestView(name="My View"))


def run():
    app.run(port=os.getenv("ADMIN_PORT_CONTAINER"), debug=False, host="127.0.0.1")
