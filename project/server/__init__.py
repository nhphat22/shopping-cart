import os
from flask import Flask
from flask_cors import CORS
from project.server.auth.views import auth_blueprint


app = Flask(__name__)
CORS(app)
app.register_blueprint(auth_blueprint)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
