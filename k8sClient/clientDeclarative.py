from kubernetes import client, config
import time
import os
from os import path
import yaml

#txt1 = "My name is {fname}, I'am {age}".format(fname = "John", age = 36)

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
config.load_kube_config(config_file="{}/myConfig".format(CURR_DIR))

NAMEPOD = "mypod"
NAMECONTAINER = "pythoncontainer"

# Create the temp YAML to be used for actual deployment
str = open("{}/k8sDeployTemplate.yaml".format(CURR_DIR), 'r').read().format(PodName = NAMEPOD, ContainerName = NAMECONTAINER, ScriptPath = '/mnt/azure')
open("{}/k8sDeploy.yaml".format(CURR_DIR), 'w').write(str)


with open(path.join(path.dirname(__file__), "k8sDeploy.yaml")) as f:
    dep = yaml.safe_load(f)
    k8s_core_v1 = client.CoreV1Api()
    resp = k8s_core_v1.create_namespaced_pod(body=dep, namespace="default")

# Delete the YAML used for actual deployment
os.remove("{}/k8sDeploy.yaml".format(CURR_DIR))


while True:
    #resp = k8s_core_v1.read_namespaced_pod(name=NAMEPOD, namespace='default')
    resp = k8s_core_v1.read_namespaced_pod_status(name=NAMEPOD, namespace='default')

    if (resp.status.container_statuses[0].state.terminated is not None):
        if (resp.status.container_statuses[0].state.terminated.reason=='Completed'):
            print("Deployment for pod {}, now has a container status = {}".format(resp.metadata.name, resp.status.container_statuses[0].state.terminated.reason))
        else:
            print("Deployment for pod {}, now has a container status = {}. This is not expected.".format(resp.metadata.name, resp.status.container_statuses[0].state.terminated.reason))
        break

    time.sleep(1)

print ("Now status is completed - checking the log...")

resp = k8s_core_v1.read_namespaced_pod_log(name=NAMEPOD, namespace='default')

print(resp)


# v1 = client.CoreV1Api()

# pod=client.V1Pod()
# pod.metadata=client.V1ObjectMeta(name=NAMEPOD)

# container=client.V1Container(name="C1")
# container.image="python:3"
# container.args=["python3", "https://appealmbs.blob.core.windows.net/lms/service.py"]
# container.name=NAMECONTAINER
# container.volume_mounts


#spec=client.V1PodSpec(containers=[container])

#pod.spec = spec

#v1.create_namespaced_pod(namespace="default",body=pod)

#while True:
#    resp = v1.read_namespaced_pod(name=NAMEPOD,
#                                            namespace='default')
#    if resp.status.phase != 'Pending':
#        break
#    time.sleep(1)

#api_response = api_instance.read_namespaced_pod_log(name=NAMEPOD, namespace='default')
#v1.delete_namespaced_pod(name="busybox", namespace="default", body=client.V1DeleteOptions())



#     volumeMounts:
#       - name: azure
#         mountPath: /mnt/azure
#   volumes:
#   - name: azure
#     azureFile:
#       secretName: azure-secret
#       shareName: aksshare
#       readOnly: false
