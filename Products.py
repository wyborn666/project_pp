import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QMainWindow, QTableWidgetItem, QComboBox, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
import sqlite3

class ProductClass(QMainWindow):
    windowClosed = pyqtSignal()

    def __init__(self, parent, db_filename):
        super().__init__()
        self.parent = parent
        uic.loadUi('products.ui', self)
        self.db_filename = db_filename
        self.LoadUI()

    def closeEvent(self, event):
        self.windowClosed.emit()
        super().closeEvent(event)

    def LoadUI(self):
        self.mas = ['айди', 'Название', 'Цена', 'Количество', 'Категория']
        self.goods = ['id', 'name', 'price', 'quantity', 'category']
        self.setWindowTitle("Products")

        self.setFixedSize(1200, 800)
        self.loadTable(self.db_filename)

        self.select_button.clicked.connect(self.filter_products_by_category)
        self.delete_button.clicked.connect(self.delete_products)
        self.add_button.clicked.connect(self.insert_movies_by_first_class)
        self.save_button.clicked.connect(self.save_movies)
        self.table.cellChanged.connect(self.update_table)

    def filter_products_by_category(self):
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
        print(f"Executing query: {query}")  # Отладочная информация
        products = self.cursor.execute(query).fetchall()

        self.table.setRowCount(len(products))
        self.table.clearContents()

        for i, row in enumerate(products):
            for j, elem in enumerate(row):
                item = QTableWidgetItem(str(elem))
                self.table.setItem(i, j, item)
        self.table.blockSignals(False)

    def delete_products(self):
        result = QMessageBox.question(
            self,
            "Delete it?",
            "Save changes?",
            QMessageBox.Yes | QMessageBox.No)

        if result == QMessageBox.Yes:
            selected_items = map(lambda x: x.row(), self.table.selectedItems())

            deleted_rows = []

            for row in selected_items:
                id = self.table.item(row, 0).text()

                self.cursor.execute(f"DELETE FROM test WHERE id = ?", (id,))

                deleted_rows.append(row)

            self.connection.commit()

            for row in sorted(deleted_rows, reverse=True):
                self.table.removeRow(row)

            self.loadTable(self.db_filename)

    def save_movies(self):
        self.connection.commit()

    def update_table(self, row, column):
        id = self.table.item(row, 0).text()
        text = self.table.item(row, column).text()

        if self.goods[column] == "name":
            text = f"'{text}'"
        self.cursor.execute(f"UPDATE test SET {self.goods[column]} = {text} WHERE id = {id}")


    def insert_movies_by_first_class(self):
        self.insert_window = InsertWindow(self)
        self.insert_window.show()


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


class InsertWindow(QMainWindow):
    def __init__(self, parent: ProductClass):
        super().__init__()
        self.parent = parent
        uic.loadUi('insert_rows.ui', self)
        self.insert_button.clicked.connect(self.insert_movies)

    def insert_movies(self):
        get_text_name = self.name_plain_text_edit.toPlainText()
        get_text_price = self.price_plain_text_edit.toPlainText()
        get_text_quantity = self.quantity_plaint_text_edit.toPlainText()
        get_text_category = self.category_plain_text_edit.toPlainText()

        self.parent.cursor.execute(
        f"INSERT INTO test(name, price, quantity, category) VALUES"
        f" ('{get_text_name}', {get_text_price}, {get_text_quantity}, {get_text_category})")
        self.parent.filter_products_by_category()
        self.parent.connection.commit()
        self.close()
