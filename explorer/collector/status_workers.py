from kubernetes.stream import stream


def main(pod_ip, namespace, pod_name, v1):
    supervisor_status = []
    try:
        command = ['/bin/ash', '-c', 'supervisorctl status all']
        stderr = True  # bool | Redirect the standard error stream of the pod for this call. Defaults to true. (optional)
        stdin = True  # bool | Redirect the standard input stream of the pod for this call. Defaults to false. (optional)
        stdout = True  # bool | Redirect the standard output stream of the pod for this call. Defaults to true. (optional)
        tty = True  # bool | TTY if true indicates that a tty will be allocated for the exec call. Defaults to false. (optional)
        api_response = stream(v1.connect_get_namespaced_pod_exec, pod_name, namespace, command=command, stderr=stderr, stdin=stdin, stdout=stdout, tty=tty)
        for line in api_response.splitlines():
            worker, worker_status = line.split()[0:2]
            print(worker.split(':')[1], worker_status)
            status = 0
            if 'RUNNING' in worker_status:
                status = 1
            supervisor_status.append('supervisor_status{name="%s", state="%s", namespace="%s", k8s="1"} %s' % (
            worker.split(':')[1],
            worker_status,
            namespace,
            status))
    except Exception as e:
        print('%s' %e)
    return "\n".join(supervisor_status)
