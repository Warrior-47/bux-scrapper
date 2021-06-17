from progress import Ui_ProgressUI
from bux_scrapper import Scrapper
from sign_in import Ui_SignInUI

from PyQt5 import QtCore, QtWidgets

from os import environ, path, mkdir
import sys


class ProgressWindow(QtWidgets.QMainWindow):
    def __init__(self, email, pass_, course_id):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_ProgressUI()
        self.ui.setupUi(self)
        self.ui.scrap_button.clicked.connect(self.go_back)
        self.show()

        self.scrapper = Scrapper(email, pass_, course_id)
        self.scrapper.start()

        self.scrapper.str_signal.connect(self.change_info)
        self.scrapper.int_progress_signal.connect(self.update_progress_bar)
        self.scrapper.int_progress_max_signal.connect(self.update_max_progress)
        self.scrapper.down_done_signal.connect(self.show_button)

    @QtCore.pyqtSlot(str)
    def change_info(self, message):
        self.ui.info_label.setText(message)

    @QtCore.pyqtSlot(int)
    def update_progress_bar(self, val):
        self.ui.progressBar.setProperty('value', val)

    @QtCore.pyqtSlot(int)
    def update_max_progress(self, val):
        self.ui.progressBar.setProperty('maximum', val)

    @QtCore.pyqtSlot()
    def show_button(self):
        self.ui.scrap_button.show()

    def go_back(self):
        self.sign_in = SignInWindow()
        self.close()


class SignInWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_SignInUI()
        self.ui.setupUi(self)
        self.ui.scrap_button.clicked.connect(self.scrap)
        self.show()

    def scrap(self):
        email = self.ui.email_input.text().strip()
        pass_ = self.ui.pass_input.text().strip()
        course_id = self.ui.id_input.text().strip().upper()

        self.progress = ProgressWindow(email, pass_, course_id)
        self.close()


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


if __name__ == '__main__':
    suppress_qt_warnings()

    if not path.exists('Output'):
        mkdir('Output')

    app = QtWidgets.QApplication(sys.argv)
    window = SignInWindow()
    sys.exit(app.exec_())
