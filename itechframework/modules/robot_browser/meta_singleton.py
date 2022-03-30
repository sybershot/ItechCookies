class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls.__qualname__ not in cls._instances:
            cls._instances[cls.__qualname__] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls.__qualname__]
