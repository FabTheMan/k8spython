from kubernetes import client, config
import os
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
config.load_kube_config(config_file="{}/myConfig".format(CURR_DIR))

v1 = client.CoreV1Api()
print("Listing pods with their IPs:")
ret = v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))