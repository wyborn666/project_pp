import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QFont
from PyQt5 import uic
import sqlite3

class ProductClass(QMainWindow):
    def __init__(self, parent, db_filename):
        super().__init__()
        self.parent = parent
        uic.loadUi('products.ui', self)
        self.db_filename = db_filename
        self.LoadUI()

    def LoadUI(self):
        self.mas = ['айди', 'Название', 'Цена', 'Количество', 'Категория']
        self.goods = ['id', 'name', 'price', 'quantity', 'category']
        self.setWindowTitle("Products")

        self.setFixedSize(1200, 800)
        self.loadTable(self.db_filename)

        self.select_button.clicked.connect(self.filter_movies_by_genre)

    def filter_movies_by_genre(self):
        self.table.blockSignals(True)
        filter_value = self.combo_box_category.currentText()

        get_text_line_edit_price_from = self.line_edit_price_from.text()
        get_text_line_edit_price_to = self.line_edit_price_to.text()
        name_text = self.line_edit_name.text()
        quantity_text = self.line_edit_quantity.text()

        price_from = get_text_line_edit_price_from if get_text_line_edit_price_from else "0"
        price_to = get_text_line_edit_price_to if get_text_line_edit_price_to else "2000"
        quantity = quantity_text if quantity_text else "1"

        filter_condition = (f"price BETWEEN {price_from} AND {price_to} "
                            f"AND quantity >= {quantity} "
                            f"AND name LIKE '%{name_text}%'")

        if filter_value != 'Все':
            get_id = self.cursor.execute(f"SELECT id FROM category WHERE name = '{filter_value}'").fetchone()
            if get_id:
                filter_condition += f" AND category = {get_id[0]}"

        query = f"SELECT id, name, price, quantity, category FROM test WHERE {filter_condition}"
        print(f"Executing query: {query}")
        products = self.cursor.execute(query).fetchall()

        self.table.setRowCount(len(products))
        self.table.clearContents()

        for i, row in enumerate(products):
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                self.table.setItem(i, j, item)
        self.table.blockSignals(False)

    def loadTable(self, db_filename):
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.data = self.cursor.execute("SELECT id, name, price, quantity, category FROM test").fetchall()

        self.combo_box_category.addItem("Все")
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