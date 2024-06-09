import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QComboBox, QMessageBox
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
        self.mas = ['айди', 'Название', 'Цена', 'Количество', 'Категория', 'Картинка', 'Скидка']
        self.goods = ['id', 'name', 'price', 'quantity', 'category', 'pictures', 'sale']
        self.setWindowTitle("Products")

        self.setFixedSize(1200, 800)
        self.loadTable(self.db_filename)

        self.select_button.clicked.connect(self.filter_products_by_category)
        self.delete_button.clicked.connect(self.delete_products)
        self.add_button.clicked.connect(self.insert_products_by_first_class)
        self.save_button.clicked.connect(self.save_products)
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

        query = f"SELECT id, name, price, quantity, category, pictures, sale FROM test WHERE {filter_condition}"
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
            "Delete Confirmation",
            "Are you sure you want to delete the selected items?",
            QMessageBox.Yes | QMessageBox.No
        )

        if result == QMessageBox.Yes:
            selected_items = self.table.selectedItems()

            if not selected_items:
                QMessageBox.warning(self, "Warning", "No items selected for deletion.")
                return

            rows = set()
            for item in selected_items:
                rows.add(item.row())

            rows = sorted(rows, reverse=True)

            for row in rows:
                id = self.table.item(row, 0).text()
                self.cursor.execute("DELETE FROM test WHERE id = ?", (id,))
                self.table.removeRow(row)

            self.connection.commit()
            self.loadTable(self.db_filename)

    def save_products(self):
        self.connection.commit()

    def update_table(self, row, column):
        id = self.table.item(row, 0).text()
        text = self.table.item(row, column).text()

        # Check for text columns and wrap in quotes
        if self.goods[column] in ["name", "category", "pictures"]:
            text = f"'{text}'"

        try:
            self.cursor.execute(f"UPDATE test SET {self.goods[column]} = {text} WHERE id = {id}")
            self.connection.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def insert_products_by_first_class(self):
        self.insert_window = InsertWindow(self)
        self.insert_window.show()

    def loadTable(self, db_filename):
        self.connection = sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.data = self.cursor.execute("SELECT id, name, price, quantity, category, pictures, sale FROM test").fetchall()

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
        self.insert_button.clicked.connect(self.insert_products)

    def insert_products(self):
        get_text_name = self.name_plain_text_edit.toPlainText()
        get_text_price = self.price_plain_text_edit.toPlainText()
        get_text_quantity = self.quantity_plaint_text_edit.toPlainText()
        get_text_category = self.category_plain_text_edit.toPlainText()
        get_text_pictures = self.pictures_plain_text_edit.toPlainText()
        get_text_sales = self.sales_plain_text_edit.toPlainText()

        try:
            # Проверка, что все поля заполнены
            if not all([get_text_name, get_text_price, get_text_quantity, get_text_category, get_text_pictures,
                        get_text_sales]):
                raise ValueError("Все поля должны быть заполнены")

            # Проверка, что цена и количество являются числами
            if not get_text_price.isdigit() or not get_text_quantity.isdigit():
                raise ValueError("Цена и количество должны быть числом")

            # Проверка, что скидка - число в диапазоне от 0 до 100
            if not get_text_sales.isdigit() or not (0 <= int(get_text_sales) <= 100):
                raise ValueError("Скидка должна быть числом от 0 до 100")

            # Проверка наличия товара с такими же параметрами (без учета поля sale)
            query = ("SELECT id, quantity FROM test WHERE name = ? AND price = ? AND category = ? AND pictures = ?")
            self.parent.cursor.execute(query, (get_text_name, get_text_price, get_text_category, get_text_pictures))
            result = self.parent.cursor.fetchone()

            if result:
                # Товар уже существует, обновляем количество и скидку
                item_id, current_quantity = result
                new_quantity = int(current_quantity) + int(get_text_quantity)
                update_query = "UPDATE test SET quantity = ?, sale = ? WHERE id = ?"
                self.parent.cursor.execute(update_query, (new_quantity, get_text_sales, item_id))
            else:
                # Товара нет, вставляем новую строку
                insert_query = (
                    "INSERT INTO test(name, price, quantity, category, pictures, sale) VALUES (?, ?, ?, ?, ?, ?)")
                self.parent.cursor.execute(insert_query, (
                get_text_name, get_text_price, get_text_quantity, get_text_category, get_text_pictures, get_text_sales))

            self.parent.connection.commit()
            self.parent.loadTable(self.parent.db_filename)
            self.close()
        except ValueError as e:
            QMessageBox.critical(self, "Value Error", str(e))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductClass(None, 'test.db')
    ex.show()
    sys.exit(app.exec_())
