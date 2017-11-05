from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import threading

from urllib import request
import json
import time
import re
import ffmpeg

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 300)
        Dialog.setMinimumSize(QtCore.QSize(500, 300))
        Dialog.setMaximumSize(QtCore.QSize(500, 300))
        Dialog.setWindowTitle("")
        Dialog.setStyleSheet("QDialog {\n"
" background-color: rgb(255, 255, 255);\n"
"}")
        #Dialog.setSizeGripEnabled(False)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(190, 90, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 20, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(190, 150, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,   stop:0 rgba(60, 186, 162, 255), stop:1 rgba(98, 211, 162, 255))\n"
"}\n"
"QPushButton {\n"
"     background-color: #3cbaa2; border: 0px solid black;\n"
"     border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgb(170, 170, 127)\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(21, 234, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "想被哪个小宝宝甜呀~"))
        self.pushButton.setText(_translate("Dialog", "原谅她"))

class MainWindow(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.pushButton.clicked.connect(self.forgive)
        self.buttonState = False
        self.recording = False
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.operate)
        self.t = Job()
        self.recordingMonitor = QtCore.QTimer()
        self.recordingMonitor.timeout.connect(self.judge)

        self.api48 = 'https://plive.48.cn/livesystem/api/live/v1/memberLivePage'
        self.headers = {
            'os': 'android',
            'User-Agent': 'Mobile_Pocket',
            'IMEI': '864394020228161',
            'token': '0',
            'version': '5.0.1',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'plive.48.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

    def forgive(self):
        if self.buttonState is False:
            self.pushButton.setText("不再原谅")
            self.buttonState = True
            self.timer.start(5000)
        else:
            self.pushButton.setText("原谅她")
            self.buttonState = False
            self.timer.stop()

    def operate(self):
        name = self.plainTextEdit.toPlainText()
        self.record(name)
        if self.recording is True:
            self.timer.stop()
            self.recordingMonitor.start(1000)

    def judge(self):
        if self.t.finished is True:
            self.recordingMonitor.stop()
            self.timer.start(5000)

    @staticmethod
    def postform(url, form, headers):
        data = bytes(form, encoding='utf8')
        req = request.Request(url=url, data=data, headers=headers, method='POST')
        response = request.urlopen(req)
        return response.read().decode('utf-8')

    def record(self, name):
        last_stamp = int(time.time() * 1000)
        form = '{"lastTime":%s,"limit":20,"groupId":0,"memberId":0,"type":0,"giftUpdTime":1490857731000}' % \
               str(last_stamp)
        try:
            response_json = self.postform(self.api48, form, self.headers)
            response_dict = json.loads(response_json)
            self.label_2.setText(name + ' 没在直播 ' + time.strftime("%b%d - %H:%M:%S", time.localtime(last_stamp / 1000)))
        except:
            self.label_2.setText('网络出错 ' + time.strftime("%b%d - %H:%M:%S", time.localtime(last_stamp / 1000)))
            return 0
        try:
            live_list = response_dict['content']['liveList']
        except:
            return 0
        for live_item in live_list:
            title = live_item['title']
            check = re.match("(.)*{}(.)*".format(name), title)
            if check is not None:
                fname = '{}{}.mp4'.format(live_item['title'],
                                          time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000)))
                stream = ffmpeg.input(live_item["streamPath"])
                stream = ffmpeg.output(stream, fname)
                try:
                    self.t = Job(target=ffmpeg.run, args=(stream,))
                    self.t.setDaemon(True)
                    self.t.start()
                    self.label_2.setText('正在录制：' + fname)
                    self.recording = True
                except:
                    self.label_2.setText('录制出错')


class Job(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

        self.finished = False

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            try:
                if self._target:
                    self._target(*self._args, **self._kwargs)
                    self.finished = True
            finally:
                # Avoid a refcycle if the thread is running a function with
                # an argument that has a member that points to the thread.
                del self._target, self._args, self._kwargs
            time.sleep(1)

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False


def main():
    app = QtWidgets.QApplication(sys.argv)
    execution = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
