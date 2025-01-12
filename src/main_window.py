'''
Main window

'''
from PyQt5 import QtWidgets

from .core.camera_thread import CameraRecorder
from .core.tobii_thread import TobiiEyeTracker



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
