class InvalidParams(Exception):
    """
    raised when a function or method is called
    using invalid data types for parameter(s)
    """
    pass


class InvalidFilename(Exception):
    """
    raised when attempting to open a file
    for using an invalid filename
    """
    pass


class BadRequest(Exception):
    """
    raised when an unknown exception occurs
    that results from a bad HTTP request
    """
    pass


class BadResponse(Exception):
    """
    raised when an unexpected HTTP response
    body is received
    """
    pass
