from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import sys
import stylesheet


class SlotDigit(QGraphicsItemGroup):
    carry_out = 0
    
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
            if abs(delta_num) < .2:
                self.position = round(self.position)
            else:
                self.position += (delta_num / abs(delta_num)) / 15
            self.image.setPos(self.image.x(), -self.position * self.gap + 30)
        if self.position >= 10:
            self.position -= 10
            self.target -= 10
            self.carry_out += 1
        elif self.position < 0:
            self.position += 10
            self.target += 10
            self.carry_out -= 1
        
    def wheelEvent(self, event):
        self.target += int(event.delta() / abs(event.delta()))


def print_this(string):
    print(string)


class SlotMachine(QGraphicsView):
    shout = Signal(str)
    carry = False
    items = []
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(stylesheet.slate)
        self.setMaximumSize(1800, 900)
        
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
            integer = "".join([str(int(each.position)) for each in self.items])
            self.shout.emit(integer)
        elif self.carry:
            self.check_carry()
        return False

    def check_carry(self):
        temp = [each.carry_out for each in self.items]
        for each in range(len(temp)):
            if each > 0 and self.items[each].carry_out != 0:
                temp = self.items[each-1].position + self.items[each].carry_out
                if temp > 0:
                    self.items[each-1].target = temp
                    self.items[each].carry_out = 0
                else:
                    self.items[each-1].carry_out += 1
                    self.items[each].carry_out = 0
                    
    def toggle_carry(self):
        if self.carry:
            self.carry = False
        else:
            self.carry = True
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    
    box = SlotMachine(window)
    window.setCentralWidget(box)
    
    window.show()
    sys.exit(app.exec_())

