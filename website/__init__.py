from flask import Flask, render_template
from flask_session import Session
from dotenv import load_dotenv
import os
load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    @app.errorhandler(404)
    def page_not_found(e):
        return "404 Page Not Found"

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    return app