from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys
import stylesheet


class SlotDigit(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.position = 0
        self.target = 0
        self.step = 0
        self.image_width = 300
        self.gap = self.image_width * 54 / 30
        self.updater = QTimer()
        self.updater.connect(SIGNAL('timeout()'), self.nudge_step)
        self.updater.start(10)
        
        back_image = QPixmap("./slot_digitback.png").scaledToHeight(400)
        self.back = QGraphicsPixmapItem(back_image)
        self.back.setFlags(QGraphicsItem.ItemClipsChildrenToShape)
        self.addToGroup(self.back)
        
        numbers_image = QPixmap("./numbers.png").scaledToWidth(self.image_width)
        self.image = QGraphicsPixmapItem(numbers_image)
        self.image.setParentItem(self.back)
        self.image.setPos(-20, self.image_width / 10)
        
    def delta_change(self, delta_insert):
        self.target += delta_insert
        
    def nudge_step(self):
        delta_num = self.target - self.position
        if delta_num != 0:
            self.position += (delta_num / abs(delta_num))
            if self.position > 10:
                self.position -= 10
                self.target -= 10
            elif self.position < 0:
                self.position += 10
                self.target += 10
            self.image.setPos(self.image.x(), -self.position * self.gap + 30)
        
    def wheelEvent(self, event):
        self.target += int(event.delta() / abs(event.delta()))


def print_this(string):
    print(string)


class SlotMachine(QGraphicsView):
    shout = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(stylesheet.slate)
        self.setMaximumSize(1800, 900)
        self.items = []
        
        self.scene_1 = QGraphicsScene()
        self.scene_1.setSceneRect(QRectF(-40, -40, 1290, 500))
        for each in range(4):
            self.items.append(SlotDigit())
            self.scene_1.addItem(self.items[-1])
            self.items[-1].setPos(300*each, 0)
        self.setScene(self.scene_1)
        self.installEventFilter(self)
        self.shout.connect(print_this)
        
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            output = []
            for each in range(len(self.items)):
                number = self.items[each].position
                if number == 10:
                    number = 0
                output.append(number)
            integer = "".join([str(int(each)) for each in output])
            self.shout.emit(integer)
        return False


app = QApplication(sys.argv)
window = QMainWindow()

box = SlotMachine(window)
window.setCentralWidget(box)

window.show()
sys.exit(app.exec_())
