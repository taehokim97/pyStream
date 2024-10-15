import socket
import struct


class PyStreamBaseError(BaseException):
    pass


class PyStreamSenderError(PyStreamBaseError):
    pass


class Sender:
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        meta: int
        data: bytes
        while True:
            try:
                # TODO: 다른 객체에 위임
                meta, data = None
            except StopIteration:
                break
            except Exception as e:
                raise PyStreamSenderError() from e
            else:
                rng = range(0, len(data), self.packet_size)
                packet_count = len(rng)
                for packet_index, seek in enumerate(rng, 1):
                    packet = (
                            struct.pack("III", meta, packet_count, packet_index) +
                            data[seek:seek + self.packet_size]
                    )
                    sock.sendto(packet, self.address)
