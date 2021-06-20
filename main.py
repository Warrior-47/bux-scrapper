from progress import Ui_ProgressUI
from bux_scrapper import Scrapper
from sign_in import Ui_SignInUI

from PyQt5 import QtCore, QtWidgets

from os import environ, path, mkdir
import sys


class ProgressWindow(QtWidgets.QMainWindow):
    closing_signal = QtCore.pyqtSignal()

    def __init__(self, email, pass_, course_id):
        """The UI that shows the progress of scrapping

        Args:
            email (str): buX Email
            pass_ (str): buX Password
            course_id (str): Course ID user wants to scrap
        """
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_ProgressUI()
        self.ui.setupUi(self)
        self.__email = email
        self.ui.scrap_button.clicked.connect(self.go_back)
        self.show()

        # Creating the scrapper
        self.scrapper = Scrapper(email, pass_, course_id)

        self.scrapper.str_signal.connect(self.change_info)
        self.scrapper.int_progress_signal.connect(self.update_progress_bar)
        self.scrapper.int_progress_max_signal.connect(self.update_max_progress)
        self.scrapper.down_done_signal.connect(self.show_button)

        self.closing_signal.connect(self.scrapper.parent_closing)
        
        # Starting the scrapper on a different thread
        self.scrapper.start()

    def closeEvent(self, event):
        """Makes sure all working threads properly exit before
        stopping main thread
        """
        self.hide()

        # Checks if any worker threads are working
        if self.scrapper.pool.activeThreadCount() != 0:
            # If true, then notifies scrapper to stop all workers
            # and waits till all workers stop
            self.closing_signal.emit()
            self.scrapper.pool.waitForDone()

    @QtCore.pyqtSlot(str)
    def change_info(self, message):
        """Updates the GUI label with the message passed

        Args:
            message (str): The message that needs to shown on
            the GUI
        """
        self.ui.info_label.setText(message)

    @QtCore.pyqtSlot(int)
    def update_progress_bar(self, val):
        """Updates the GUI progress bar value

        Args:
            val (int): The value the progress bar needs to
            update to
        """
        self.ui.progressBar.setProperty('value', val)

    @QtCore.pyqtSlot(int)
    def update_max_progress(self, val):
        """Updates the maximum value of the GUI progress bar

        Args:
            val (int): Maximum progress bar value
        """
        self.ui.progressBar.setProperty('maximum', val)

    @QtCore.pyqtSlot()
    def show_button(self):
        """Shows the scrap again button
        """
        self.ui.scrap_button.show()

    def go_back(self):
        """Closes the current window and opens the Sign-In window
        """
        self.sign_in = SignInWindow(self.__email)
        self.close()


class SignInWindow(QtWidgets.QMainWindow):
    def __init__(self, email=None):
        """The Sign-In UI

        Args:
            email (str, optional): buX Email. Defaults to None.
        """
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_SignInUI()
        self.ui.setupUi(self)

        # Updates email input field if email was passed
        self.ui.email_input.setText(email if email else '')

        self.ui.scrap_button.clicked.connect(self.scrap)
        self.show()

    def scrap(self):
        """Takes all the input from the input fields and
        starts the scrapper
        """
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
