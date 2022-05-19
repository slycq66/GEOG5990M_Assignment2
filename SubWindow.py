# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\SubWindow.ui'
#
# Created by: PyQt5 UI code generator 

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    
    def setupUi(self, Dialog):
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(1400, 1050)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Dialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        Dialog.setSizeGripEnabled(False)
        
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 40, 160, 901))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        
        self.verticalLayout_legend = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_legend.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_legend.setObjectName("verticalLayout_legend")
        
        self.btn_start = QtWidgets.QPushButton(Dialog)
        self.btn_start.setGeometry(QtCore.QRect(190, 950, 311, 50))
        self.btn_start.setObjectName("btn_start")
        
        self.btn_draw = QtWidgets.QPushButton(Dialog)
        self.btn_draw.setGeometry(QtCore.QRect(510, 950, 311, 50))
        self.btn_draw.setObjectName("btn_draw")
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(190, 10, 891, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(180, 40, 1200, 900))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1198, 898))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Drunk Plan"))
        self.btn_start.setText(_translate("Dialog", "Start"))
        self.btn_draw.setText(_translate("Dialog", "Draw Density Map"))
        self.label.setText(_translate("Dialog", "Drunks passing by"))
        self.label_2.setText(_translate("Dialog", "Density Map"))
