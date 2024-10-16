import socket
import struct
from typing import Tuple, Protocol, Generator, runtime_checkable

STRUCT_PACK_FORMAT = "<IIII"


class PyStreamBaseError(BaseException):
    pass


class PyStreamSenderError(PyStreamBaseError):
    pass


@runtime_checkable
class DataGeneratorProtocol(Protocol):
    def generate(self) -> Generator[Tuple[int, bytes], None, None]:
        pass


class Sender:
    def __init__(self, host: str, port: int, packet_size: int):
        # Initialize private member variables
        self._host = ""
        self._port = 0
        self._packet_size = 0

        # Set member variables with property
        self.host = host
        self.port = port
        self.packet_size = packet_size

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str) -> None:
        try:
            socket.inet_aton(value)
        except socket.error:
            raise ValueError(f"host must be an IPv4 formated string, but got '{type(value)}: {value}'")
        self._host = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        if isinstance(value, int) and 0 <= value <= 65535:
            self._port = value
            return
        raise ValueError(f"port must be an integer that is between 0 and 65535, but got '{type(value)}: {value}'")

    @property
    def address(self) -> Tuple[str, int]:
        return self.host, self.port

    @property
    def packet_size(self) -> int:
        return self._packet_size

    @packet_size.setter
    def packet_size(self, value: int) -> None:
        if isinstance(value, int):
            if struct.calcsize(STRUCT_PACK_FORMAT) < value <= 65536:
                self._packet_size = value - struct.calcsize(STRUCT_PACK_FORMAT)
                return
        raise ValueError(
            f"packet_size must be an integer that is between {struct.calcsize(STRUCT_PACK_FORMAT) + 1} and 65535, but got '{type(value)}: {value}'")

    def run(self, generator: DataGeneratorProtocol) -> None:
        meta: int
        data: bytes

        if not isinstance(generator, DataGeneratorProtocol):
            raise TypeError("generator must be DataGeneratorProtocol object")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with sock:
            data_index = 1
            while True:
                try:
                    meta_data, data = generator.generate()

                    offset_range = range(0, len(data), self.packet_size)
                    packet_count = len(offset_range)
                    for packet_index, offset in enumerate(offset_range, start=1):
                        packet = (
                                struct.pack(STRUCT_PACK_FORMAT, meta_data, data_index, packet_count, packet_index) +
                                data[offset:offset + self.packet_size]
                        )
                        sock.sendto(packet, self.address)

                    data_index += 1
                except StopIteration:
                    break
                except Exception as e:
                    raise PyStreamSenderError() from e
