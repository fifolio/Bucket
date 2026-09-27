from postgrest.exceptions import APIError
from app.exceptions import AppError, ConflictError, InvalidReferenceError, NotFoundError

# Postgres SQLSTATE codes worth distinguishing
FOREIGN_KEY_VIOLATION = "23503"
UNIQUE_VIOLATION = "23505"
NOT_NULL_VIOLATION = "23502"

def translate_db_error(e: Exception) -> AppError:
    if isinstance(e, APIError):
        code = getattr(e, "code", None)
        if code == FOREIGN_KEY_VIOLATION:
            return InvalidReferenceError("One of the referenced IDs does not exist")
        if code == UNIQUE_VIOLATION:
            return ConflictError("A resource with that value already exists")
        if code == NOT_NULL_VIOLATION:
            return AppError(detail="A required field was missing")
    return AppError(detail=str(e))