class AppError(Exception):
    """Base exception for application-level errors"""

    def __init__(sefl, message: str, code: str = "APPLICATION_ERROR"):
        sefl.message = message
        sefl.code = code
        super().__init__(message)
