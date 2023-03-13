class CouldNotDownloadError(Exception):
    def __init__(self, message="CouldNotDownloadError"):
        super().__init__(message)


class EmptyQueueError(Exception):
    def __init__(self, message="Parser queue is empty"):
        super().__init__(message)


class UnsupportedOptionError(Exception):
    def __init__(self, message="UnsupportedOptionError"):
        super().__init__(message)
