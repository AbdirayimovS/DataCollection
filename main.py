'''
Scene to display a view and record webcamera and tobii tracker results.
'''
import sys
import argparse
import os

from PyQt5 import QtCore, QtWidgets, QtGui

from camera_thread import CameraRecorder
from tobii_thread import TobiiEyeTracker



class MainWindow(QtWidgets.QWidget):
    '''
    each circle must be looked for 3 seconds and total is 36 seconds.
    Program auto close after 36 seconds.
    I need to add timer
    '''
    def __init__(self, screen: QtWidgets.QWidget, filename):
        super().__init__()
        self.child_screen = screen
        self.recorder = CameraRecorder(filename+"/webcam")
        self.tobii_worker = TobiiEyeTracker(filename+"/tobii")
        self.running = False
        self._init_ui()

    def _init_ui(self):
        grid_layout = QtWidgets.QGridLayout()
        self.start_button = QtWidgets.QPushButton('START')
        self.start_button.clicked.connect(self._start)
        self.stop_button = QtWidgets.QPushButton('STOP')
        self.stop_button.clicked.connect(self._stop)
        grid_layout.addWidget(self.start_button, 0, 0)
        grid_layout.addWidget(self.stop_button, 0, 1)
        self.setLayout(grid_layout)

    def _start(self):
        '''start all processes.'''
        print('Starting...')
        self.running = True
        self.recorder.start()
        self.tobii_worker.start()
    
    def _stop(self):
        ''' stop all processes.'''
        self.running = False
        self.recorder.requestInterruption()
        self.tobii_worker.requestInterruption()
        self.recorder.wait()
        self.tobii_worker.wait()
        self.recorder = None
        self.tobii_worker = None

        print("Terminated all processes!")

    def closeEvent(self, event) -> None:
        if self.running:
            self._stop()
        self.child_screen.close()
        super().closeEvent(event)

    def show(self):
        self.child_screen.show()
        return super().show()


class CirclewithNumber(QtWidgets.QWidget):
    '''
    Circle with a number inside like a pool ball.
    '''
    def __init__(self, points):
        super().__init__()
        self.points = points
        self.update()

    def paintEvent(self, a0):
        qp = QtGui.QPainter(self)

        qp.setRenderHint(QtGui.QPainter.Antialiasing)  # FIXME: What is usage of this renderhit?
        qp.setBrush(QtGui.QBrush(QtGui.QColor(0, 128, 255)))

        # Circle grows back to original size during the end state
        diameter = 100  # px? FIXME: What is the unit of this variable
        font = QtGui.QFont('Arial', 24)
        qp.setFont(font)
        qp.setPen(QtGui.QPen(QtCore.Qt.black, 5))
        for number, (x_px, y_px) in enumerate(self.points, start=1):
            label = str(number)
            # Calculate circle position
            x = int(x_px - diameter / 2)
            y = int(y_px - diameter / 2)
            qp.drawEllipse(x, y, diameter, diameter)
            rect = QtCore.QRectF(x, y, diameter, diameter)

            qp.drawText(rect,QtCore.Qt.AlignCenter, label)

        return super().paintEvent(a0)




class ScenarioScreen(QtWidgets.QWidget):
    '''
    Scene which has 12 points (located evenly).

    '''
    def __init__(self, screen: QtGui.QScreen):
        super().__init__()
        self.screen_geometry = screen.geometry()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.WindowOverridesSystemGestures
            | QtCore.Qt.WindowType.MaximizeUsingFullscreenGeometryHint
            )  # https://doc.qt.io/qtforpython-5/overviews/qtwidgets-widgets-windowflags-example.html#window-flags-example
        self.setGeometry(self.screen_geometry)
        self._setup_ui()
    
    def _setup_ui(self):
        points = [
            (0.05, 0.1), # 1
            (0.05, 0.5), # 2
            (0.05, 0.9), # 3

            (0.33, 0.9), # 4
            (0.33, 0.5), # 5
            (0.33, 0.1), # 6

            (0.66, 0.1), # 7
            (0.66, 0.5), # 8
            (0.66, 0.9), # 9

            (0.95, 0.9), # 10
            (0.95, 0.5), # 11
            (0.95, 0.1), # 12

            ]
        points = [
            (
                int(x * self.screen_geometry.width()),
                int(y * self.screen_geometry.height())
            ) for (x, y) in points
            ]
        circle = CirclewithNumber(points)
        self.layout.addWidget(circle)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="Path to the file")

    args = parser.parse_args()

    os.path.dirname(args.filename)
    os.makedirs(args.filename)

    app = QtWidgets.QApplication(sys.argv)
    primary_screen = app.primaryScreen()
    screens = app.screens()
    if len(screens) < 2:
        raise RuntimeError("Program can not see second monitor! Please connect second monitor.")
    screens.remove(primary_screen)
    secondary_screen=screens[0]
    patient_window = ScenarioScreen(secondary_screen)
    experiment_dashboard = MainWindow(patient_window, args.filename)
    experiment_dashboard.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    print("Bismillahir-Rohmanir-Rohiim!")
    main()
