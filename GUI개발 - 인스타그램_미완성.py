from PyQt5.QtWidgets import *
import sys
from PyQt5 import uic
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from selenium import webdriver
import time
import random
import urllib.request as req
from PyQt5.QtGui import QPixmap
import os
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

InstagramUI = "./instagram.ui"


class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(InstagramUI, self)
        self.login_progressbar.setValue(0)
        self.search_progressbar.setValue(0)
        self.search_button.setEnabled(False)

        self.login_button.clicked.connect(self.LoginButtonClicked)
        self.search_button.clicked.connect(self.SearchButtonClicked)

    def ShowImage(self, img_url):
        data = req.urlopen(img_url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(400, 400)  # 이미지 resizing
        self.img_label.setPixmap(pixmap)

    def ShowContent(self, content):
        self.content_label.clear()
        self.content_label.append(content)


    def finish_search(self, data):
        if data == True:
            self.search_status.setText("검색 완료! 자동 좋아요 누르는 중..")

    def SearchButtonClicked(self):
        self.search_status.setText("검색 중....")
        self.worker.keyword = self.input_search.text()

    def finish_login(self, data):
        if data == True:
            self.login_status.setText("로그인 성공!")
            self.search_button.setEnabled(True)
        else:
            self.login_status.setText("로그인 실패! 다시 입력해주세요..")
            self.login_button.setEnabled(True)

    def LoginButtonClicked(self):
        self.login_button.setEnabled(False)
        self.login_status.setText("로그인 중...")
        user_id = self.input_id.text()
        user_pw = self.input_pw.text()


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())

