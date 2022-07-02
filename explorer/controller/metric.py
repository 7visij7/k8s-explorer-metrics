from explorer.collector import  get_metric


def search(*args, **kwargs):
    metric = get_metric.read_metrics()
    return metric
