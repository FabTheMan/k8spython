import flask
from flask import request, jsonify
from kubernetes.client.api import core_v1_api
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import time
import os
import yaml

app = flask.Flask(__name__)
app.config["DEBUG"] = False

def create_Pod(yamlPath, namePod):

    with open(yamlPath) as f:
        dep = yaml.safe_load(f)
        resp = core_v1.create_namespaced_pod(body=dep, namespace="default")

    while True:
        #resp = k8s_core_v1.read_namespaced_pod(name=NAMEPOD, namespace='default')
        resp = core_v1.read_namespaced_pod_status(name=namePod, namespace='default')

        if resp.status.phase == 'Failed':
            return "Failure"

        if resp.status.phase == 'Succeeded' or resp.status.phase == 'Running' :
            return "Success"

        time.sleep(1)

def container_Status_In_Pod(namePod):
    resp = core_v1.read_namespaced_pod_status(name=namePod, namespace='default')

    if (resp.status.container_statuses[0].state.terminated is not None):
        return resp.status.container_statuses[0].state.terminated.reason
    else:
        return "unknown"

def log_Container_In_Pod(namePod):
    resp = core_v1.read_namespaced_pod_log(name=namePod, namespace='default')
    return resp

def delete_The_Pod(namePod):
    resp = core_v1.delete_namespaced_pod(name=namePod, namespace='default')
    if resp is not None:
        return "success"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/runPod', methods=['GET'])
def run_pod():
    query_parameters = request.args

    # Check if all the parameters are in query string
    if ('namePod' in request.args) and ('nameContainer' in request.args) and ('scriptPath' in request.args) :
        namePod = query_parameters.get('namePod')
        nameContainer = query_parameters.get('nameContainer')
        scriptPath = query_parameters.get('scriptPath')
    else:
        return jsonify("Failure: wrong parameters"),404

    # Create the temp YAML to be used for actual deployment
    str = open("{}/k8sDeployTemplate.yaml".format(CURR_DIR), 'r').read().format(PodName = namePod, ContainerName = nameContainer, ScriptPath = scriptPath)
    open("{}/k8sDeploy.yaml".format(CURR_DIR), 'w').write(str)

    result = create_Pod("{}/k8sDeploy.yaml".format(CURR_DIR), namePod)
    os.remove("{}/k8sDeploy.yaml".format(CURR_DIR))

    return jsonify(result)

@app.route('/api/statusPod', methods=['GET'])
def status_container_in_pod():
    query_parameters = request.args

    # Check if all the parameters are in query string
    if ('namePod' in request.args) :
        namePod = query_parameters.get('namePod')
    else:
        return jsonify("Failure: wrong parameters"),404

    result = container_Status_In_Pod(namePod)
    return jsonify(result)

@app.route('/api/logPod', methods=['GET'])
def log_container_in_pod():
    query_parameters = request.args

    # Check if all the parameters are in query string
    if ('namePod' in request.args) :
        namePod = query_parameters.get('namePod')
    else:
        return jsonify("Failure: wrong parameters"),404

    result = log_Container_In_Pod(namePod)
    return jsonify(result)

@app.route('/api/deletePod', methods=['GET'])
def delete_pod():
    query_parameters = request.args

    # Check if all the parameters are in query string
    if ('namePod' in request.args) :
        namePod = query_parameters.get('namePod')
    else:
        return jsonify("Failure: wrong parameters"),404

    result = delete_The_Pod(namePod)
    return jsonify(result)

if __name__ == "__main__":
    
    # Load kubeConfig
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    config.load_kube_config(config_file="{}/myConfig".format(CURR_DIR))
    core_v1 = core_v1_api.CoreV1Api()
    app.run(host='0.0.0.0')
