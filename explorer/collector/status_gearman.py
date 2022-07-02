from company.network import discovery_sockets
from company.coding import rchop, lchop
import socket
import re


METRIC_NAME = 'gearman_status'


def get_appver(queue_name):
    try:
        assert '|' in queue_name
        return queue_name.split('|')[0]
    except:
        return


def get_shard_num(queue_name):
    try:
        m = re.findall('shard_([0-9.]+)$', queue_name)
        assert m
        return m[-1]
    except:
        return


def get_segment_num(queue_name):
    try:
        m = re.findall('\.(\d+)$', queue_name)
        assert m
        return m[-1]
    except:
        return


def get_lines_from_socket(pod_ip):
    """Yields the output of Gearman response to 'status' command."""
    gearman = socket.socket()
    gearman.connect((pod_ip, 4730))

    gearman.send(b'status\n')
    gearman_response = ''
    while True:
        buf = gearman.recv(1024).decode('utf-8')
        if not buf:
            break
        elif buf.endswith('.\n'):
            gearman_response += buf[:-3]
            break
        gearman_response += buf
    gearman.close()

    for line in gearman_response.split('\n'):
        yield line


def main(pod_ip, namespace, pod_name, v1):
    gearman_status = []
    for line in get_lines_from_socket(pod_ip):
        if not line:
                continue
        original_queue_name, values = line.split(None, 1)
        runtime_queue_name = original_queue_name
        # if line contains .\d+ in the end - this is segment, chop it!
        segment_num = get_segment_num(runtime_queue_name)
        if segment_num:
            runtime_queue_name = rchop(runtime_queue_name, '.%s' % segment_num)
        # if line contains shard_\d+ in the end - this is shard, chop it!
        shard_num = get_shard_num(runtime_queue_name)
        if shard_num:
            runtime_queue_name = rchop(runtime_queue_name, '|shard_%s' % shard_num)
        # if line contains | - text before| is a appver
        appver = get_appver(runtime_queue_name)
        if appver:
            runtime_queue_name = lchop(runtime_queue_name, '%s|' % appver)
        # all other is a worker name
        # sorry for this pizdets
        worker_name = runtime_queue_name
        for mode, value in iter(zip(['queue', 'running', 'workers'], values.split())):
            gearman_status.append('%s{name="%s", app="%s", shard="%s", segment="%s", worker_name="%s", mode="%s", namespace="%s", k8s="1"} %s' % (
                METRIC_NAME,
                original_queue_name,
                appver,
                shard_num,
                segment_num,
                worker_name,
                mode,
                namespace,
                value))
    return "\n".join(gearman_status)
