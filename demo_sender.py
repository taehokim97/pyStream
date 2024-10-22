import cv2
import numpy as np

from pystream.core import stream_via_udp


def frame_generator():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("sender", frame)

        ret, byte = cv2.imencode(".jpg", frame)
        if not ret:
            break

        yield 0, byte.tobytes()

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    stream_via_udp(frame_generator(), "192.168.0.21", 12345, 32768 - 16)
