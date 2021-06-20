# pip install pyqt5
# 구글에 qt designer download

from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
import urllib.request as req
from bs4 import BeautifulSoup
from PyQt5.QtGui import QPixmap      # 이미지를 뜰때 꼭 필요한 모쥴


ui_file = './movie_chart_test.ui'
class MainDaialog(QDialog):
    ''' MainDaialog 클래스는 gui 자체다'''
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(ui_file, self)                           # uic.loadUi 파일을 파이썬 코드에서 로드하기
        self.pushButton.clicked.connect(self.showMovieChart)        # button > QT 디자이네어서 만든이름 | self.button으로 가져옴
        # showString > 이거 함수인데 > connect안에서는 () 넣으면 안됨> 함수이름만 적기로되어있음
        # 함수앞에도 self를 넣네...


    def showMovieChart(self):
        code = req.urlopen("http://www.cgv.co.kr/movies/")
        soup = BeautifulSoup(code, "html.parser")
        # title = soup.select_one("strong.title") # 요소 하나만 가져옴!
        title = soup.select("div.sect-movie-chart strong.title")  # 요소 여러개 한번에!
        img = soup.select("span.thumb-image > img")
        for i in range(len(title)):
            imgUrl = img[i].attrs['src']
            data = req.urlopen(imgUrl).read()  # 바이너리로 된> 이미지 파일을 읽어온다
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            # 숫자로 형태로 된 이미지 데이터를 > 전달만 해주면 (loadFromData에 ) >
            #  PYQT5 gui창에 > 띄울수있는 형태로 만들어준다
            pixmap = pixmap.scaled(185, 260)    # 이미지 리사이징
            getattr(self, f'img{i+1}').setPixmap(pixmap)
            getattr(self, f'text{i+1}').setText(f'{i+1}위 : {title[i].text}')


QApplication.setStyle('fusion')     # 이것 저것 다해봤는데 > fusion스타일이 제일 낫대
app = QApplication(sys.argv)        # 프로그램을 실행할때 > 입력된 값을 읽어 들일수 있는 라이브러리
main_dialog = MainDaialog()         # 클래스를 담고
main_dialog.show()                  # .show() 보여줘라

sys.exit(app.exec_())               # 창을 닫았을때, 프로그램을 종료 시켜라.

