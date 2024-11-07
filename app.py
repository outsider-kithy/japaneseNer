import sys
from flask import Flask

def create_app():
    app = Flask(__name__)
    from api import views as api_views
    app.register_blueprint(api_views.api, url_prefix="/api")

    return app
