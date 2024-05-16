import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTableWidget, QWidget, QTableWidgetItem, QMainWindow, QLineEdit, \
    QPushButton, QFileDialog, QComboBox, QPlainTextEdit, QMessageBox, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sqlite3





class ProductClass(QMainWindow):
    def __init__(self, parent, db_filename):
        super().__init__()
        self.parent = parent
        self.fileOpen = ""
        uic.loadUi('products.ui', self)
        self.db_filename = db_filename
        self.LoadUI()

    def LoadUI(self):
        self.mas = ['айди', 'Название', 'Цена', 'Количество', 'Категория']
        self.titles = ['id', 'name', 'category', 'price', 'quantity']
        self.setWindowTitle("Products")


        self.setFixedSize(1200, 800)
        self.loadTable(self.db_filename)

        self.select_button.clicked.connect(self.filter_movies_by_genre)

    def filter_movies_by_genre(self):
        self.table.blockSignals(True);
        filter_value = self.combo_box_category.currentText()

        get_text_line_edit_price_from = self.line_edit_price_from.text()
        get_text_line_edit_price_to = self.line_edit_price_to.text()
        name_text = self.line_edit_name.text()
        quantity_text = self.line_edit_quantity.text()

        filter_condition = (f"price BETWEEN {get_text_line_edit_price_from if get_text_line_edit_price_from else 0} "
                            f"AND {get_text_line_edit_price_to if get_text_line_edit_price_to else 2012} "
                            f"AND duration BETWEEN {get_text3 if get_text3 else 0} "
                            f"AND {get_text4 if get_text4 else 6900} "
                            f"AND title like '%{name_text}%'")


        if filter_value != 'Все':
            get_id = self.cursor.execute(f"SELECT id FROM genres WHERE title = '{filter_value}'").fetchone()[0]
            filter_condition += f" AND genre = {get_id}"

        films = self.cursor.execute(
            f"SELECT id, title, genre, year, duration FROM Films WHERE {filter_condition}").fetchall()

        self.table.setRowCount(len(films))
        self.table.clearContents()

        for i, row in enumerate(films):
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                self.table.setItem(i, j, item)
        self.table.blockSignals(False);








    def loadTable(self, db_filename):
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.data = self.cursor.execute("SELECT id, name, price, quantity, category FROM test").fetchall()

        self.combo_box_category.addItem("All")
        font = QFont("Times New Roman", 12)
        self.combo_box_category.setFont(font)
        category_list = self.cursor.execute('SELECT name FROM category').fetchall()


        for i in category_list:
            self.combo_box_category.addItem(i[0])

        if self.data:
            self.table.setRowCount(len(self.data))
            self.table.setColumnCount(len(self.data[0]))
            self.table.setHorizontalHeaderLabels(self.mas)
            for i, row in enumerate(self.data):
                for j, elem in enumerate(row):
                    item = QTableWidgetItem(str(elem))
                    self.table.setItem(i, j, item)

        self.table.show()




