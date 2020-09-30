"""Docstring."""
import logging

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cfm_core.ingredient import Ingredient
from cfm_core.pantry import Pantry
from cfm_service.storage import CfmStorage


class CassandraCfmStorage(CfmStorage):
    """Docstring."""

    def __init__(self, storage_config: dict):
        """Docstring."""
        logging.getLogger("cassandra").setLevel(storage_config["log_level"])

        auth_provider = PlainTextAuthProvider(
            storage_config["username"], storage_config["password"]
        )
        cloud_config = {"secure_connect_bundle": "secure-connect-cfm.zip"}

        self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = self.cluster.connect()

        self.pantry_lookup = self.session.prepare(
            "SELECT pantry_id, blob FROM cfm.pantry WHERE pantry_id=?;"
        )
        self.pantry_store = self.session.prepare(
            "INSERT INTO cfm.pantry (pantry_id, blob) VALUES (?, ?);"
        )

        self.store_pantry("-1", "-1", Pantry([Ingredient("egg", 1, "piece")]))

    def store_pantry(self, user_id: str, pantry_id: str, pantry: Pantry) -> str:
        """Docstring."""
        statement = self.pantry_store.bind([pantry_id, str(pantry)])
        self.session.execute(statement)
        return "OK"

    def get_pantry(self, pantry_id: str) -> Pantry:
        """Docstring."""
        statement = self.pantry_lookup.bind([pantry_id])
        rows = self.session.execute(statement)
        pantry_id, blob = rows.all().pop()
        return Pantry.from_str(blob)
