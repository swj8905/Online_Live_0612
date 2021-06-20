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

chrome_path = chromedriver_autoinstaller.install()

InstagramUI = "./instagram.ui"

class SeleniumWork(QObject):
    login_progress_signal = pyqtSignal(int)
    login_success_signal = pyqtSignal(bool)
    search_progress_signal = pyqtSignal(int)
    search_success_signal = pyqtSignal(bool)
    image_signal = pyqtSignal(str)
    content_signal = pyqtSignal(str)
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_path)
        QObject.__init__(self, None)
        self.input_id = ""
        self.input_pw = ""

    def login(self):
        self.login_progress_signal.emit(10)
        self.browser.get("https://www.instagram.com/accounts/login/?hl=ko")
        self.login_progress_signal.emit(20)
        time.sleep(3)
        self.login_progress_signal.emit(30)
        id = self.browser.find_element_by_name("username")
        id.send_keys(self.input_id)
        self.login_progress_signal.emit(50)
        pw = self.browser.find_element_by_name("password")
        pw.send_keys(self.input_pw)
        self.login_progress_signal.emit(70)
        self.browser.find_element_by_css_selector("div.Igw0E.IwRSH.eGOV_._4EzTm.bkEs3.CovQj.jKUp7.DhRcB").click()
        self.login_progress_signal.emit(90)
        time.sleep(4)
        self.login_progress_signal.emit(100)
        if self.browser.current_url == "https://www.instagram.com/accounts/login/?hl=ko":
            self.login_success_signal.emit(False)
        else:
            self.login_success_signal.emit(True)

    def search(self):
        self.search_progress_signal.emit(10)
        url = "https://www.instagram.com/explore/tags/{}/?hl=ko".format(self.keyword)
        self.search_progress_signal.emit(30)
        self.browser.get(url)
        self.search_progress_signal.emit(50)
        time.sleep(4)
        self.search_progress_signal.emit(70)
        # 첫번째 사진 클릭
        self.browser.find_element_by_css_selector("div._9AhH0").click()
        self.search_progress_signal.emit(90)
        time.sleep(5)
        self.search_progress_signal.emit(100)
        self.search_success_signal.emit(True)
        # 자동 좋아요 시작.
        row_num = 1
        while True:
            like = self.browser.find_element_by_css_selector("button.wpO6b span > svg._8-yf5")
            value = like.get_attribute("aria-label")
            next = self.browser.find_element_by_css_selector("a._65Bje.coreSpriteRightPaginationArrow")
            ### 크롤링 ###
            nick_name = self.browser.find_element_by_css_selector("a.sqdOP.yWX7d._8A5w5.ZIAjV")
            content = self.browser.find_element_by_css_selector("div.C4VMK > span")
            self.content_signal.emit(content.text)
            try:
                img = self.browser.find_element_by_css_selector("article.M9sTE.L_LMM.JyscU.ePUX4 div.KL4Bh > img")
                img_url = img.get_attribute("src")
            except:  # 게시물이 영상이라면?
                img = self.browser.find_element_by_css_selector("video.tWeCl")
                img_url = img.get_attribute("poster")

            self.image_signal.emit(img_url)
            row_num += 1

            if value == "좋아요":  # 좋아요가 안눌려있다면?
                like.click()
                time.sleep(random.randint(2, 5) + random.random())
                next.click()
                time.sleep(random.randint(2, 5) + random.random())
            elif value == "좋아요 취소":  # 좋아요가 눌려있다면?
                next.click()
                time.sleep(random.randint(2, 5) + random.random())


class MainDialog(QDialog):
    login_signal = pyqtSignal()
    search_signal = pyqtSignal()

    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(InstagramUI, self)
        self.login_progressbar.setValue(0)
        self.search_progressbar.setValue(0)
        self.search_button.setEnabled(False)
        ##### 쓰레드 할당 (추가 노동자 만들기)
        self.worker = SeleniumWork()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.start()
        ########################
        self.login_button.clicked.connect(self.LoginButtonClicked)
        self.search_button.clicked.connect(self.SearchButtonClicked)
        self.login_signal.connect(self.worker.login)
        self.worker.login_progress_signal.connect(self.login_progressbar.setValue)
        self.worker.login_success_signal.connect(self.finish_login)
        self.search_button.clicked.connect(self.SearchButtonClicked)
        self.search_signal.connect(self.worker.search)
        self.worker.search_progress_signal.connect(self.search_progressbar.setValue)
        self.worker.search_success_signal.connect(self.finish_search)
        self.worker.image_signal.connect(self.ShowImage)
        self.worker.content_signal.connect(self.ShowContent)

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
        self.search_signal.emit()


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
        self.worker.input_id = user_id
        self.worker.input_pw = user_pw
        self.login_signal.emit()



QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()

sys.exit(app.exec_())

