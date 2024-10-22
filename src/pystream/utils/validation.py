"""
Utility functions for data validation
"""

import socket

from pystream.constants import PACKET_HEADER_SIZE, PACKET_MAX_SIZE
from pystream.exceptions import (InvalidIPAddressError, InvalidPacketSizeError,
                                 InvalidPortError)


def __is_exact_int(value: int) -> bool:
    # Note: `isinstance(value, int)` would consider `bool` values (`True` and `False`) as valid `int` types
    # because `bool` is a subclass of `int`. To strictly allow only `int` values, we use `type(value) is int`,
    # which ensures that `True` and `False` are not accepted.
    return type(value) is int


def validate_ipv4_address(value: str) -> None:
    """
    Validates whether a given string is a valid IPv4 address.

    :param value: The IPv4 address to validate as a string (e.g., "192.168.0.1").
    :type value: str
    :return: None
    :raises InvalidIPAddressError: If the input is not a string or not a valid IPv4 address format.

    :example:
        >>> validate_ipv4_address("192.168.0.1")
        # No exception raised

        >>> validate_ipv4_address("192.168.0.300")
        InvalidIPAddressError: Format of value mst be IPv4, but got '192.168.0.300'

        >>> validate_ipv4_address(True)
        InvalidIPAddressError: Type of value must be string, but got '<class 'bool'>'

    :note:
        This function uses 'socket.inet_pton' for validation
    """
    try:
        socket.inet_pton(socket.AF_INET, value)
    except TypeError as e:
        raise InvalidIPAddressError(
            f"Type of value must be string, but got {type(value)}"
        ) from e
    except OSError as e:
        raise InvalidIPAddressError(
            f"Format of value must be IPv4, but got {value}"
        ) from e


def validate_port(value: int) -> None:
    """
    Validates whether a given value is a valid IPv4 port.

    :param value: The IPv4 port to validate as int (e.g. 80)
    :type value: int
    :return: None
    :raises InvalidPortError: If the input is not an int or a invalid range.

    :example:
        >>> validate_port(80)
        # No exception raised
        >>> validate_port(True)
        InvalidPortError: Port must be an integer, but got <class 'int'>
        >>> validate_port(-1)
        InvalidPortError: Port must be between 0 and 65535 inclusive, but got -1
    """
    if not __is_exact_int(value):
        raise InvalidPortError(f"Port must be an integer, but got {type(value)}")
    elif value < 0 or value > 65535:
        raise InvalidPortError(
            f"Port must be between 0 and 65535 inclusive, but got {value}"
        )


def validate_packet_size(value: int) -> None:
    """
    Validates whether a given value is a valid packet size.

    :param value: The packet size to validate as a int (e.g. 1024)
    :type value: int
    :return: None
    :raises InvalidPacketSizeError: If the input is not an int or a invalid packet size.

    :example:
        >>> validate_packet_size(1024)
        # No exception raised
        >>> validate_packet_size(None)
        InvalidPacketSizeError: Packet size must be an integer, but got <class 'int'>
        >>> validate_packet_size(-1)
        InvalidPacketSizeError: Packet size must be between 0 and {PACKET_MAX_SIZE - PACKET_HEADER_SIZE} inclusive, but got -1
        # Check out PACKET_MAX_SIZE and PACKET_HEADER_SIZE in pystream/constants.py
    """
    if not __is_exact_int(value):
        raise InvalidPacketSizeError(
            f"Packet size must be an integer, but got {type(value)}"
        )
    elif not 0 < value <= PACKET_MAX_SIZE - PACKET_HEADER_SIZE:
        raise InvalidPacketSizeError(
            f"Packet size must greater than 0 and less than {PACKET_MAX_SIZE - PACKET_HEADER_SIZE}"
            f", but got {value}"
        )
