class ApplicationError(Exception):
    def __init__(self, reason, status=500):
        self.status = status
        self.reason = reason
        super().__init__(reason)


class ResourceExistsError(ApplicationError):
    def __init__(self, rtype, rname):
        self.rtype = rtype
        self.rname = rname
        reason = f'{self.rtype} resource {self.rname} already exists'
        super().__init__(reason, status=409)


class ResourceNotFoundError(ApplicationError):
    def __init__(self, rtype, rname):
        self.rtype = rtype
        self.rname = rname
        reason = f'{self.rtype} resource {self.rname} does not exist'
        super().__init__(reason, status=404)
