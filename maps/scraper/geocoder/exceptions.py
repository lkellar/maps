
class BingKeyNotFound(BaseException):
    """An exception class to use when the Bing API Key isn't found"""


class BingAPIError(BaseException):
    """An exception class to use when the Bing API throws an error"""

class BingStallError(BaseException):
    """An exception class to use when we hit out pending jobs quota which are stalled"""
