import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTableWidget, QWidget, QTableWidgetItem, QMainWindow, QLineEdit, \
    QPushButton, QFileDialog, QComboBox, QPlainTextEdit, QMessageBox, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sqlite3
from Products import ProductClass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fileOpen = ""
        self.LoadUI()

    def LoadUI(self):
        x = -300

        self.title = QLabel("Inventory Management System", self)
        self.title.setGeometry(x, 0, 1200 - x, 70)
        self.title.setAlignment(Qt.AlignCenter)
        font = QFont("times new roman", 30, QFont.Bold)
        self.title.setFont(font)

        self.setFixedSize(1500, 800)

        self.setStyleSheet("background-color: #A5A5A5;")
        self.title.setStyleSheet("color: white; background-color: #000000;")

        self.image_label = QLabel(self)
        self.image_label.setGeometry(-20, -65, 200, 200)
        self.SetImage('icons//cart.png')

        self.login_button = QPushButton("Login", self)
        self.login_button.setGeometry(1000, 11, 200, 70)
        self.login_button.resize(150, 50)
        self.login_button.setStyleSheet("background-color: #7ef574;")
        font = QFont("times new roman", 13, QFont.Bold)
        self.login_button.setFont(font)

        Interface = QFrame(self)
        Interface.setFrameShape(QFrame.StyledPanel)
        Interface.setGeometry(0, 70, 200, 565)
        Interface.setStyleSheet("background-color: #293133; border-style: solid;")

        self.title_menu = QLabel("Menu", Interface)
        self.title_menu.setGeometry(0, 0, 200, 90)
        self.title_menu.setAlignment(Qt.AlignCenter)
        self.title_menu.setStyleSheet("background-color: #7ef574")
        font = QFont("times new roman", 17, QFont.Bold)
        self.title_menu.setFont(font)

        self.products_button = QPushButton("Products", Interface)
        self.products_button.setGeometry(-2, 92, 200, 50)
        self.products_button.setStyleSheet("background-color: #DCDCDC")
        font = QFont("times new roman", 13, QFont.Bold)
        self.products_button.setFont(font)

        self.stocks_button = QPushButton("Stocks", Interface)
        self.stocks_button.setGeometry(-2, 144, 200, 50)
        self.stocks_button.setStyleSheet("background-color: #DCDCDC")
        font = QFont("times new roman", 13, QFont.Bold)
        self.stocks_button.setFont(font)

        self.exit_button = QPushButton("Exit", Interface)
        self.exit_button.setGeometry(-2, 513, 200, 50)
        self.exit_button.setStyleSheet("background-color: #DCDCDC")
        font = QFont("times new roman", 13, QFont.Bold)
        self.exit_button.setFont(font)


        self.products_button.clicked.connect(self.ProductsWindow)




    def SetImage(self, path):
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(150, 150, aspectRatioMode=Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setStyleSheet("background-color: transparent;")

    def ProductsWindow(self):
        try:
            db_filename = 'test.db'
            self.products_window = ProductClass(self, db_filename)
            self.products_window.show()
        except Exception as E:
            print(E)




class MyWindow(QMainWindow):
    def closeEvent(self, event):
        event.accept()

app = QApplication(sys.argv)
ex = MyWidget()
window = MyWindow()
window.setCentralWidget(ex)

window.show()
sys.exit(app.exec_())
