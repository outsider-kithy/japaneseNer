import sys
from flask import Flask

def create_app():
    app = Flask(__name__)
    from api import views as api_views
    app.register_blueprint(api_views.api, url_prefix="/api")

    from title import views as title_views
    app.register_blueprint(title_views.title, url_prefix="/title")

    return app
