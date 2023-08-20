from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
import sys

user32 = ctypes.windll.user32
app_window_name = "Crosshair"

class Crosshair(QtWidgets.QWidget):
    def __init__(self, parent=None, windowSize=24, penWidth=2):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle(app_window_name)
        self.ws = windowSize
        self.resize(windowSize+1, windowSize+1)
        self.pen = QtGui.QPen(QtGui.QColor(255,255,0,255))                
        self.pen.setWidth(penWidth)                                            
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center() + QtCore.QPoint(1,1))

    def paintEvent(self, event):
        ws = self.ws
        # d = 3
        d = 6
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        # painter.drawLine(int(ws/2), 9, int(ws/2), int(ws/2 - ws/d))   # Top
        # painter.drawLine(   int(ws/2), int(ws/2 + ws/d),     int(ws/2), 15           )   # Bottom
        # painter.drawLine(   9, int(ws/2),               int(ws/2 - ws/d), int(ws/2)   )   # Left
        # painter.drawLine(   int(ws/2 + ws/d), int(ws/2),     15, int(ws/2)            )   # Right

        painter.drawLine(int(ws/2), 12, int(ws/2), int(ws/2 - ws/d))   # Top
        painter.drawLine(   int(ws/2), int(ws/2 + ws/d),     int(ws/2), 12           )   # Bottom
        painter.drawLine(   12, int(ws/2),               int(ws/2 - ws/d), int(ws/2)   )   # Left
        painter.drawLine(   int(ws/2 + ws/d), int(ws/2),     12, int(ws/2)            )   # Right

app = QtWidgets.QApplication(sys.argv)

widget = Crosshair(windowSize=24, penWidth=1)
widget.show()

sys.exit(app.exec_())

# pyinstaller -i icon.ico --noconsole --distpath ./ --workpath ./ -p ./ --clean -D -F -n crosshair crosshair.py