from idapi.api.base import BaseAPI

api_version = 'rbac.authorization.k8s.io/v1'


class Role(BaseAPI):
    api_version = api_version
    kind = 'ClusterRole'


class ClusterRole(BaseAPI):
    api_version = api_version
    kind = 'ClusterRole'


class RoleBinding(BaseAPI):
    api_version = api_version
    kind = 'RoleBinding'


class ClusterRoleBinding(BaseAPI):
    api_version = api_version
    kind = 'ClusterRoleBinding'
