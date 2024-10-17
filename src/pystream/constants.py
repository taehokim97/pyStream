"""
pystream/constants.py

Defines constants used throughout the `pystream` package.

This module centralizes key constants to improve maintainability and readability
by avoiding "magic numbers" spread across multiple files.
"""
import struct

# About UDP packet
STRUCT_PACK_FORMAT = "<IIII"
PACKET_HEADER_SIZE = struct.calcsize(STRUCT_PACK_FORMAT)
# https://en.wikipedia.org/wiki/User_Datagram_Protocol @ UDP datagram structure
# ... However, the actual limit for the data length, which is imposed by the underlying IPv4 protocol,
# is 65,507 bytes (65,535 bytes − 8-byte UDP header − 20-byte IP header).[8]
PACKET_MAX_SIZE = 65507




