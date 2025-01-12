'''
secondary window
'''


from PyQt5 import QtCore, QtWidgets, QtGui




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


class SecondaryWindow(QtWidgets.QWidget):
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
