import flask

from kubernetes import client
from openshift.dynamic import DynamicClient

from idapi.api import OpenShiftAPI


class Response(flask.Response):
    default_mimetype = 'application/json'


class App(flask.Flask):
    response_class = Response
    valid_roles = ['admin', 'edit', 'view']
    rbprefix = 'moc-'

    def rolebinding_name_from_role(self, role):
        return f'{self.rbprefix}{role}'

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

        self.logger.info('creating api client')
        k8api = client.ApiClient()
        dynclient = DynamicClient(k8api)
        self.api = OpenShiftAPI(dynclient)
        self.logger.info('finished starting up')

    def get_user(self, user):
        self.logger.info('get user %s', user)
        return self.api.user.get(user)

    def delete_user(self, user):
        u = self.api.user.get(user)
        self.logger.info('delete user %s', user)
        if u.get('identities') is not None:
            for ident in u['identities']:
                self.logger.debug('delete identity %s for user %s',
                                  ident, user)
                self.api.identity.delete(ident)

        return self.api.user.delete(user)

    def exists_user(self, user):
        self.logger.info('exists user %s', user)
        return self.api.user.exists(user)

    def create_user(self, user, full_name=None):
        self.logger.info('create user %s (%s)', user, full_name)
        return self.api.user.create(user, full_name=full_name)

    def get_project(self, project):
        self.logger.info('get project %s', project)
        return self.api.project.get(project)

    def delete_project(self, project):
        self.logger.info('delete project %s', project)
        return self.api.project.delete(project)

    def exists_project(self, project):
        self.logger.info('exists project %s', project)
        return self.api.project.exists(project)

    def create_project(self, project, requester=None, display_name=None):
        self.logger.info('create project %s (%s) for %s',
                         project,
                         display_name,
                         requester)
        return self.api.project.create(project,
                                       requester=requester,
                                       display_name=display_name)

    def get_rolebinding(self, project, role):
        if role not in self.valid_roles:
            raise ValueError(role)

        rbname = self.rolebinding_name_from_role(role)
        self.logger.info('get rolebinding %s from project %s',
                         rbname,
                         project)
        return self.api.rolebinding.get(rbname, namespace=project)

    def exists_rolebinding(self, project, role):
        rbname = f'moc-{role}'
        self.logger.info('exists rolebinding %s in project %s',
                         rbname,
                         project)
        return self.api.rolebinding.exists(rbname, namespace=project)

    def create_rolebinding(self, project, role):
        if role not in self.valid_roles:
            raise ValueError(role)

        rbname = self.rolebinding_name_from_role(role)
        self.logger.info('create rolebinding %s in project %s',
                         rbname,
                         project)
        return self.api.rolebinding.create(
            rbname, role, project)

    def delete_rolebinding(self, project, role):
        if role not in self.valid_roles:
            raise ValueError(role)

        rbname = self.rolebinding_name_from_role(role)
        self.logger.info('delete rolebinding %s in project %s',
                         rbname,
                         project)
        return self.api.rolebinding.delete(rbname, namespace=project)

    def add_user_to_rolebinding(self, project, role, user):
        if role not in self.valid_roles:
            raise ValueError(role)

        rbname = self.rolebinding_name_from_role(role)
        self.logger.info('add user %s to rolebinding %s in project %s',
                         user, rbname, project)

        rb = self.api.rolebinding.get(rbname, namespace=project)
        if not rb.get('subjects'):
            rb['subjects'] = []

        if not any(x['kind'] == 'User' and x['name'] == user
                   for x in rb['subjects']):
            rb['subjects'].append({
                'kind': 'User',
                'name': user,
            })

        return self.api.rolebinding.apply(rb)

    def remove_user_from_rolebinding(self, project, role, user):
        if role not in self.valid_roles:
            raise ValueError(role)

        rbname = self.rolebinding_name_from_role(role)
        self.logger.info('remove user %s from rolebinding %s in project %s',
                         user, rbname, project)

        rb = self.api.rolebinding.get(rbname, namespace=project)

        rb['subjects'] = [
            sub for sub in rb.get('subjects', [])
            if sub['kind'] != 'User' or sub['name'] != user
        ]

        return self.api.rolebinding.apply(rb)
