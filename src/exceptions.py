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
