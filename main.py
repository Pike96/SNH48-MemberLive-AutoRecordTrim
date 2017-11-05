from PyQt5 import QtWidgets, QtCore
from ui_main import Ui_Dialog
import sys
import constants
import threading

from urllib import request
import json
import time
import re
import ffmpeg


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
            response_json = self.postform(constants.api48, form, constants.headers)
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
