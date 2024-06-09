import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTableWidget, QWidget, QTableWidgetItem, QMainWindow, QLineEdit, \
    QPushButton, QFileDialog, QComboBox, QPlainTextEdit, QMessageBox, QLabel, QFrame,  QGridLayout, QButtonGroup, \
    QVBoxLayout, QScrollArea, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QColor, QPixmap, QFont
from PyQt5 import uic, sip
from PyQt5.QtCore import Qt
import sqlite3
from math import ceil

class UserInterfaceClass(QMainWindow):

    #Use for transform to dictionary
    def touple_to_dict(self, touple, dict): 
        try:
            name, price, quantity, sale = touple[0], touple[1], touple[2], touple[3]
            dict[name] = [price, quantity, sale]
        except Exception:
            name, price, quantity = touple[0], touple[1], touple[2]
            dict[name] = [price, quantity]


    def __init__(self, parent):
        super().__init__()

        self.fileOpen_1 = "UserInterfaceList.ui"
        self.table_name = "test.db"
        self.bill_name = "Current_Bill.bd"
        self.is_sale_indicator = 0
        self.need_sale_indicator = 0
        self.indicator = None
        self.parent = parent

        self.back_background = QLabel(self)
        self.back_background.setGeometry(0, -85, 1300, 1100)
        self.SetImage(self.back_background, 'icons//background.jpg', 2000, 1150)
        self.back_background.setStyleSheet("background-image: url(icons//backgound.jpg);")

        x = 0

        self.title = QLabel("Key Food Marketplace", self)
        self.title.setGeometry(x, 0, 1500 - x, 70)
        self.title.setAlignment(Qt.AlignCenter)

        self.title.setAlignment(Qt.AlignCenter)
        font = QFont("times new roman", 30, QFont.Bold)
        self.title.setFont(font)

        self.setFixedSize(1300, 800)

        self.title.setStyleSheet("color: white; background-color: #0E294B;")

        self.image_label_cart = QLabel(self)
        self.image_label_cart.setGeometry(-30, -65, 200, 200)
        self.SetImage(self.image_label_cart, 'icons//cart.png', 150, 150)

        self.connection = sqlite3.connect(self.table_name)
        self.cur = self.connection.cursor()

        uic.loadUi(self.fileOpen_1, self)
        self.category_comboBox.addItem("Все")
        categories = sorted(self.cur.execute("""SELECT name FROM category"""))
        for i in categories:
            self.category_comboBox.addItem(i[0])

        self.LoadUI()

        self.bucket_pushButton.clicked.connect(self.clickedSelectBut)
        self.delete_pushButton.clicked.connect(self.clickedDeleteBut)
        self.filter_pushButton.clicked.connect(self.clickedFilterBut)
        self.product_buttons.buttonClicked.connect(self.clickedBut)
        self.sale_pushButton.clicked.connect(self.clickedSaleBut)
        

    def closeEvent(self, event) :
        sys.exit()


    def SetImage(self, label, path, width, height):
        pixmap = QPixmap(path)
        scaled_pixmap = pixmap.scaled(width, height, aspectRatioMode=Qt.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)
        label.setStyleSheet("background-color: transparent;")


    def LoadUI(self):

        #self.setFixedSize(1200, 800)
        category_text_from_box = self.category_comboBox.currentText()

        #Check sale conditin, so this condition filter products that have sale
        if category_text_from_box == "Все":
            sale_condition = "WHERE sale > 0" if self.is_sale_indicator == 1 else ""
        else:
            sale_condition = ("AND sale > 0") if self.is_sale_indicator == 1 else ""


        #Create dict for data from db and Supply paths for pictures
        #The product category is taken into account
        #The sale codition is taken into account
        if category_text_from_box == "Все":
            self.data_1 = self.cur.execute(f"""SELECT name, price, quantity, sale FROM test {sale_condition}""")
            self.data = dict()
            for row in self.data_1:
                self.touple_to_dict(row, self.data)

            self.data_names_bdinfo = self.cur.execute(f"""SELECT pictures FROM test {sale_condition}""")
        
        else:
            current_category_for_filter = self.cur.execute(f"""SELECT id FROM category 
                                                                    WHERE (name = '{category_text_from_box}')""")
            for i in current_category_for_filter:
                current_category_id_for_filter = i[0]

            self.data_1 = self.cur.execute(f"""SELECT name, price, quantity, sale FROM test
                                                WHERE (category = '{current_category_id_for_filter}') {sale_condition}""")
            self.data = dict()
            for row in self.data_1:
                self.touple_to_dict(row, self.data)

            self.data_names_bdinfo = self.cur.execute(f"""SELECT pictures FROM test
                                                            WHERE (category = '{current_category_id_for_filter}') {sale_condition}""")
            
        self.data_names = []
        i = 0
        for i, name in enumerate(self.data_names_bdinfo):
            current_name = name[0]
            self.data_names.append(f'ProductImages//{current_name}.jpg')
        
        self.table_headers = ["Name", "Price", "Amount", "Total Price"]

        #Layot for products
        self.layout_scroll = QGridLayout()
        self.product_buttons = QButtonGroup(self)

        positions = [(i,j) for i in range(int(ceil(len(self.data.keys())/5))) for j in range(5)]   
        array_of_ru_names = list(self.data.values())
        count = 0
        
        for position, name in zip(positions, self.data_names):
            
            verBox = QVBoxLayout()

            label1 = QLabel()
            label1.setFixedHeight(150)

            image = QPixmap(f"{name}")
            image = image.scaled(150, 150, Qt.KeepAspectRatio, Qt.FastTransformation)
            label1.setPixmap(image)
            verBox.addWidget(label1)

            image_data = list(self.data.keys())[count]

            self.button = QPushButton(image_data)
            self.button.setFont(QFont('times new roman', 15))
            self.button.setFlat(True)
            self.button.setFixedWidth(150)
            self.button.setStyleSheet("""
                           QPushButton {
                               color: black;
                           }
                           QPushButton:hover {
                               color: red;
                           }
                       """)

            self.product_buttons.addButton(self.button)
            self.product_buttons.setId(self.button, count)

            verBox.addWidget(self.button)

            price_label = QLabel()
            price_label.setText(f'{array_of_ru_names[count][0] - array_of_ru_names[count][0] * array_of_ru_names[count][2] / 100}')
            price_label.setFont(QFont("times new roman", 14))
            if array_of_ru_names[count][2]:
                price_label.setStyleSheet('color : green')
            price_label.setAlignment(Qt.AlignCenter)
            verBox.addWidget(price_label)

            self.layout_scroll.addLayout(verBox, *position)
            count += 1


        #Add layout on the scrollArea
        self.frame = QFrame()
        self.layout_scroll.setAlignment(Qt.AlignTop)
        self.frame.setLayout(self.layout_scroll)

        self.scrollArea.setWidget(self.frame)
        self.scrollArea.setWidgetResizable(False)
        
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(self.table_headers)
        self.table.resizeColumnsToContents()
        

    def FormTable(self):

        bill_connection = sqlite3.connect(self.bill_name)
        bill_cur = bill_connection.cursor()

        self.current_bill_data = bill_cur.execute(f"""SELECT Name, Price, Amount, Total_Price FROM Current_Bill""")

        self.table.clear()
        self.table.setRowCount(0)

        self.table.setColumnCount(len(self.table_headers))
        self.table.setHorizontalHeaderLabels(self.table_headers)

        total_sum = 0 

        for co, row in enumerate(self.current_bill_data):
            total_sum += row[3]
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(co, j, QTableWidgetItem(str(elem)))

        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.show()

        self.summary_label.setText(f"Итого: {total_sum}")


    def clickedBut(self, button_or):

        bill_connection = sqlite3.connect(self.bill_name)
        bill_cur = bill_connection.cursor()

        #If dont exist in the db: int
        #Else <sqlite3.cursor>
        local_id = button_or.text()
        current_amount = bill_cur.execute(f"""SELECT Amount FROM Current_Bill WHERE name = '{local_id}' """)
        for i in current_amount:
            current_amount = i[0]

        #Cheking class compliance
        if isinstance(current_amount, int):
            quantity = self.data[local_id][1]
            if current_amount + 1 <= quantity:
                bill_cur.execute(f"""UPDATE Current_Bill SET Amount = '{current_amount + 1}' WHERE name = '{local_id}'""")
                bill_connection.commit()
            
            else:
                mes = QMessageBox.information(self, "Предупреждение", "Достигнуто максимальное количесвто товара в корзине")

        else:
            bill_cur.execute(f"""INSERT INTO Current_Bill VALUES ('{local_id}', '{int(self.data[local_id][0]) -  int(self.data[local_id][0])* int(self.data[local_id][2]) / 100}', 
                             '{int(self.data[local_id][1])}', '{int(1)}') """)
            bill_connection.commit()

        #Form the bill
        self.FormTable()


    def clickedSelectBut(self):
        
        if self.indicator is None:
            self.indicator = BuketWindow(self)
            self.indicator.show()

        else:
            self.indicator = None
    

    def clickedFilterBut(self):

        self.deleteLayout(self.frame.layout())
        self.LoadUI()
        self.product_buttons.buttonClicked.connect(self.clickedBut)


    def deleteLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(layout)


    def clickedSaleBut(self):
        
        self.is_sale_indicator = 0 if self.is_sale_indicator else 1
        self.clickedFilterBut()


    def clickedDeleteBut(self):

        bill_connection = sqlite3.connect(self.bill_name)
        bill_cur = bill_connection.cursor()
        
        rows_fordel = []
        for x in self.table.selectedItems():
            rows_fordel.append(x.row())

        erase_rows = []
        for row in rows_fordel:
            name = self.table.item(row, 0).text()
            bill_cur.execute(f"""DELETE FROM Current_Bill WHERE (Name = '{name}')""")
            erase_rows.append(row)

        bill_connection.commit()
        self.FormTable()



