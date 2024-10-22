import socket
import struct
from queue import PriorityQueue

from pystream.constants import PACKET_HEADER_SIZE, STRUCT_PACK_FORMAT
from pystream.utils.validation import (
    validate_ipv4_address,
    validate_packet_size,
    validate_port,
)


def receive_stream_via_udp(ip: str, port: int, packet_size: int):
    validate_ipv4_address(ip)
    validate_port(port)
    validate_packet_size(packet_size)

    db = [[[b""] * 100, 0, 0] for _ in range(100)]
    address = (ip, port)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(address)
        sock.setblocking(False)
        sock.settimeout(10)

        while True:
            try:
                byte, _ = sock.recvfrom(packet_size)
            except socket.timeout:
                break
            if not byte:
                break
            (metadata, data_index, packet_index, packet_count) = struct.unpack(
                STRUCT_PACK_FORMAT, byte[:PACKET_HEADER_SIZE]
            )
            db_index = data_index % 100

            if packet_index == 1:
                db[db_index][0]
                db[db_index][1] = 0
                db[db_index][2] = packet_count

            db[db_index][0][packet_index - 1] = byte[PACKET_HEADER_SIZE:]
            db[db_index][1] += 1

            if db[db_index][1] == db[db_index][2]:
                data = b"".join(db[db_index][0][:packet_count])
                yield data_index, data
