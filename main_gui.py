# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 300)
        self.addImageBtn = QtWidgets.QPushButton(Dialog)
        self.addImageBtn.setGeometry(QtCore.QRect(10, 230, 130, 60))
        self.addImageBtn.setObjectName("addImageBtn")
        self.recogBtn = QtWidgets.QPushButton(Dialog)
        self.recogBtn.setGeometry(QtCore.QRect(160, 230, 130, 60))
        self.recogBtn.setObjectName("recogBtn")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 280, 210))
        self.label.setAutoFillBackground(True)
        self.label.setText("")
        self.label.setObjectName("label")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(300, 10, 171, 281))
        self.listView.setAutoFillBackground(True)
        self.listView.setObjectName("listView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.addImageBtn.setText(_translate("Dialog", "Thêm ảnh"))
        self.recogBtn.setText(_translate("Dialog", "Nhận diện"))

