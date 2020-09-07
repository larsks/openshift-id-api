from openshift.dynamic import exceptions as openshift_exceptions


class BaseAPI(object):
    api_version = None
    kind = None

    def __init__(self, dynclient):
        if self.api_version is None or self.kind is None:
            raise NotImplementedError('unknown api version')

        self._api = dynclient.resources.get(
            api_version=self.api_version, kind=self.kind)

    def exists(self, name, **kwargs):
        try:
            self._api.get(name, **kwargs)
        except openshift_exceptions.NotFoundError:
            return False
        else:
            return True

    def delete(self, name, **kwargs):
        return self._api.delete(name, **kwargs).to_dict()

    def get(self, name, **kwargs):
        return self._api.get(name, **kwargs).to_dict()

    def list(self, **kwargs):
        return self._api.get(**kwargs).to_dict()

    def names(self, **kwargs):
        return [x.metadata.name for x in self._api.get(**kwargs).items]

    def create(self, body, **kwargs):
        return self._api.create(body=body, **kwargs).to_dict()

    def apply(self, body, **kwargs):
        return self._api.apply(body, **kwargs).to_dict()

    def patch(self, body, **kwargs):
        return self._api.patch(body=body, **kwargs).to_dict()
