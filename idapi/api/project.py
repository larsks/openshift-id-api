from idapi.api.base import BaseAPI


class Project(BaseAPI):
    api_version = 'project.openshift.io/v1'
    kind = 'Project'

    def create(self, name, display_name=None, requester=None):
        proj = {
            'apiVersion': self.api_version,
            'kind': self.kind,
            'metadata': {
                'name': name,
            }
        }

        if display_name:
            proj['metadata']['annotations'] = {
                'openshift.io/display-name': display_name
            }

        if requester:
            proj['metadata']['annotations'] = {
                'openshift.io/requester': requester
            }

        super().create(proj)
