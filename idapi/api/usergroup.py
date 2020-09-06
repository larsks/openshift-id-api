from idapi.api.base import BaseAPI

api_version = 'user.openshift.io/v1'


class User(BaseAPI):
    api_version = api_version
    kind = 'User'

    def create(self, name, full_name):
        user = {
            'apiVersion': self.api_version,
            'kind': self.kind,
            'metadata': {
                'name': name,
            },
            'fullName': full_name,
        }

        return super().create(user)


class Identity(BaseAPI):
    api_version = api_version
    kind = 'Identity'


class Group(BaseAPI):
    api_version = api_version
    kind = 'Group'

    def create(self, name, **kwargs):
        group = {
            'apiVersion': self.api_version,
            'kind': self.kind,
            'metadata': {
                'name': name,
            },
        }

        return super().create(group)

    def add_user(self, name, username):
        old = self.get(name)
        new = {
            'apiVersion': self.api_version,
            'kind': self.kind,
            'metadata': {
                'name': name,
            },
            'users': old['users'] + [username]
        }

        return self.patch(new)

    def remove_user(self, name, username):
        old = self.get(name)
        new = {
            'apiVersion': self.api_version,
            'kind': self.kind,
            'metadata': {
                'name': name,
            },
            'users': old['users']
        }

        try:
            new['users'].remove(username)
            return self.patch(new)
        except ValueError:
            return old
