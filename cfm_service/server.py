"""Docstring."""

import logging
import os

from cfm_service.server_impl import ServerImpl
from flask import Flask, jsonify


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
logging.info("Hello")

app = Flask(__name__)
app.config.from_object("cfm_service.default_settings.Config")

custom_settings = os.environ.get("FLASK_APP_SETTINGS", None)
if custom_settings:
    app.logger.info("Loading custom settings from {}".format(custom_settings))
    app.config.from_object(custom_settings)

app.logger.info("Loaded settings {}".format(app.config))

storage_type = app.config["STORAGE"]
app.logger.info("Storage backend will be: {}".format(storage_type))

if storage_type == "memory":
    storage_config = {}
elif storage_type == "cassandra":
    storage_config = app.config["CASSANDRA"]
else:
    storage_config = {}

server = ServerImpl(storage_type, storage_config)


@app.route("/ping")
def hello_world():
    """Docstring."""
    return "pong"


@app.route("/advice/<pantry_id>")
def advise_pantry(pantry_id: str):
    """Docstring."""
    advices = server.advise_pantry(pantry_id)
    return jsonify(advices)


@app.route("/pantry/<pantry_id>")
def get_pantry(pantry_id: str):
    """Docstring."""
    return jsonify(server.get_pantry(pantry_id))
