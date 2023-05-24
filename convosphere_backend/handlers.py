from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry

from convosphere_backend.services import MessageService


def grpc_handlers(server):
    app_registry = AppHandlerRegistry("convosphere_backend", server)
    app_registry.register(MessageService)
