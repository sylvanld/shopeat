class RepositoryException(Exception):
    ...


class ObjectAlreadyExistsError(RepositoryException):
    ...


class AuthenticationError(RepositoryException):
    ...
