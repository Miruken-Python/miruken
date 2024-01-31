import inspect
import importlib
import functools


class handles2:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args):
        return self.fn(*args)

    def __get__(self, obj, cls=None):
        if not obj:
            # Decorating an unbound function
            return self
        else:
            # Decorating a bound method
            return functools.partial(self, obj)


class HandlerRepository:
    def __init__(self):
        self.handlers = {}

    def register(self, fn):
        params = list(inspect.signature(fn).parameters.values())
        if params and params[0].name == 'self':  # If the first parameter is 'self'
            params = params[1:]  # Skip the 'self' parameter
        annotated_params = (p for p in params if p.annotation != p.empty)
        first_annotated_param = next(annotated_params, None)
        if first_annotated_param:
            message_type = first_annotated_param.annotation
            if message_type not in self.handlers:
                self.handlers[message_type] = []
            self.handlers[message_type].append(fn)
        return fn

    def handle(self, message):
        message_type = type(message)
        for handler in self.handlers.get(message_type, []):
            cls = self.get_class(handler)
            if cls is not None:
                instance = cls()
                handler(instance, message)
            else:
                handler(message)

    @staticmethod
    def get_class(fn):
        cls_name_parts = fn.__qualname__.split('.')
        if len(cls_name_parts) <= 1:
            return None
        module_name = fn.__module__
        module = importlib.import_module(module_name)
        cls = getattr(module, cls_name_parts[0])
        for part in cls_name_parts[1:-1]:  # Exclude the method name
            cls = getattr(cls, part, None)
        return cls


handlers = HandlerRepository()
handles = handlers.register
