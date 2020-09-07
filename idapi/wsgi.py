import flask
import os

from functools import wraps
from kubernetes import client, config
from openshift.dynamic import DynamicClient
from openshift.dynamic import exceptions as openshift_exceptions

from idapi.api import OpenShiftAPI
from idapi.app import App
from idapi.exc import ApplicationError, ResourceExistsError, ResourceNotFoundError


def handle_http_errors(func):
    @wraps(func)
    def _(*args, **kwargs):
        global app
        try:
            return func(*args, **kwargs)
        except openshift_exceptions.NotFoundError as err:
            return app.make_response((
                {
                    'status': 'error',
                    'code': err.status,
                    'reason': err.reason,
                }, err.status
            ))
        except ValueError as err:
            return app.make_response((
                {
                    'status': 'error',
                    'code': 500,
                    'reason': str(err),
                }, 500
            ))
        except ApplicationError as err:
            return app.make_response((
                {
                    'status': 'error',
                    'code': err.status,
                    'reason': str(err),
                }, 409
            ))

    return _


if os.environ.get('USE_K8S_SA'):
    config.load_incluster_config()
else:
    config.load_kube_config()

k8api = client.ApiClient()
dynclient = DynamicClient(k8api)
api = OpenShiftAPI(dynclient)
app = App(__name__, api)


@app.route('/user/<user>')
@handle_http_errors
def get_user(user):
    return app.get_user(user)


@app.route('/user/<user>', methods=['DELETE'])
@handle_http_errors
def delete_user(user):
    return app.delete_user(user)


@app.route('/user', methods=['POST'])
@handle_http_errors
def create_user():
    if not flask.request.is_json:
        raise ValueError('expected json data')

    data = flask.request.get_json()
    user = data['user']
    full_name = data.get('full_name')

    if not app.exists_user(user):
        return app.create_user(user, full_name=full_name)
    else:
        raise ResourceExistsError('User', user)


@app.route('/project/<project>')
@handle_http_errors
def get_project(project):
    return app.get_project(project)


@app.route('/project/<project>', methods=['DELETE'])
@handle_http_errors
def delete_project(project):
    return app.delete_project(project)


@app.route('/project', methods=['POST'])
@handle_http_errors
def create_project():
    if not flask.request.is_json:
        raise ValueError('expected json data')

    data = flask.request.get_json()
    project = data['project']

    if not app.exists_project(project):
        return app.create_project(project,
                                  requester=data.get('requester'),
                                  display_name=data.get('display_name'))
    else:
        raise ResourceExistsError('Project', project)


@app.route('/project/<project>/role', methods=['POST'])
@handle_http_errors
def create_rolebinding(project):
    if not flask.request.is_json:
        raise ValueError('expected json data')

    data = flask.request.get_json()
    role = data['role']

    return app.create_rolebinding(project, role)


@app.route('/project/<project>/role/<role>')
@handle_http_errors
def get_rolebinding(project, role):
    return app.get_rolebinding(project, role)


@app.route('/project/<project>/role/<role>', methods=['DELETE'])
@handle_http_errors
def delete_rolebinding(project, role):
    return app.delete_rolebinding(project, role)


@app.route('/project/<project>/role/<role>', methods=['POST'])
@handle_http_errors
def add_user_to_rolebinding(project, role):
    if not flask.request.is_json:
        raise ValueError('expected json data')

    data = flask.request.get_json()
    user = data['user']

    if not app.exists_rolebinding(project, role):
        app.create_rolebinding(project, role)

    return app.add_user_to_rolebinding(project, role, user)


@app.route('/project/<project>/role/<role>/user/<user>', methods=['DELETE'])
@handle_http_errors
def remove_user_from_rolebinding(project, role, user):
    return app.remove_user_from_rolebinding(project, role, user)