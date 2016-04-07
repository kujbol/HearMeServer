from mock import sentinel
import pytest

from hear_me.libs.services import ServiceRegistry


class TestServiceRegistry(object):
    @pytest.fixture
    def service_registry(self):
        return ServiceRegistry()

    def test_register(self, service_registry):
        service_registry.register('service_1', sentinel.service_1)
        service_registry.register('service_2', sentinel.service_2)

        assert service_registry.services == {
            'service_1': sentinel.service_1,
            'service_2': sentinel.service_2,
        }

        assert service_registry.services.service_1 == sentinel.service_1
        assert service_registry.services.service_2 == sentinel.service_2

    def test_register_on_already_registered_service(self, service_registry):
        service_registry.register('service_1', sentinel.service_1)
        with pytest.raises(RuntimeError):
            service_registry.register('service_1', sentinel.service_1)

    def test_query_service(self, service_registry):
        service_registry.register('service_1', sentinel.service_1)
        service_registry.register('service_2', sentinel.service_2)

        service_1 = service_registry.query_service('service_1')
        service_2 = service_registry.query_service('service_2')

        assert service_1 == sentinel.service_1
        assert service_2 == sentinel.service_2

    def test_service_decorator_registry(self, service_registry):
        @service_registry.service
        def random_service():
            return sentinel.service_1

        service_registry.services.random_service = sentinel.service_1
