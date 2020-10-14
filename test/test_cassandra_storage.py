"""Test cassandra storage."""
import logging
import unittest

from cassandra import cluster as cassandra_driver
from cassandra.protocol import ConfigurationException
from ccmlib import common
from ccmlib.cluster import Cluster as CCMCluster
from ccmlib.cluster_factory import ClusterFactory as CCMClusterFactory
from cfm_core.ingredient import Ingredient
from cfm_core.pantry import Pantry
from cfm_service.storage.cassandra_storage import CassandraCfmStorage


class CassandraStorageTest(unittest.TestCase):
    """Testing pantry class."""

    CLUSTER_NAME = "cfm-ccm-cluster"
    CLUSTER_PATH = "/Users/zvo/.ccm"
    CLUSTER_VERSION = "3.11.8"
    CLUSTER_KWARGS = {"version": CLUSTER_VERSION}
    CLUSTER_NODE_COUNT = 1

    def __init__(self, *args, **kwargs):
        """__init__."""
        super().__init__(*args, **kwargs)

    def setUp(self):
        """Docstring."""
        self._start_cluster()
        self._init_cluster()

    def tearDown(self):
        """Docstring."""
        self._stop_cluster()

    def _start_cluster(self):
        """Docstring."""
        try:
            cluster = CCMClusterFactory.load(self.CLUSTER_PATH, self.CLUSTER_NAME)
            logging.debug(
                "Found existing ccm {} cluster; clearing".format(self.CLUSTER_NAME)
            )
            cluster.start(wait_for_binary_proto=True, wait_other_notice=True)
            self.CCM_CLUSTER = cluster
        except Exception:
            logging.debug(
                "Creating new ccm cluster {} with {}",
                self.CLUSTER_NAME,
                self.CLUSTER_KWARGS,
            )
            cluster = CCMCluster(
                self.CLUSTER_PATH, self.CLUSTER_NAME, **self.CLUSTER_KWARGS
            )
            cluster.set_configuration_options({"start_native_transport": True})
            common.switch_cluster(self.CLUSTER_PATH, self.CLUSTER_NAME)
            cluster.populate(self.CLUSTER_NODE_COUNT, ipformat=None)
            cluster.start(wait_for_binary_proto=True, wait_other_notice=True)
            self.CCM_CLUSTER = cluster

    def _init_cluster(self):
        session = cassandra_driver.Cluster(contact_points=["localhost"]).connect()
        try:
            session.execute("DROP KEYSPACE cfm;")
        except ConfigurationException:
            logging.debug("keyspace was not there")
        session.execute(
            """
            CREATE KEYSPACE cfm WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '1'}
        """
        )
        session.execute(
            """
            CREATE TABLE IF NOT EXISTS cfm.pantry (
                pantry_id text primary key,
                blob text
            );
        """
        )

    def _stop_cluster(self):
        self.CCM_CLUSTER.stop()
        self.CCM_CLUSTER.remove()

    def test_store_pantry(self):
        """Docstring."""
        cs = CassandraCfmStorage({"contact_points": ["localhost"], "log_level": "INFO"})
        response = cs.store_pantry(
            user_id="-1", pantry_id="-1", pantry=Pantry([Ingredient("egg", 1, "piece")])
        )
        self.assertEquals("OK", response)