class BuketWindow(QMainWindow):

    def __init__(self, parent : QWidget):
        super().__init__()
        self.parent = parent
        self.bucket_window_name = "BucketWindow.ui"

        self.bill_connection = sqlite3.connect(self.parent.bill_name)
        self.bill_cur = self.bill_connection.cursor()
        uic.loadUi(self.bucket_window_name, self)


        self.load_text()
        self.return_pushButton.clicked.connect(self.clickedReturnBut)
        self.buy_pushButton.clicked.connect(self.clickedBuyBut)


    def load_text(self):
        
        self.setFixedSize(450, 450)

        bill_connection = sqlite3.connect(self.parent.bill_name)
        bill_cur = bill_connection.cursor()

        current_data = self.bill_cur.execute(f"""SELECT Name, Price, Amount, Total_Price FROM Current_Bill""")
        bill_dict = dict()
        for row in current_data:
            self.parent.touple_to_dict(row, bill_dict)

        Sum = 0
        for i, key in enumerate(bill_dict.keys()):
            price_text = f'{str(bill_dict[key][0]):>5}'
            amount_text = f'{str(bill_dict[key][1]):>5}'
            good_bill_text = str(key) + ' ' + price_text + ' ' + amount_text
            Sum += (bill_dict[key][0] * bill_dict[key][1])

            s = f'Товар {i + 1}: {good_bill_text:>32}'
            self.bill_plainTextEdit.insertPlainText(s)
            self.bill_plainTextEdit.insertPlainText("\n")
        sum_string = str(Sum) + ' руб'
        self.bill_plainTextEdit.insertPlainText(50 * ".")
        self.bill_plainTextEdit.insertPlainText("\n")
        self.bill_plainTextEdit.insertPlainText(f'Итого: {sum_string:>32}')


    def clickedReturnBut(self):

        self.close()


    def clickedBuyBut(self):

        main_bd_con = sqlite3.connect(f"{self.parent.table_name}")
        main_bd_cursor = main_bd_con.cursor()

        end = end = QMessageBox.question(self, "Окно", "Покупка совершена. Хотите покинуть магазин?", QMessageBox.Yes | QMessageBox.No)
        data_for_delete = self.bill_cur.execute(f"""SELECT Name, Amount FROM Current_Bill""")

        if end == QMessageBox.Yes:
            
            for name, quantity in data_for_delete:
                print(name, quantity)
                main_bd_cursor.execute(f"""UPDATE test 
                                            SET quantity = quantity - '{quantity}'
                                            WHERE (name = '{name}')""")
            
            main_bd_con.commit()
            self.bill_cur.execute("""DELETE FROM Current_Bill""")
            self.bill_connection.commit()
            sys.exit(app.exec_())

        else:

            for name, quantity in data_for_delete:
                print(name, quantity)
                main_bd_cursor.execute(f"""UPDATE test 
                                            SET quantity = quantity - '{quantity}'
                                            WHERE (name = '{name}')""")
                
            self.bill_cur.execute("""DELETE FROM Current_Bill""")
            self.bill_connection.commit()
            self.close()



class MyWindow(QMainWindow):

    def closeEvent(self, event):
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UserInterfaceClass(None)
    ex.show()
    sys.exit(app.exec_())

'''
app = QApplication(sys.argv)
ex = UserInterfaceClass()
window = MyWindow()
window.setCentralWidget(ex)
window.show()
sys.exit(app.exec_())
'''