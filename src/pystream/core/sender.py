import socket
import struct
import sys
from collections.abc import Iterable
from typing import Generator, Tuple

from pystream.constants import STRUCT_PACK_FORMAT
from pystream.exceptions import FailedToDataGenerationError, FailedToCreatePacketError, FailedToSendPacketError
from pystream.utils.validation import validate_ipv4_address, validate_port, validate_packet_size


def stream_via_udp(generator: Generator[Tuple[int, bytes], None, None],
                   ip: str,
                   port: int,
                   packet_size: int):
    validate_ipv4_address(ip)
    validate_port(port)
    validate_packet_size(packet_size)

    address = (ip, port)
    metadata: int
    data: bytes

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with sock:

        data_index = 1
        while True:
            try:
                item = next(generator)
            except StopIteration:
                break
            except Exception as e:
                raise FailedToDataGenerationError(
                    f"In pystream sender, generator expected stop with StopIteration, but got {type(e).__name__}"
                ) from e

            try:
                metadata, data = item
            except TypeError as e:
                hint = (f"{type(item).__name__} with {len(item)} items"
                        if isinstance(item, Iterable)
                        else type(item).__name__)
                raise FailedToDataGenerationError(
                    f"In pystream sender, generator expected yield Tuple[int, bytes], but got {hint}"
                ) from e

            rng = range(0, len(data), packet_size)
            packet_count = len(rng)
            for packet_index, data_offset in enumerate(rng, start=1):
                try:
                    packet = (
                            struct.pack(STRUCT_PACK_FORMAT, metadata, data_index, packet_count, packet_index) +
                            data[data_offset:data_offset + packet_size]
                    )
                except struct.error as e:
                    raise FailedToCreatePacketError(
                        f"Failed to create packet with metadata {metadata} of size {sys.getsizeof(metadata)} bytes. "
                        f"Ensure metadata is an integer (4 bytes)"
                    ) from e

                try:
                    sock.sendto(packet, address)
                except socket.error as e:
                    raise FailedToSendPacketError(
                        f"Failed to send data of size {len(packet)} bytes to address {address}."
                    ) from e

            data_index += 1
