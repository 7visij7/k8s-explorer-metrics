import os

def read_metrics():
    f = open(os.environ['METRICS_FILE'], 'r')
    data = f.read()
    f.close()
    return data
