"""
Application-level exceptions.
"""


class AppException(Exception):
    def __init__(self, message: str = "Application error", status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)


class ValidationError(AppException):
    def __init__(self, message: str = "Validation error"):
        super().__init__(message=message, status_code=422)


class ExternalServiceError(AppException):
    def __init__(self, message: str = "External service error"):
        super().__init__(message=message, status_code=502)
