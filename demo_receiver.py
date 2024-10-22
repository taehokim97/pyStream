import threading as th
from queue import Empty, PriorityQueue

import cv2
import numpy as np

from pystream.core import receive_stream_via_udp


def frame_decoder(
    ip: str,
    port: int,
    packet_size: int,
):
    receiver = receive_stream_via_udp(ip, port, packet_size)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        try:
            data_index, data = next(receiver)
        except StopIteration:
            break
        frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("receiver", frame)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    frame_decoder("192.168.0.21", 12345, 32768)
