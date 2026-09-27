class AppError(Exception):
    status_code = 500
    detail = "Internal server error"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)

class NotFoundError(AppError):
    status_code = 404
    detail = "Resource not found"

class ConflictError(AppError):
    status_code = 409
    detail = "Conflict with existing data"

class InvalidReferenceError(AppError):
    """Raised when a foreign key (e.g. category_id) points at something that doesn't exist."""
    status_code = 422
    detail = "Referenced resource does not exist"
