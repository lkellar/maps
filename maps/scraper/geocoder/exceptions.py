
class BingKeyNotFound(BaseException):
    """An exception class to use when the Bing API Key isn't found"""


class BingAPIError(BaseException):
    """An exception class to use when the Bing API throws an error"""


class BingStallError(BaseException):
    """An exception class to use when we hit the pending jobs quota; there must be stalled jobs"""


class BingTimeoutError(BaseException):
    """An exception class to use when a job is pending for too long"""
