import requests

URI = 'metrics'
PORT = '10254'


def get_metrics(pod_ip):
    url = 'http://{}:{}/{}'.format(pod_ip, PORT, URI)
    req = requests.get(url)
    return 


def main(pod_ip, namespace, pod_name, v1):
    ingress_metrics = []
    ingress_metrics.append()
    return "\n".join(ingress_metrics)
