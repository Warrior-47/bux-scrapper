from bux_scrapper import Scrapper, CourseNotFoundException, InvalidEmailPasswordException

from PyQt5 import QtCore, QtGui, QtWidgets

from progress import Ui_ProgressUI
from sign_in import Ui_SignInUI

import sys


class ProgressWindow(QtWidgets.QMainWindow):
    def __init__(self, email, pass_, course_id):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_ProgressUI()
        self.ui.setupUi(self)
        self.show()

        self.scrapper = Scrapper(email, pass_, course_id)
        self.scrapper.start()

        self.scrapper.str_signal.connect(self.change_info)
        self.scrapper.int_val_signal.connect(self.update_progress_bar)
        self.scrapper.int_valmax_signal.connect(self.update_max_progress)

    
    def start_work(self, email, pass_, course_id):
        scrapper = Scrapper(self.event_manager)
        scrapper.start_scrapping(email, pass_, course_id)
    
    def change_info(self, message):
        self.ui.info_label.setText(message)
    
    def update_progress_bar(self, val):
        self.ui.progressBar.setProperty('value', val)
    
    def update_max_progress(self, val):
        self.ui.progressBar.setProperty('maximum', val)


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
        course_id = self.ui.id_input.text().strip()

        self.progress = ProgressWindow(email, pass_, course_id)
        self.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = SignInWindow()
    sys.exit(app.exec_())