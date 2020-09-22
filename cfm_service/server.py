import logging
import os
from flask import Flask


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logging.info('Hello')

app = Flask(__name__)
app.config.from_object('cfm_service.default_settings.Config')

custom_settings = os.environ.get('FLASK_APP_SETTINGS', None)
if custom_settings:
    app.logger.info('Loading custom settings from {}'.format(custom_settings))
    app.config.from_object(custom_settings)

app.logger.info('Loaded settings {}'.format(app.config))


@app.route('/')
def hello_world():
    return {}
