import pytest
from mock import call, patch

from hear_me.libs.mongo import (
    MongoConnectorFactory,
    MongoConnectorFactoryError,
)
from hear_me.settings.defaults import MongoDBConfig


@pytest.fixture()
def fixt_mongo_connector():
    return MongoConnectorFactory(conf=MongoDBConfig).build()


@pytest.fixture()
def fixt_mongo_conf():
    return {
        'username': None,
        'password': None,
        'host': 'mongodb://localhost',
        'port': 27017,
    }


@pytest.mark.parametrize('conf, expected_error', [
    (None, 'missing configuration of mongo'),
    ({'DB_NAME': 'db_name'}, 'missing parameter in configuration: \'HOST\''),
    ({'HOST': 'host'}, 'missing parameter in configuration: \'DB_NAME\''),
    (
            {'HOST': 'host', 'DB_NAME': 'db_name'},
            'missing parameter in configuration: \'PORT\''
    ),
])
def test_mongo_connector_factory_errors(conf, expected_error):
    with pytest.raises(MongoConnectorFactoryError) as error:
        MongoConnectorFactory(conf)

    assert str(error.value) == expected_error


@patch('hear_me.libs.mongo.connect', autospec=True)
@patch('hear_me.libs.mongo.disconnect', autospec=True)
@patch('hear_me.libs.mongo.log', autospec=True)
def test_mongo_connector(
        mock_log, mock_disconnect, mock_connect, fixt_mongo_connector,
        fixt_mongo_conf
):
    with fixt_mongo_connector:
        pass

    mock_connect.assert_called_once_with(
        db=MongoDBConfig['DB_NAME'], alias='default', **fixt_mongo_conf
    )

    mock_log.debug.assert_has_calls([
        call('entering MongoConnector with db_alias default'),
        call('leaving MongoConnector with db_alias default'),
    ])

    mock_disconnect.assert_has_calls([
        call('default'),
        call('default'),
    ])
