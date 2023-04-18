# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\kkr13\OneDrive\Desktop\final year project\face-recognition-based-attendance\FacesRecognition.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(394, 300)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(90, 111, 261, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ftpBtn = QtWidgets.QPushButton(self.frame)
        self.ftpBtn.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.ftpBtn.setFont(font)
        self.ftpBtn.setObjectName("ftpBtn")
        self.horizontalLayout.addWidget(self.ftpBtn)
        self.localBtn = QtWidgets.QPushButton(self.frame)
        self.localBtn.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.localBtn.setFont(font)
        self.localBtn.setObjectName("localBtn")
        self.horizontalLayout.addWidget(self.localBtn)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(70, 50, 281, 31))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.selectLabel = QtWidgets.QLabel(self.frame_2)
        self.selectLabel.setGeometry(QtCore.QRect(20, 10, 281, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.selectLabel.setFont(font)
        self.selectLabel.setObjectName("selectLabel")
        self.afterSelectFrame = QtWidgets.QFrame(Form)
        self.afterSelectFrame.setGeometry(QtCore.QRect(20, 190, 361, 41))
        self.afterSelectFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.afterSelectFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.afterSelectFrame.setObjectName("afterSelectFrame")
        self.label = QtWidgets.QLabel(self.afterSelectFrame)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.fileLocation = QtWidgets.QPlainTextEdit(self.afterSelectFrame)
        self.fileLocation.setGeometry(QtCore.QRect(110, 10, 251, 20))
        self.fileLocation.setObjectName("fileLocation")
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setGeometry(QtCore.QRect(50, 240, 321, 52))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.recognizeBtn = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.recognizeBtn.setFont(font)
        self.recognizeBtn.setObjectName("recognizeBtn")
        self.horizontalLayout_2.addWidget(self.recognizeBtn)
        self.spreadSheetBtn = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.spreadSheetBtn.setFont(font)
        self.spreadSheetBtn.setObjectName("spreadSheetBtn")
        self.horizontalLayout_2.addWidget(self.spreadSheetBtn)
        self.videoTypeWindow = QtWidgets.QListView(Form)
        self.videoTypeWindow.setGeometry(QtCore.QRect(90, 110, 251, 131))
        self.videoTypeWindow.setObjectName("videoTypeWindow")
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setGeometry(QtCore.QRect(100, 120, 171, 71))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.liveStreamBtn = QtWidgets.QRadioButton(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.liveStreamBtn.setFont(font)
        self.liveStreamBtn.setObjectName("liveStreamBtn")
        self.verticalLayout.addWidget(self.liveStreamBtn)
        self.capturedVideoBtn = QtWidgets.QRadioButton(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.capturedVideoBtn.setFont(font)
        self.capturedVideoBtn.setObjectName("capturedVideoBtn")
        self.verticalLayout.addWidget(self.capturedVideoBtn)
        self.frame_5 = QtWidgets.QFrame(Form)
        self.frame_5.setGeometry(QtCore.QRect(110, 200, 211, 31))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.okBtn = QtWidgets.QPushButton(self.frame_5)
        self.okBtn.setGeometry(QtCore.QRect(0, 0, 93, 28))
        self.okBtn.setObjectName("okBtn")
        self.cancelBtn = QtWidgets.QPushButton(self.frame_5)
        self.cancelBtn.setGeometry(QtCore.QRect(110, 0, 93, 28))
        self.cancelBtn.setObjectName("cancelBtn")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(90, 100, 241, 141))
        self.listWidget.setObjectName("listWidget")
        self.frame_6 = QtWidgets.QFrame(Form)
        self.frame_6.setGeometry(QtCore.QRect(110, 110, 211, 80))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.sheetNameLabel = QtWidgets.QLabel(self.frame_6)
        self.sheetNameLabel.setGeometry(QtCore.QRect(10, 10, 191, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.sheetNameLabel.setFont(font)
        self.sheetNameLabel.setObjectName("sheetNameLabel")
        self.sheetNameText = QtWidgets.QTextEdit(self.frame_6)
        self.sheetNameText.setGeometry(QtCore.QRect(0, 40, 201, 31))
        self.sheetNameText.setObjectName("sheetNameText")
        self.frame_7 = QtWidgets.QFrame(Form)
        self.frame_7.setGeometry(QtCore.QRect(110, 190, 217, 52))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.spreadOkBtn = QtWidgets.QPushButton(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.spreadOkBtn.setFont(font)
        self.spreadOkBtn.setObjectName("spreadOkBtn")
        self.horizontalLayout_3.addWidget(self.spreadOkBtn)
        self.spreadCancelBtn = QtWidgets.QPushButton(self.frame_7)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.spreadCancelBtn.setFont(font)
        self.spreadCancelBtn.setObjectName("spreadCancelBtn")
        self.horizontalLayout_3.addWidget(self.spreadCancelBtn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.ftpBtn.setText(_translate("Form", "FTP SERVER"))
        self.localBtn.setText(_translate("Form", "LOCAL FILES"))
        self.selectLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#1793c8;\">SELECT COMPILED FILE FROM</span></p></body></html>"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" color:#1a2cc8;\">SELECTED FILE:</span></p></body></html>"))
        self.recognizeBtn.setText(_translate("Form", "RECOGNIZE"))
        self.spreadSheetBtn.setText(_translate("Form", "UPDATE SHEET"))
        self.liveStreamBtn.setText(_translate("Form", "LIVE STREAM"))
        self.capturedVideoBtn.setText(_translate("Form", "CAPTURED VIDEO"))
        self.okBtn.setText(_translate("Form", "OK"))
        self.cancelBtn.setText(_translate("Form", "CANCEL"))
        self.sheetNameLabel.setText(_translate("Form", "ENTER THE SHEET FILENAME"))
        self.spreadOkBtn.setText(_translate("Form", "OK"))
        self.spreadCancelBtn.setText(_translate("Form", "CANCEL"))