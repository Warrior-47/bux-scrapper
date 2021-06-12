from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SignInUI(object):
    def setupUi(self, SignInUI):
        SignInUI.setObjectName("SignInUI")
        SignInUI.setWindowIcon(QtGui.QIcon('icon/scraper.png'))
        SignInUI.setWindowModality(QtCore.Qt.NonModal)
        SignInUI.setEnabled(True)
        SignInUI.resize(480, 640)
        SignInUI.setMaximumSize(480, 640)
        SignInUI.setMinimumSize(480, 640)
        font = QtGui.QFont()
        font.setPointSize(10)
        SignInUI.setFont(font)
        SignInUI.setAutoFillBackground(False)
        SignInUI.setStyleSheet("background-color:rgb(32,32,32);")
        SignInUI.setInputMethodHints(QtCore.Qt.ImhNone)
        SignInUI.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        SignInUI.setAnimated(True)
        SignInUI.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(SignInUI)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.email_label = QtWidgets.QLabel(self.centralwidget)
        self.email_label.setGeometry(QtCore.QRect(180, 40, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.email_label.setFont(font)
        self.email_label.setAutoFillBackground(False)
        self.email_label.setStyleSheet("color: white;")
        self.email_label.setTextFormat(QtCore.Qt.AutoText)
        self.email_label.setOpenExternalLinks(False)
        self.email_label.setObjectName("email_label")
        self.pass_label = QtWidgets.QLabel(self.centralwidget)
        self.pass_label.setGeometry(QtCore.QRect(150, 170, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.pass_label.setFont(font)
        self.pass_label.setStyleSheet("color: white;")
        self.pass_label.setObjectName("pass_label")
        self.scrap_button = QtWidgets.QToolButton(self.centralwidget)
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
        self.email_input = QtWidgets.QLineEdit(self.centralwidget)
        self.email_input.setGeometry(QtCore.QRect(70, 100, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.email_input.setFont(font)
        self.email_input.setTabletTracking(False)
        self.email_input.setAutoFillBackground(False)
        self.email_input.setStyleSheet("background-color: white;\n"
"color: black;\n"
"padding:7px;")
        self.email_input.setText("")
        self.email_input.setPlaceholderText("")
        self.email_input.setObjectName("email_input")
        self.pass_input = QtWidgets.QLineEdit(self.centralwidget)
        self.pass_input.setEnabled(True)
        self.pass_input.setGeometry(QtCore.QRect(70, 230, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setUnderline(False)
        self.pass_input.setFont(font)
        self.pass_input.setAutoFillBackground(False)
        self.pass_input.setStyleSheet("background-color: white;\n"
"padding:7px;\n"
"color: black;")
        self.pass_input.setInputMethodHints(QtCore.Qt.ImhNone)
        self.pass_input.setText("")
        self.pass_input.setFrame(True)
        self.pass_input.setPlaceholderText("")
        self.pass_input.setObjectName("pass_input")
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.id_label = QtWidgets.QLabel(self.centralwidget)
        self.id_label.setGeometry(QtCore.QRect(120, 300, 301, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.id_label.setFont(font)
        self.id_label.setStyleSheet("color: white;")
        self.id_label.setObjectName("id_label")
        self.id_input = QtWidgets.QLineEdit(self.centralwidget)
        self.id_input.setEnabled(True)
        self.id_input.setGeometry(QtCore.QRect(70, 360, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setUnderline(False)
        self.id_input.setFont(font)
        self.id_input.setAutoFillBackground(False)
        self.id_input.setStyleSheet("background-color: white;\n"
"padding:7px;\n"
"color: black;")
        self.id_input.setInputMethodHints(QtCore.Qt.ImhNone)
        self.id_input.setText("")
        self.id_input.setFrame(True)
        self.id_input.setPlaceholderText("")
        self.id_input.setObjectName("id_input")
        SignInUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(SignInUI)
        QtCore.QMetaObject.connectSlotsByName(SignInUI)
        SignInUI.setTabOrder(self.email_input, self.pass_input)
        SignInUI.setTabOrder(self.pass_input, self.id_input)
        SignInUI.setTabOrder(self.id_input, self.scrap_button)

    def retranslateUi(self, SignInUI):
        _translate = QtCore.QCoreApplication.translate
        SignInUI.setWindowTitle(_translate("SignInUI", "buX Scrapper"))
        self.email_label.setText(_translate("SignInUI", "buX Email"))
        self.pass_label.setText(_translate("SignInUI", "buX Password"))
        self.scrap_button.setText(_translate("SignInUI", "Start Scrapping"))
        self.id_label.setText(_translate("SignInUI", "Course ID to Scrap"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SignInUI = QtWidgets.QMainWindow()
    ui = Ui_SignInUI()
    ui.setupUi(SignInUI)
    SignInUI.show()
    sys.exit(app.exec_())
