import sys, random
from PyQt4 import QtGui, QtCore
from main import City


class Example(QtGui.QWidget):
    repaint_flag = False
    scale_w = 0
    scale_h = 0
    max_vert_h = 1
    max_vert_w = 1
    lbl_teach = app = btn_go = btn_teach = lbl_iter = lbl_a = lbl_b = field_iter = field_a = field_b = city = None
    prev = None

    @QtCore.pyqtSlot()
    def updateSlot(self):
        print('work')
        self.repaint_flag = True  # not self.repaint_flag
        self.repaint()

    @QtCore.pyqtSlot()
    def teachSlot(self):
        self.teaching(self.field_iter.text())

    def __init__(self):
        super(Example, self).__init__()
        self.city = City()
        self.initUI()
        self.update()
        self.teaching(1000)
        self.max_vert_h = self.city.max_heigth()
        self.max_vert_w = self.city.max_width()
        self.set_scale()
        self.repaint()

    def initUI(self):
        self.setFixedSize(800, 600)
        w, h = self.frameGeometry().width(), self.frameGeometry().height()
        self.btn_teach = QtGui.QPushButton('Обучить', self)
        self.btn_go = QtGui.QPushButton('Найти путь', self)
        self.field_iter = QtGui.QLineEdit(self)
        self.connect(self.btn_teach, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('teachSlot()'))
        self.connect(self.btn_go, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('updateSlot()'))
        self.field_a = QtGui.QLineEdit(self)
        self.field_b = QtGui.QLineEdit(self)
        self.lbl_iter = QtGui.QLabel('Количество итераций\nдля обучения', self)
        self.lbl_a = QtGui.QLabel('Начало пути', self)
        self.lbl_b = QtGui.QLabel('Конец пути', self)
        self.lbl_teach = QtGui.QLabel('Идет обучение...', self)
        self.setWindowTitle('WayZ')
        self.field_iter.resize(70, 30)
        self.lbl_iter.resize(200, 60)
        self.field_iter.move(w * 0.8, h * 0.1)
        self.lbl_iter.move(w * 0.8, h * 0.02)
        self.field_a.move(w * 0.8, h * 0.3)
        self.lbl_a.move(w * 0.8, h * 0.27)
        self.field_b.move(w * 0.8, h * 0.4)
        self.lbl_b.move(w * 0.8, h * 0.37)
        self.btn_teach.move(w * 0.8, h * 0.17)
        self.btn_go.move(w * 0.8, h * 0.46)
        self.lbl_teach.move(w * 0.8, h * 0.7)
        self.show()
        self.setFocus()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)
        if self.repaint_flag:
            if self.field_a.text() in self.city.Names and self.field_b.text() in self.city.Names:
                self.drawPoints(qp, self.field_a.text(), self.field_b.text())
                self.prev = (self.field_a.text(), self.field_b.text())
            else:
                self.drawPoints(qp)
                self.repaint_flag = False
        else:
            if self.prev:
                self.drawPoints(qp, self.prev[0], self.prev[1])
            else:
                self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp, A=None, B=None):
        self.set_scale()
        pen0 = QtGui.QPen()
        pen0.setWidth(7)
        pen0.setColor(QtCore.Qt.red)

        pen3 = QtGui.QPen()
        pen3.setWidth(17)
        pen3.setColor(QtCore.Qt.green)

        pen1 = QtGui.QPen()
        pen1.setWidth(2)
        pen1.setColor(QtCore.Qt.blue)
        pen2 = QtGui.QPen()
        pen2.setWidth(2)
        pen2.setColor(QtCore.Qt.magenta)
        qp.setPen(pen0)

        for k in self.city.Vertex:
            if k == A or k == B:
                qp.setPen(pen3)
            else:
                qp.setPen(pen0)
            qp.drawPoint(self.city.Vertex[k][0] * self.scale_w, self.city.Vertex[k][1] * self.scale_h)
            qp.drawText(self.city.Vertex[k][0] * self.scale_w - 10, self.city.Vertex[k][1] * self.scale_h - 10, k)
        qp.setPen(pen1)
        way = []
        if A and B:
            way = self.city.GoTo(pFrom=A, pTo=B, Way=[])
        for k, v in self.city.City.items():
            x1, y1 = self.city.Vertex[k]
            for k2, d in v.items():
                x2, y2 = self.city.Vertex[k2]
                if k in way and k != way[-1] and way[way.index(k) + 1] == k2:
                    qp.setPen(pen2)
                elif k2 in way and k2 != way[-1] and way[way.index(k2) + 1] == k:
                    qp.setPen(pen2)
                else:
                    qp.setPen(pen1)
                qp.drawLine(x1 * self.scale_w, y1 * self.scale_h, x2 * self.scale_w, y2 * self.scale_h)
                qp.drawText((x1 + x2) * self.scale_w / 2 + 10, (y1 + y2) * self.scale_h / 2 + 10, str(d))

    def set_scale(self):
        self.scale_w = 0.75 * self.frameGeometry().width() / self.max_vert_w
        self.scale_h = 0.8 * self.frameGeometry().height() / self.max_vert_h

    def teaching(self, iter):
        try:
            iter = int(iter)
        except ValueError:
            iter = 0
        self.lbl_teach.setVisible(True)
        self.btn_teach.setEnabled(False)
        self.btn_go.setEnabled(False)
        self.repaint()
        max = len(self.city.Names) - 1
        r = random.randint(0, max)
        Now = self.city.Names[r]

        for i in range(iter):

            r = random.randint(0, max)
            To = self.city.Names[r]

            if (Now != To):
                W = self.city.GoTo(pFrom=Now, pTo=To, Way=[])
                print(Now, "=>", To, ':', W)
                self.city.UpdateWeight(W)
                Now = To

        self.btn_teach.setEnabled(True)
        self.btn_go.setEnabled(True)
        self.lbl_teach.setVisible(False)
        self.repaint()


app = QtGui.QApplication(sys.argv)
_ = Example()
sys.exit(app.exec_())
