class ApplicationError(Exception):
    status = 500

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


class ResourceExistsError(ApplicationError):
    status = 409

    def __init__(self, rtype, rname):
        reason = f'{rtype} resource {rname} already exists'
        super().__init__(reason)


class ResourceNotFoundError(ApplicationError):
    status = 404

    def __init__(self, rtype, rname):
        reason = f'{rtype} resource {rname} does not exist'
        super().__init__(reason)


class AccessDeniedError(ApplicationError):
    status = 403

    def __init__(self):
        super().__init__('Access requires authorization')
