'''
start recording camera and saving the results

In addition, it write down timestamp in txt file.
In does not include distortion removing logic. I will apply it later.
but I need to set the cv2. width t640, 480

'''
import time

import cv2

from PyQt5.QtCore import QObject, QThread



class CameraRecorder(QThread):
    """
    FrameSaver saves frames and their corresponding timestamps into an HDF5 file.
    It works independently in its own thread.
    """
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.cap = cv2.VideoCapture(0)  #pylint: disable=E1101
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  #pylint: disable=E1101
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  #pylint: disable=E1101

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        fps = 30.0
        width, height = (
            int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            )
        self.writer = cv2.VideoWriter(f"{filename}.mp4", fourcc, fps, (width, height))

    def run(self):
        """Main loop for saving frames."""
        timestamps = []
        while True:
            if QThread.currentThread().isInterruptionRequested():
                break

            ret, frame = self.cap.read()

            if not ret:
                break

            self.writer.write(frame)
            ts = time.time()
            timestamps.append(ts)

        self.cap.release()
        self.writer.release()

        # Save the timestamps to a file
        with open(f"{self.filename}.txt", "w") as f:
            for ts in timestamps:
                f.write(f"{ts}\n")
