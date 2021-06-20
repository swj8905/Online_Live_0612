from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
import urllib.request as req
from bs4 import BeautifulSoup
from PyQt5.QtGui import QPixmap

ui_file = "./movie_chart.ui"
class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)
        self.button.clicked.connect(self.showMovieChart)

    def showMovieChart(self):
        code = req.urlopen("http://www.cgv.co.kr/movies/")
        soup = BeautifulSoup(code, "html.parser")
        img = soup.select("span.thumb-image > img")
        title = soup.select("div.sect-movie-chart strong.title")
        for i in range(len(title)):
            img_url = img[i].attrs["src"]
            data = req.urlopen(img_url).read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            pixmap = pixmap.scaled(185, 260)
            getattr(self, f"img{i+1}").setPixmap(pixmap)
            getattr(self, f"text{i+1}").setText(f"{i+1}위 : {title[i].text}")


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())