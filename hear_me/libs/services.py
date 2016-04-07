import inspect


class ServiceRegistry(object):
    """Basic global services registry implementation."""

    def __init__(self):
        self.services = AtDict()

    def register(self, service_name, service):
        if service_name in self.services:
            raise RuntimeError(
                'Service "{}" already registered'.format(service_name)
            )
        self.services[service_name] = service

    def query_service(self, service_name):
        return self.services[service_name]

    def service(self, factory_callable):
        service_name = factory_callable.__name__
        required_service_names = inspect.getargspec(factory_callable).args
        required_services = [
            self.query_service(required_service_name)
            for required_service_name in required_service_names
        ]
        new_service = factory_callable(*required_services)
        self.register(service_name, new_service)
        return factory_callable


class AtDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

service_registry = ServiceRegistry()
