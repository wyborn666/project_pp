import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFrame, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5 import uic
from Products import ProductClass
import sqlite3


class MyWidget(QMainWindow):
    def __init__(self, db_filename):
        super().__init__()
        self.fileOpen = ""
        uic.loadUi('menu_admin.ui', self)
        self.db_filename = db_filename
        self.LoadUI()

    def LoadUI(self):
        self.mas = ['айди', 'Название', 'Цена', 'Количество', 'Категория', 'Картинка']
        self.goods = ['id', 'name', 'price', 'quantity', 'category', 'pictures']
        self.loadTable(self.db_filename)

        x = -300

        self.title = QLabel("Inventory Management System", self)
        self.title.setGeometry(x, 0, 1500 - x, 70)
        self.title.setAlignment(Qt.AlignCenter)
        font = QFont("times new roman", 30, QFont.Bold)
        self.title.setFont(font)

        self.setFixedSize(1500, 800)

        self.setStyleSheet("background-color: #ffffff;")
        self.title.setStyleSheet("color: white; background-color: #0E294B;")

        self.image_label_cart = QLabel(self)
        self.image_label_cart.setGeometry(-30, -65, 200, 200)
        self.SetImage(self.image_label_cart, 'icons//cart.png', 150, 150)

        self.image_label_emblem = QLabel(self)
        self.image_label_emblem.setGeometry(0, 50, 225, 200)
        self.SetImage(self.image_label_emblem, 'emblem_shop.png', 220, 300)

        Interface = QFrame(self)
        Interface.setFrameShape(QFrame.StyledPanel)
        Interface.setGeometry(0, 235, 225, 565)
        Interface.setStyleSheet("background-color: #293133; border-style: solid;")

        self.title_menu = QLabel("Menu", Interface)
        self.title_menu.setGeometry(0, 0, 225, 90)
        self.title_menu.setAlignment(Qt.AlignCenter)
        self.title_menu.setStyleSheet("background-color: #11e848")
        font = QFont("times new roman", 17, QFont.Bold)
        self.title_menu.setFont(font)

        self.products_button = QPushButton("Products", Interface)
        self.products_button.setGeometry(-2, 92, 225, 50)
        self.products_button.setStyleSheet("background-color: #DCDCDC")
        font = QFont("times new roman", 13, QFont.Bold)
        self.products_button.setFont(font)

        self.stocks_button = QPushButton("Stocks", Interface)
        self.stocks_button.setGeometry(-2, 144, 225, 50)
        self.stocks_button.setStyleSheet("background-color: #DCDCDC")
        font = QFont("times new roman", 13, QFont.Bold)
        self.stocks_button.setFont(font)

        self.exit_button = QPushButton("Exit", Interface)
        self.exit_button.setGeometry(-2, 513, 225, 50)
        self.exit_button.setStyleSheet("background-color: #DCDCDC")
        font = QFont("times new roman", 13, QFont.Bold)
        self.exit_button.setFont(font)

        self.products_button.clicked.connect(self.ProductsWindow)

    def SetImage(self, label, path, width, height):
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)
        label.setStyleSheet("background-color: transparent;")

    def loadTable(self, db_filename):
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.data = self.cursor.execute("SELECT id, name, price, quantity, category, pictures FROM test").fetchall()

        if self.data:
            self.table.setRowCount(len(self.data))
            self.table.setColumnCount(len(self.data[0]))
            self.table.setHorizontalHeaderLabels(self.mas)
            font = QFont("times new roman", 15)
            self.table.setFont(font)

            for i, row in enumerate(self.data):
                for j, elem in enumerate(row):
                    item = QTableWidgetItem(str(elem))
                    self.table.setItem(i, j, item)

            for col in range(len(self.data[0])):
                self.table.setColumnWidth(col, 255)

            row_height = 100
            self.table.verticalHeader().setDefaultSectionSize(row_height)

            header_font = QFont("times new roman", 14, QFont.Bold)
            self.table.horizontalHeader().setFont(header_font)

        self.table.show()

    def ProductsWindow(self):
        try:
            db_filename = 'test.db'
            self.products_window = ProductClass(self, db_filename)
            self.products_window.windowClosed.connect(self.on_products_window_closed)
            self.products_window.show()
        except Exception as e:
            print(f"Error opening products window: {e}")

    @pyqtSlot()
    def on_products_window_closed(self):
        self.loadTable(self.db_filename)


class MyWindow(QMainWindow):
    def closeEvent(self, event):
        event.accept()


app = QApplication(sys.argv)
ex = MyWidget('test.db')
window = MyWindow()
window.setCentralWidget(ex)
window.show()
sys.exit(app.exec_())
