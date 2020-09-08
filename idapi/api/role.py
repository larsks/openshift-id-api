from .base import BaseAPI

api_version = 'rbac.authorization.k8s.io/v1'


class Role(BaseAPI):
    api_version = api_version
    kind = 'Role'


class ClusterRole(BaseAPI):
    api_version = api_version
    kind = 'ClusterRole'


class RoleBinding(BaseAPI):
    api_version = api_version
    kind = 'RoleBinding'

    def create(self, name, rolename, projectname, users=None, **kwargs):
        rolebinding = {
            'apiVersion': self.api_version,
            'kind': self.kind,
            'metadata': {
                'name': name,
                'namespace': projectname,
            },
            'roleRef': {
                'kind': 'ClusterRole',
                'name': rolename,
            },
            'subjects': [],
        }

        if users:
            rolebinding['subjects'] = [
                {'kind': 'User', 'name': user}
                for user in users
            ]

        return super().create(rolebinding, **kwargs)


class ClusterRoleBinding(BaseAPI):
    api_version = api_version
    kind = 'ClusterRoleBinding'
