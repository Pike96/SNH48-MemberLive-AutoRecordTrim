from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import threading

from urllib import request
import json
import time
import re
import ffmpy

import wave
import numpy as np
import math
import struct


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 360)
        Dialog.setMinimumSize(QtCore.QSize(500, 360))
        Dialog.setMaximumSize(QtCore.QSize(500, 360))
        Dialog.setWindowTitle("")
        Dialog.setStyleSheet("QDialog {\n"
                             " background-color: rgb(255, 255, 255);\n"
                             "}")
        # Dialog.setSizeGripEnabled(False)
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
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setText("")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 290, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(190, 90, 111, 41))
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

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
        self.fname = ''
        self.lineEdit.returnPressed.connect(self.pushButton.click)

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
            #self.operate()
            self.timer.start(10000)
        else:
            self.pushButton.setText("原谅她")
            self.buttonState = False
            self.timer.stop()

    def operate(self):
        name = self.lineEdit.text()
        self.fname = self.record(name)
        if self.recording is True:
            self.timer.stop()
            self.recordingMonitor.start(3000)

    def judge(self):
        if self.t.finished is True:
            self.recordingMonitor.stop()
            self.timer.start(10000)
            self.t.finished = False
            t_trim = Job(target=self.trim, args=(self.fname,))
            t_trim.setDaemon(True)
            t_trim.start()

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
                fname = live_item['title'] + time.strftime("%b%d-%H-%M-%S", time.localtime(last_stamp / 1000))
                ff = ffmpy.FFmpeg(
                    inputs={live_item["streamPath"]: None},
                    outputs={fname + '.mp4': None}
                )
                try:
                    self.t = Job(target=ff.run)
                    self.t.setDaemon(True)
                    self.t.start()
                    self.label_2.setText('正在录制：' + fname + '.mp4 ...')
                    self.recording = True
                except:
                    self.label_2.setText('录制出错')
                return fname

    def trim(self, fname):
        self.label_3.setText('开始保留人声：' + self.fname + '.mp4 ...')

        du = 0.5
        th = 0.02
        inputFName = fname
        outputFName = inputFName + '[Trimmed].wav'

        # Convert
        ff2 = ffmpy.FFmpeg(
            inputs={inputFName + '.mp4': None},
            outputs={inputFName + '.wav': None}
        )
        try:
            ff2.run()
        except:
            self.label_3.setText('MP4转wav失败')

        # Read
        with wave.open(inputFName + '.wav') as fInput:
            params = fInput.getparams()
            nchannels, sampwidth, framerate, nframes, comptype, compname = params[:6]
            strData = fInput.readframes(nframes)
            waveData = np.fromstring(strData, dtype=np.int16)
            waveData = waveData * 1.0 / (max(abs(waveData)))
            waveData = np.reshape(waveData, [nframes, nchannels])

        # Trim
        self.label_3.setText('人声保留处理中 ...')
        outData = waveData
        lenWindow = int(du * framerate)
        numWindow = math.floor(nframes / lenWindow)
        count = 0
        end = nframes
        for i in range(0, numWindow + 1):
            tempCh1 = waveData[i * lenWindow:min(lenWindow * (i + 1) - 1, nframes), 0]
            max_value = max(tempCh1)
            if max_value > th:
                count += 1
                start = (count - 1) * lenWindow
                end = start + len(tempCh1)
                outData[start:end, 0] = tempCh1
                outData[start:end, 1] = waveData[i * lenWindow:min(lenWindow * (i + 1) - 1, nframes), 1]
        outData = np.resize(outData, (end, 2))

        # Save
        outData = np.reshape(outData, [end * nchannels, 1])
        with wave.open(outputFName, 'wb') as outwave:
            outwave.setparams((nchannels, sampwidth, framerate, end, comptype, compname))
            for v in outData:
                outwave.writeframes(struct.pack('h', int(v * 64000 / 2)))  # outData:16位，-32767~32767，注意不要溢出

        # Convert output to MP3
        ff2 = ffmpy.FFmpeg(
            inputs={outputFName: None},
            outputs={inputFName + '[Trimmed].mp3': None}
        )
        try:
            ff2.run()
        except:
            self.label_3.setText('WAV转MP3失败')

        self.label_3.setText('人声保留完毕')


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
