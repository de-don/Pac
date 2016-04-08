import sys, random
from PyQt4 import QtGui, QtCore
from main import City


class Example(QtGui.QWidget):

    scale = 0
    max_vert_h = 1
    max_vert_w = 1
    city = None

    def __init__(self):
        super(Example, self).__init__()
        self.city = City()
        self.initUI()
        self.max_vert_h = self.city.max_heigth()
        self.max_vert_w = self.city.max_width()
        self.set_scale()
        print(self.scale)

    def initUI(self):
        self.showMaximized()
        self.setWindowTitle('PACK')
        self.show()

    def paintEvent(self, e):
        print(self.frameGeometry())
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
        self.set_scale()

        pen0 = QtGui.QPen()
        pen0.setWidth(7)
        pen0.setColor(QtCore.Qt.red)

        pen1 = QtGui.QPen()
        pen1.setWidth(2)
        pen1.setColor(QtCore.Qt.blue)
        qp.setPen(pen0)

        for k in self.city.Vertex:
            qp.drawPoint(self.city.Vertex[k][0] * self.scale, self.city.Vertex[k][1] * self.scale)
            qp.drawText(self.city.Vertex[k][0] * self.scale - 10, self.city.Vertex[k][1] * self.scale - 10, k)
        qp.setPen(pen1)
        for k, v in self.city.City.items():
            x1, y1 = self.city.Vertex[k]
            for k2, d in v.items():
                x2, y2 = self.city.Vertex[k2]
                qp.drawLine(x1 * self.scale, y1 * self.scale, x2 * self.scale, y2 * self.scale)
                qp.drawText((x1 + x2) * self.scale / 2 + 10, (y1 + y2) * self.scale / 2 + 10, str(d))

    def set_scale(self):
        ratio = self.frameGeometry().width() / self.frameGeometry().height()
        self.scale = int(0.8 * (self.frameGeometry().height()
                             if self.max_vert_h > self.max_vert_w and self.max_vert_w / self.max_vert_h < ratio
                             else
                             self.frameGeometry().width())
                           / max(self.max_vert_w, self.max_vert_h)
                      )


def main():
    app = QtGui.QApplication(sys.argv)
    _ = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
