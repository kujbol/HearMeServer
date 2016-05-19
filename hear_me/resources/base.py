from simplejson import JSONDecodeError
import logging
import requests
from werkzeug.exceptions import HTTPException

log = logging.getLogger(__name__)


class ClientError(HTTPException):
    """Exception for Service errors."""

    def __init__(self, resource, code, text):
        super().__init__(
            description='Service: {}, Text: {}'.format(resource, text),
        )
        self.resource = resource
        self.code = code
        self.text = text


    @classmethod
    def from_response(cls, response):
        return cls(
            response.url,
            response.status_code,
            response.text,
        )

    def __str__(self):
        return 'Code: {}, {}'.format(self.code, self.description)


class BaseClient(object):
    REQUESTS_EXCEPTION_STATUS_CODE = -1
    ERROR_CLASS = ClientError

    def __init__(self, api_url):
        self.api_url = api_url

    def make_url(self, path):
        return self.api_url + path

    def handle_request(
            self, request, url_suffix, *args, **kwargs
    ):
        resource_url = self.make_url(url_suffix)
        try:
            response = request(resource_url, *args, **kwargs)
            return response
        except requests.exceptions.RequestException as ex:
            msg = '{} unreachable: {}'.format(self.__class__.__name__, ex)
            raise self.ERROR_CLASS(
                resource_url, self.REQUESTS_EXCEPTION_STATUS_CODE, msg
            )

    def handle_response(self, response, schema=None):
        if response.status_code == requests.codes.ok:
            try:
                response_json = response.json()
            except JSONDecodeError:
                log.error(
                    'Invalid json data: %s %s %s',
                    response.url, response.encoding, response.text
                )
                raise

            if schema is not None:
                return schema.deserialize(response_json)
            else:
                return response_json

        elif response.status_code == 401:
            # TODO handle token expiration
            raise self.ERROR_CLASS.from_response(response)
        else:
            raise self.ERROR_CLASS.from_response(response)

    def make_call(self, request, url_suffix, schema=None, *args, **kwargs):
        return self.handle_response(
            self.handle_request(
                request, url_suffix, *args, **kwargs
            ),
            schema=schema
        )
