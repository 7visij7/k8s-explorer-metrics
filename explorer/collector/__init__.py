from explorer.collector import store_metric
from multiprocessing import Pool
from kubernetes import client
from datetime import datetime
import importlib
import time
import re
import os


def get_bearer():
    with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as fd:
        BEARER_TOKEN = fd.read()
    return BEARER_TOKEN


def k8s_instance():
    BEARER_TOKEN = get_bearer()
    configuration = client.Configuration()
    configuration.api_key["authorization"] = get_bearer()
    configuration.api_key_prefix['authorization'] = 'Bearer' 
    configuration.host = os.environ['K8S_HOST']
    #configuration.host = 'https://10.13.254.124:6443'
    configuration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
    v1 = client.CoreV1Api(client.ApiClient(configuration))
    return v1


def get_pods_kuber(v1):
    pods_list = v1.list_pod_for_all_namespaces(watch=False)
    return pods_list


def dynamic_import(module):
    return importlib.import_module(module)


# def get_pods(namespase='default'):
#     url = 'https://10.13.254.124:6443/api/v1/namespaces/monitoring/pods'
#     header = {'Authorization': 'Bearer {}'.format(get_bearer()),
#               'Content-type': 'application/json'}
#     response = requests.get(url, headers=header, verify='/var/run/secrets/kubernetes.io/serviceaccount/ca.crt')
#     return response.json(), response.status_code


def update():
    start_time = datetime.now()
    metrics = []
    #pool = Pool(100)
    v1 = k8s_instance()
    ret = get_pods_kuber(v1)
    for i in ret.items:
        pods_list.append(i)
        pods_list.append("%s, %s, %s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
        comp = re.findall(r'beanstalk|gearman|memcached|workers|backend', i.metadata.name)
        if comp:
            try:
                collect_module = dynamic_import('explorer.collector.status_%s' % i.metadata.labels['app'])
                result = collect_module.main(i.status.pod_ip, i.metadata.namespace, i.metadata.name, v1)
                metrics.append(result) 
                metrics.append("\n")
            except Exception:
                pass
            async_task = pool.apply_async(collect_module.main, (i.status.pod_ip, i.metadata.namespace, i.metadata.name, v1,))
            result = (async_task.get(timeout=2),)
            for line in result:
                metrics.append(line) 
                metrics.append("\n")
    pool.close()
    pool.join()    
    end_time = datetime.now()
    store_metric.write_metrics(''.join(metrics))
    return 'Update succesfull'

def forever():
    while 1 > 0:
        update()
        time.sleep(60)
