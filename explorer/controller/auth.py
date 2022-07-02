from explorer import config


def apikey(*args, **kwargs):
    key = args[0]
    if key != config.API_KEY:
        return
    return {'foo': 'bar'}