"""
# pystream/exceptions.py

Defines Exception class used throughout the `pystream` package.

This module centralizes Exception classes to improve maintainability and readability,
by providing a clear hierarchy of errors.

Exception Hierarchy:
    PyStreamBaseException (Based on built-in Exception)
    ├── ValidationError
    │   ├── InvalidIPAddressError
    │   ├── InvalidPortError
    │   └── InvalidPacketSizeError
"""


class PyStreamBaseException(Exception):
    pass


# ===== pystream.utils.validation.py ===== #
class ValidationError(PyStreamBaseException):
    pass


class InvalidIPAddressError(ValidationError):
    pass


class InvalidPortError(ValidationError):
    pass


class InvalidPacketSizeError(ValidationError):
    pass


# ===== pystream.core =====
class PyStreamCoreError(PyStreamBaseException):
    pass


class StreamError(PyStreamCoreError):
    pass


class FailedToDataGenerationError(StreamError):
    pass


class FailedToCreatePacketError(StreamError):
    pass


class FailedToSendPacketError(StreamError):
    pass
