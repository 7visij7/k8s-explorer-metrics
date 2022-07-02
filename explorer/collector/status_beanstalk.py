from telnetlib import Telnet


def telnet_connect(pod_ip, cmd):
    con = Telnet(pod_ip, 11300)
    con.write(('%s\r\n' %cmd).encode('utf-8'))
    con.write(('quit\r\n').encode('utf-8'))
    return con


def get_stats(pod_ip):
    con = telnet_connect(pod_ip, 'stats')
    #a = con.read_all().split(b'\n')
    for line in con.read_until(b'hostname').splitlines()[:-1]:
        if b':' in line:
            k,v = line.decode('utf-8').split(':')
            yield (k.strip(), v.strip())


def get_tubes(pod_ip):
    con = telnet_connect(pod_ip, 'list-tubes')
    for tubes in con.read_all().splitlines()[2:-1]:
        yield (tubes.decode('utf-8').strip('- '))


def get_tube_stats(pod_ip, tube):
    con = telnet_connect(pod_ip, 'stats-tube %s' %tube)
    for line in con.read_all().splitlines()[3:-1]:
        if b':' in line:
            k,v = line.decode('utf-8').split(':')
            yield (k.strip(), v.strip())


def main(pod_ip, namespace, pod_name, v1):
    beanstalk_status = []
    for tup in get_stats(pod_ip):
        if 'jobs' in tup[0] or tup[0]== 'id':
            continue
        beanstalk_status.append('beanstalk_status{tube="default", mode="%s", namespace="%s", k8s="1"} %s' % (
            tup[0], 
            namespace,
            tup[1]))

    for tube in get_tubes(pod_ip):
        for stat in get_tube_stats(pod_ip, tube):
            beanstalk_status.append('beanstalk_status{tube="%s", mode="%s", namespace="%s", k8s="1"} %s' % (
                tube, 
                stat[0], 
                namespace,
                stat[1]))
    return "\n".join(beanstalk_status)