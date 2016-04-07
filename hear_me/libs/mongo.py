import logging

from mongoengine import connect
from mongoengine.connection import disconnect

log = logging.getLogger(__name__)


class MongoConnectorFactoryError(Exception):
    pass


class MongoConnectorFactory:
    def __init__(self, conf=None):
        if conf is None:
            raise MongoConnectorFactoryError("missing configuration of mongo")
        try:
            self.host = conf['HOST']
            self.db_name = conf['DB_NAME']
            self.port = conf['PORT']
        except KeyError as error:
            raise MongoConnectorFactoryError(
                "missing parameter in configuration: {}".format(error)
            )

    def build(self):
        return MongoConnector(self.host, self.db_name, self.port)


class MongoConnector:
    def __init__(
            self, host, db_name, port, username=None, password=None,
            db_alias=None,
    ):
        self.db_alias = db_alias or 'default'
        self.db_name = db_name
        self.mongo_conf = {
            'host': host,
            'username': username,
            'password': password,
            'port': port,
        }

    def __enter__(self):
        msg = 'entering MongoConnector with db_alias {}'
        log.debug(msg.format(self.db_alias))
        disconnect(self.db_alias)
        return connect(
            db=self.db_name,
            alias=self.db_alias,
            **self.mongo_conf
        )

    def __exit__(self, *args):
        msg = 'leaving MongoConnector with db_alias {}'
        log.debug(msg.format(self.db_alias))
        disconnect(self.db_alias)
