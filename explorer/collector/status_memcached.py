from telnetlib import Telnet


def telnet_connect(pod_ip):
    con = Telnet(pod_ip, 11211)
    con.write(('stats\r\n').encode('utf-8'))
    con.write(('quit\r\n').encode('utf-8'))
    return con


def get_stats(pod_ip):
    con = telnet_connect(pod_ip)
    for line in con.read_until(b'END').splitlines()[:-1]:
        if 'STAT' not in line.decode('utf-8'):
            continue
        fields = line.decode('utf-8').split()
        if len(fields) > 3:
            continue
        k,v = line.decode('utf-8').split()[1:]
        try:
            if '.' in v:
                yield(k.strip(), float(v.strip()))
            else:
                yield(k.strip(), int(v.strip()))
        except:
            pass
        

def main(pod_ip, namespace, pod_name, v1):
    memcached_status = []
    for tup in get_stats(pod_ip):
        if tup[0] == "id":
            continue
        memcached_status.append('memcache_status{mode="%s", namespace="%s", k8s="1"} %s' % (tup[0], namespace, tup[1]))
    return "\n".join(memcached_status)
