from collections import Counter
import subprocess
import json
import os


def cgi_fcgi_request(ip, port, uri):
    os.environ['SCRIPT_NAME'] = uri
    os.environ['SCRIPT_FILENAME'] = ''
    os.environ['QUERY_STRING'] = 'full&json'
    os.environ['REQUEST_METHOD'] = 'GET'
    addr = '%s:%s' % (ip, port)
    cmd = 'cgi-fcgi -bind -connect %s' % addr
    try:
        data = subprocess.check_output(cmd, shell=True)
        for line in data.decode().splitlines():
            try:
                yield json.loads(line)
            except ValueError:
                pass
    except subprocess.CalledProcessError:
        import traceback
        print(traceback.format_exc())


def main(pod_ip, namespace, pod_name, v1):
    phpfpm_status = []
    port = "9000"
    uri = "/health"
    try:
        for item in cgi_fcgi_request(pod_ip, port, uri):
            print(pod_ip, port,namespace)
            phpfpm_status.append('phpfpm_pool_stat_active_processes{namespace="%s", k8s="1"} %s' % (namespace, item['active processes']))
            phpfpm_status.append('phpfpm_pool_stat_accepted_conn{namespace="%s", k8s="1"} %s' % (namespace,  item['accepted conn']))
            phpfpm_status.append('phpfpm_pool_stat_listen_queue{namespace="%s", k8s="1"} %s' % (namespace,  item['listen queue']))
            phpfpm_status.append('phpfpm_pool_stat_start_since{namespace="%s", k8s="1"} %s' % (namespace,  item['start since']))
            phpfpm_status.append('phpfpm_pool_stat_idle_processes{namespace="%s", k8s="1"} %s' % (namespace,  item['idle processes']))
            phpfpm_status.append('phpfpm_pool_stat_start_time{namespace="%s", k8s="1"} %s' % (namespace,  item['start time']))
            phpfpm_status.append('phpfpm_pool_stat_slow_requests{namespace="%s", k8s="1"} %s' % (namespace,  item['slow requests']))
            phpfpm_status.append('phpfpm_pool_stat_max_active_processes{namespace="%s", k8s="1"} %s' % (namespace,  item['max active processes']))
            phpfpm_status.append('phpfpm_pool_stat_max_children_reached{namespace="%s", k8s="1"} %s' % (namespace,  item['max children reached']))
            phpfpm_status.append('phpfpm_pool_stat_max_listen_queue{namespace="%s", k8s="1"} %s' % (namespace,  item['max listen queue']))
            phpfpm_status.append('phpfpm_pool_stat_total_processes{namespace="%s", k8s="1"} %s' % (namespace,  item['total processes']))
            phpfpm_status.append('phpfpm_pool_stat_listen_queue_len{namespace="%s", k8s="1"} %s' % (namespace,  item['listen queue len']))
            proc_count = 0
            states_counter = Counter()
            for proc in item['processes']:
                states_counter.update([proc['state']])
                proc_count += 1
            for k, v in iter(states_counter.items()):
                phpfpm_status.append('phpfpm_pool_stat_process_states{namespace="%s", state="%s", k8s="1"} %s' % (namespace,  k, v))
            phpfpm_status.append('phpfpm_pool_stat_processes_count{namespace="%s"} %s' % (namespace,  proc_count))
    except TypeError:
        import traceback
        print(traceback.format_exc())
    return "\n".join(phpfpm_status)
