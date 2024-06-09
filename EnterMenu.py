import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic
import sqlite3
from UserInterface import UserInterfaceClass
from MenuAdmin import MyWidget


class EnterMenu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.enter_interface_name = "EnterMenu Interface.ui"
        self.users_table_name = "Users_Admins.bd"
        self.indicator_reg = None
        self.conn = sqlite3.connect(self.users_table_name)
        self.curs = self.conn.cursor()

        uic.loadUi(self.enter_interface_name, self)

        self.registration_pushButton.clicked.connect(self.clickedRegistrationBut)
        self.enter_pushButton.clicked.connect(self.clickedEnterBut)
    

    def clickedEnterBut(self):

        current_login = self.login_lineEdit.text()
        current_password = self.password_lineEdit.text()

        if len(current_login) != 0 and len(current_password) != 0:
            
            try:
                password = list(*self.curs.execute(f"""SELECT password FROM 'Logins and passwords' 
                                                        WHERE (login = '{current_login}')"""))[0]
                author_status = list(*self.curs.execute(f"""SELECT status FROM 'Logins and passwords'
                                                        WHERE (login = '{current_login}')"""))[0]
            except Exception:
                password = None

            if current_password == password:
                try:
                    self.main_window = UserInterfaceClass(self) if author_status == 2 else MyWidget(self, 'test.db')
                    self.main_window.show()
                except Exception:
                    print("BAD TRY")

            else: 
                print("Bad PASS")

        else:
            print("BAD LEN")


    def clickedRegistrationBut(self):

        if self.indicator_reg is None:
            self.indicator_reg = RegistrationWindow(self)
            self.indicator_reg.show()

        else:
            self.indicator_reg = None


class RegistrationWindow(QMainWindow):

    def __init__(self, parent: QWidget):
        super().__init__()
        self.parent = parent

        uic.loadUi(self.parent.enter_interface_name, self)

    
class MyWindow(QMainWindow):

    def closeEvent(self, event):
        event.accept()


app = QApplication(sys.argv)
ex = EnterMenu()
window = MyWindow()
window.setCentralWidget(ex)
window.show()
sys.exit(app.exec_())