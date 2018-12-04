import os
import sys
import threading
import time

import cv2
import numpy
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QListView, QAbstractItemView, QMessageBox as qm
from picamera import PiCamera
from picamera.array import PiRGBArray

from main_gui import Ui_Dialog

FACES_DIR = './faces/'

face_detector = cv2.CascadeClassifier("lbpcascade_frontalface_improved.xml")

faceCascade = cv2.CascadeClassifier("lbpcascade_frontalface_improved.xml")
cap = PiCamera()
cap.resolution = (640, 480)
cap.framerate = 20
rawCapture = PiRGBArray(cap, size=(640, 480))
time.sleep(1)
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21, GPIO.OUT)


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.addImageBtn.clicked.connect(self.addImg)
        self.ui.recogBtn.clicked.connect(self.recogImg)
        self.model = QStandardItemModel()
        self.ui.listView.setModel(self.model)
        self.ui.listView.setViewMode(QListView.IconMode)
        self.ui.listView.setIconSize(QSize(70, 70))
        self.ui.listView.doubleClicked.connect(self.delete_item)
        self.ui.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load_imgs()
        self.retrain()
        self.is_training = False
        self.frame = None
        self.face = None
        self.recog_count = 0
        self.last_open_relay = 0
        self.show()

    def load_imgs(self):
        if not os.path.isdir(FACES_DIR):
            os.mkdir(FACES_DIR)
        for img_name in os.listdir(FACES_DIR):
            item = QStandardItem(img_name)
            q_pixmap = QPixmap()
            q_pixmap.load(FACES_DIR + img_name)
            icon = QIcon(q_pixmap)
            item.setIcon(icon)
            self.model.appendRow(item)
        self.ui.listView.scrollToBottom()

    def delete_item(self, index):
        ret = qm.question(self, 'Confirm', "Are you sure to delete this?", qm.Yes | qm.No)
        if ret == qm.Yes:
            file_name = FACES_DIR + self.model.data(index)
            if os.path.isfile(file_name):
                os.unlink(file_name)
            self.model.removeRow(index.row())
            self.retrain()

    def addImg(self):
        if self.face is not None:
            img_name = str(time.time()) + '.png'
            cv2.imwrite(FACES_DIR + img_name, self.face)
            item = QStandardItem(img_name)
            q_pixmap = QPixmap()
            q_pixmap.load(FACES_DIR + img_name)
            icon = QIcon(q_pixmap)
            item.setIcon(icon)
            self.model.appendRow(item)
            self.ui.listView.scrollToBottom()

    def recogImg(self):
        self.recog_count = 5

    def in_frame(self, frame):
        self.frame = frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            x, y, w, h = faces[0]
            self.face = numpy.array(frame[y:y + h, x:x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if self.recog_count > 0 and not self.is_training:
                self.recog_count -= 1
                face = cv2.cvtColor(self.face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (64, 64))
                _, sure = self.face_recog.predict(face)
                print(sure)
                cv2.putText(frame, str(int(sure)), (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
                if sure < 900:
                    print('open relay')
                    GPIO.output(21, GPIO.HIGH)
                    self.last_open_relay = time.time()
                    self.recog_count = 0
        if self.last_open_relay is not -1:
            if time.time() - self.last_open_relay > 5:
                print('close relay')
                self.last_open_relay = -1
                GPIO.output(21, GPIO.LOW)

        self.set_image(frame)

    def set_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (280, 210))
        height, width, bpc = img.shape
        bpl = bpc * width
        image = QImage(img.data, width, height, bpl, QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        global is_running
        is_running = False

    def retrain(self):
        self.is_training = True
        self.face_recog = cv2.face.EigenFaceRecognizer_create(30)
        imgs = []
        ids = []
        for img_name in os.listdir(FACES_DIR):
            img = cv2.imread(FACES_DIR + img_name, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (64, 64))
            imgs.append(img)
            ids.append(1)
        self.face_recog.train(imgs, numpy.array(ids))
        self.is_training = False


class ReadImage(threading.Thread):
    def __init__(self):
        super().__init__()
        time.sleep(1)

    def run(self):
        global is_running
        for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame = frame.array
            window.in_frame(frame)
            rawCapture.truncate(0)
            cv2.waitKeyEx(0)
            if not is_running:
                break


app = QApplication(sys.argv)
window = AppWindow()
window.setWindowTitle("RPi face recognition")
is_running = True
ReadImage().start()
window.show()

sys.exit(app.exec_())
