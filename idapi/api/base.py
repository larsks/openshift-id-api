from openshift.dynamic import exceptions as openshift_exceptions


class BaseAPI(object):
    api_version = None
    kind = None

    def __init__(self, osapi):
        if self.api_version is None or self.kind is None:
            raise NotImplementedError('unknown api version')

        self._api = osapi.resources.get(
            api_version=self.api_version, kind=self.kind)

    def exists(self, name):
        try:
            self._api.get(name)
        except openshift_exceptions.NotFoundError:
            return False
        else:
            return True

    def delete(self, name):
        return self._api.delete(name).to_dict()

    def get(self, name):
        return self._api.get(name).to_dict()

    def list(self):
        return self._api.get().to_dict()

    def names(self):
        return [x.metadata.name for x in self._api.get().items]

    def create(self, body, **kwargs):
        return self._api.create(body=body, **kwargs).to_dict()

    def patch(self, body, **kwargs):
        return self._api.patch(body=body, **kwargs).to_dict()
