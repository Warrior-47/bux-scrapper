from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressUI(object):
    def setupUi(self, ProgressUI):
        ProgressUI.setObjectName("ProgressUI")
        ProgressUI.setWindowIcon(QtGui.QIcon('icon/scraper.png'))
        ProgressUI.setEnabled(True)
        ProgressUI.resize(480, 640)
        ProgressUI.setStyleSheet("background-color:rgb(32,32,32);")
        self.centralwidget = QtWidgets.QWidget(ProgressUI)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.scrap_button = QtWidgets.QToolButton(self.centralwidget)
        self.scrap_button.setEnabled(True)
        self.scrap_button.setMinimumSize(QtCore.QSize(225, 50))
        self.scrap_button.setMaximumSize(QtCore.QSize(225, 72))
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
        self.gridLayout_2.addWidget(self.scrap_button, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(6, -1, 6, -1)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setMinimumSize(QtCore.QSize(350, 160))
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
        self.gridLayout.addWidget(self.info_label, 1, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
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
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout.addItem(spacerItem3, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem4, 3, 0, 1, 1)
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
