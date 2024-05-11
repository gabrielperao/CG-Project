def singleton(cls):
    instances = dict()

    def get_instance(*args, **kwargs) -> object:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
