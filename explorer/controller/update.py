from explorer import collector
from explorer.collector import store_metric


def search(*args, **kwargs):
    return  collector.update()