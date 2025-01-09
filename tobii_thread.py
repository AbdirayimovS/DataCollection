'''

'''
import os
from typing import Dict
import time

from PyQt5 import QtCore

try:
    import tobii_research as tr
    from tobii_research_addons import ScreenBasedCalibrationValidation, Point2
except ImportError:
    import sys
    from unittest.mock import MagicMock
    tobii_mock = MagicMock()
    tobii_mock.find_all_eyetrackers.return_value = []
    sys.modules['tobii_research'] = tobii_mock
    sys.modules['tobii_research_addons'] = MagicMock()
    print("Issue With Importing Tobii Libraries!")
finally:
    import tobii_research as tr
    from tobii_research_addons import ScreenBasedCalibrationValidation, Point2




class TobiiEyeTracker(QtCore.QThread):

    def __init__(self, file_path: str):
        super().__init__()
        self.filename = file_path
        self.running = False
        self.is_subscribed = False
        self.data_buffer = []

        self.eye_tracker = self.__find_eye_tracker()

    def __find_eye_tracker(self):
        """
        Find and return the first available eye tracker.
        It can raise RuntimeError!
        """
        eye_trackers = tr.find_all_eyetrackers()

        if len(eye_trackers) == 0:
            raise RuntimeError("No Tobii eye tracker is found!")

        return eye_trackers[0]


    def run(self):
        """Main thread loop."""
        self.eye_tracker.subscribe_to(
                tr.EYETRACKER_GAZE_DATA, self.on_gaze_data, as_dictionary=True
            )
        # https://developer.tobiipro.com/python/python-sdk-reference-guide.html
        while True:
            if QtCore.QThread.currentThread().isInterruptionRequested():
                break


        self.eye_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.on_gaze_data)
        print("Tobii successfully unsubscribed!")

    def on_gaze_data(self, gaze: Dict):
        """Callback for receiving real-time gaze data."""
        gaze['timestamp'] = time.monotonic()

        self.data_buffer.append(gaze)
        if len(self.data_buffer) >= 100:
            self.save_data()
            self.data_buffer = []

    def save_data(self):
        """Save accumulated gaze data to a file."""
        try:
            import pandas as pd

            df = pd.DataFrame(self.data_buffer)
            mode = "a" if os.path.exists(self.filename) else "w"
            df.to_csv(self.filename, mode=mode, header=mode == "w", index=False)
        except Exception as e:
            self.error_occurred.emit(f"Error saving data: {e}")
