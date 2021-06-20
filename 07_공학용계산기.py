from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
import math

ui_file = "./calculator.ui"
class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)
        self.equalbutton.clicked.connect(self.calculate)

    def calculate(self):
        foo = self.inputbox.text()
        result = eval(foo)
        result_for_history = f"{foo}\n= {result}\n"
        self.history.append(result_for_history)
        self.inputbox.clear()


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())