from mock import patch, Mock, sentinel
import pytest

import requests

from hear_me.resources.base import ClientError, BaseClient


class TestComponentClientError(object):
    def test_init(self):
        error = ClientError(
            sentinel.resource, sentinel.code, sentinel.text
        )
        assert error.resource == sentinel.resource
        assert error.code == sentinel.code
        assert error.text == sentinel.text

    def test_init_with_json_data(self):
        error = ClientError(
            sentinel.resource, sentinel.code, sentinel.text,
        )
        assert error.resource == sentinel.resource
        assert error.code == sentinel.code
        assert error.text == sentinel.text

    @pytest.fixture
    def example_error(self):
        return ClientError(
            'res', 'stat', 'txt'
        )

    def test_str(self, example_error):
        assert str(example_error) == 'Code: stat, Service: res, Text: txt'

    def test_from_response(self):
        response = Mock(headers={'content-type': 'text/plain'})
        error = ClientError.from_response(response)
        assert error.resource == response.url
        assert error.code == response.status_code
        assert error.text == response.text

    def test_from_response_no_content_type(self):
        response = Mock(headers={})
        error = ClientError.from_response(response)
        assert error.resource == response.url
        assert error.code == response.status_code
        assert error.text == response.text


class TestBaseComponentClient(object):
    def test_basics(self):
        assert BaseClient.ERROR_CLASS == ClientError

    @pytest.fixture
    def client(self):
        return BaseClient('http://xxx.yyy/aaa')

    def test_init(self, client):
        assert client.api_url == 'http://xxx.yyy/aaa'

    @pytest.mark.parametrize('url,expected_result', [
        ('/hello/world', 'http://xxx.yyy/aaa/hello/world'),
        ('?x=y', 'http://xxx.yyy/aaa?x=y'),
    ])
    def test_make_url(self, url, expected_result, client):
        assert client.make_url(url) == expected_result

    def test_handle_request_no_error(self, client):
        request = Mock()
        result = client.handle_request(request, '/bbb', 'x', 1, a=[], b={})
        request.assert_called_once_with(
            'http://xxx.yyy/aaa/bbb', 'x', 1, a=[], b={}
        )
        assert result == request.return_value

    def test_handle_request_generic_error(self, client):
        class MyException(Exception):
            pass

        request = Mock(side_effect=MyException)
        with pytest.raises(MyException):
            client.handle_request(request, 'x/y')

    def test_handle_request_request_exception(self, client):
        request = Mock(side_effect=requests.exceptions.RequestException)
        with pytest.raises(BaseClient.ERROR_CLASS):
            client.handle_request(request, 'x/y')

    def test_handle_response(self, client):
        mock_response = Mock()
        mock_response.status_code = 200
        result = client.handle_response(mock_response)
        assert result == mock_response.json.return_value

    def test_handle_response_schema(self, client):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_schema = Mock()
        result = client.handle_response(mock_response, schema=mock_schema)
        mock_schema.deserialize.assert_called_once_with(
            mock_response.json.return_value
        )
        assert result == mock_schema.deserialize.return_value

    def test_handle_response_error(self, client):
        class DummyException(Exception):
            pass

        mock_response = Mock()
        mock_response.status_code = 404
        with patch.object(client, 'ERROR_CLASS') as mock_error_class:
            mock_error_class.from_response.return_value = DummyException()
            with pytest.raises(DummyException):
                client.handle_response(mock_response)
            mock_error_class.from_response.assert_called_once_with(
                mock_response
            )
