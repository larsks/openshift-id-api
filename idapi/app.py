import os

from flask import Flask
from kubernetes import client, config
from openshift.dynamic import DynamicClient

app = Flask(__name__)

if os.environ.get('USE_K8S_SA'):
    config.load_incluster_config()
else:
    config.load_kube_config()

k8api = client.ApiClient()
osapi = DynamicClient(k8api)
