from .user import User, Group, Identity
from .project import Project
from .role import Role, ClusterRole, RoleBinding, ClusterRoleBinding


class OpenShiftAPI(object):
    def __init__(self, dynclient):
        self.user = User(dynclient)
        self.group = Group(dynclient)
        self.identity = Identity(dynclient)
        self.project = Project(dynclient)
        self.role = Role(dynclient)
        self.clusterrole = ClusterRole(dynclient)
        self.rolebinding = RoleBinding(dynclient)
        self.clusterrolebinding = ClusterRoleBinding(dynclient)
