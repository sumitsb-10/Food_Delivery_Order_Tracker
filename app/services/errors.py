"""Domain errors used to map service failures to HTTP responses."""


class NotFoundError(ValueError):
    """The requested resource does not exist."""


class ConflictError(ValueError):
    """The request conflicts with existing data or business rules."""
