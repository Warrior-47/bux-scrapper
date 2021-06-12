from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressUI(object):
    def setupUi(self, ProgressUI):
        ProgressUI.setObjectName("ProgressUI")
        ProgressUI.setWindowIcon(QtGui.QIcon('icon/scraper.png'))
        ProgressUI.setEnabled(True)
        ProgressUI.resize(480, 640)
        ProgressUI.setMaximumSize(480, 640)
        ProgressUI.setMinimumSize(480, 640)
        ProgressUI.setStyleSheet("background-color:rgb(32,32,32);")
        self.centralwidget = QtWidgets.QWidget(ProgressUI)
        self.centralwidget.setObjectName("centralwidget")
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(10, 70, 461, 191))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.info_label.setFont(font)
        self.info_label.setAutoFillBackground(False)
        self.info_label.setStyleSheet("color: white;\n"
"background-color: rgb(40,40,40);\n"
"border-radius: 20px;\n"
"border: 2px solid white;")
        self.info_label.setText("")
        self.info_label.setTextFormat(QtCore.Qt.AutoText)
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setOpenExternalLinks(False)
        self.info_label.setObjectName("info_label")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 320, 441, 31))
        self.progressBar.setStyleSheet("QProgressBar {\n"
"    background-color:  rgb(84, 84, 84);\n"
"    color: rgb(255, 255, 255);\n"
"    border-radius: 10px;\n"
"    border: 2px solid white;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    border-radius: 10px;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.523, x2:1, y2:0.534091, stop:0 rgba(51, 51, 51, 255), stop:1 rgba(221, 24, 24, 255))\n"
"}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.scrap_button = QtWidgets.QToolButton(self.centralwidget)
        self.scrap_button.setEnabled(True)
        self.scrap_button.setGeometry(QtCore.QRect(120, 470, 221, 71))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setKerning(True)
        self.scrap_button.setFont(font)
        self.scrap_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.scrap_button.setAutoFillBackground(False)
        self.scrap_button.setStyleSheet("QToolButton {\n"
"    color: white;\n"
"    background-color:rgb(50,50,50);\n"
"    border-radius: 10px;\n"
"    border: 2px solid white;\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color:rgb(60,60,60);\n"
"    \n"
"}\n"
"\n"
"QToolButton:pressed {\n"
"    background-color:rgb(45,45,45);\n"
"    \n"
"}")
        self.scrap_button.setCheckable(False)
        self.scrap_button.setAutoRepeat(False)
        self.scrap_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.scrap_button.setAutoRaise(False)
        self.scrap_button.setArrowType(QtCore.Qt.NoArrow)
        self.scrap_button.setObjectName("scrap_button")
        self.scrap_button.hide()
        ProgressUI.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(ProgressUI)
        QtCore.QMetaObject.connectSlotsByName(ProgressUI)

    def retranslateUi(self, ProgressUI):
        _translate = QtCore.QCoreApplication.translate
        ProgressUI.setWindowTitle(_translate("ProgressUI", "buX Scrapper"))
        self.scrap_button.setText(_translate("ProgressUI", "Scrap Again"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProgressUI = QtWidgets.QMainWindow()
    ui = Ui_ProgressUI()
    ui.setupUi(ProgressUI)
    ProgressUI.show()
    sys.exit(app.exec_())
