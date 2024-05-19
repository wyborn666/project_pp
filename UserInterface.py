import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTableWidget, QWidget, QTableWidgetItem, QMainWindow, QLineEdit, \
    QPushButton, QFileDialog, QComboBox, QPlainTextEdit, QMessageBox, QLabel, QFrame,  QGridLayout, QButtonGroup, \
    QVBoxLayout, QScrollArea, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sqlite3
from math import ceil

class UserInterface(QMainWindow):

    #Use for transform to dictionary
    def touple_to_dict(self, touple, dict): 
        name, price, quantity = touple[0], touple[1], touple[2]
        dict[name] = [price, quantity]


    def __init__(self):
        super().__init__()

        self.fileOpen_1 = "UserInterfaceList.ui"
        self.table_name = "test.db"
        self.bill_name = "Current_Bill.bd"
        self.indicator = None

        self.connection = sqlite3.connect(self.table_name)
        self.cur = self.connection.cursor()

        uic.loadUi(self.fileOpen_1,self)
        self.LoadUI()

        self.bucket_pushButton.clicked.connect(self.clickedSelectBut)
        self.delete_pushButton.clicked.connect(self.clickedDeleteBut)
        self.product_buttons.buttonClicked['QAbstractButton *'].connect(self.clickedBut)


    def LoadUI(self):

        #$self.setFixedSize(1200, 800)

        #Create dict for data from db and Supply paths for pictures
        self.data_1 = self.cur.execute("""SELECT name, price, quantity FROM test""")
        self.data = dict()
        for row in self.data_1:
            self.touple_to_dict(row, self.data)

        self.data_names = ["ProductImages//Banana.jpg", "ProductImages//Soup.jpg", 
                           "ProductImages//Apple.jpg", "ProductImages//Garnet.jpg", "ProductImages//Broom.jpg"]
        
        self.table_headers = ["Name", "Price", "Amount", "Total Price"]

        #Layot for products
        self.layout_scroll = QGridLayout()
        self.product_buttons = QButtonGroup(self)

        positions = [(i,j) for i in range(int(ceil(len(self.data.keys())/5))) for j in range(5)]   
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
            self.button.setFlat(True)
            self.button.setFixedWidth(150)

            self.product_buttons.addButton(self.button)
            self.product_buttons.setId(self.button, count)

            verBox.addWidget(self.button)
            self.layout_scroll.addLayout(verBox, *position)
            count += 1

        #Add layout on the scrollArea
        frame = QFrame()
        frame.setLayout(self.layout_scroll)

        self.scrollArea.setWidget(frame)
        self.scrollArea.setWidgetResizable(False)

        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(self.table_headers)

        self.summary_label.setText(self.summary_label.text() + ":  0")


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

        self.summary_label.setText(f"Итого:   {total_sum}")


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
            bill_cur.execute(f"""UPDATE Current_Bill SET Amount = '{current_amount + 1}' WHERE name = '{local_id}'""")
            bill_connection.commit()

        else:
            bill_cur.execute(f"""INSERT INTO Current_Bill VALUES ('{local_id}', '{int(self.data[local_id][0])}', 
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
        pass


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
        uic.loadUi(self.bucket_window_name, self)

        self.load_text()

    def load_text(self):
        
        self.setFixedSize(600, 500)
        bill_connection = sqlite3.connect(self.parent.bill_name)
        bill_cur = bill_connection.cursor()

        ###  Refine
        current_data = bill_cur.execute(f"""SELECT Name, Price, Amount, Total_Price FROM Current_Bill""")
        for i in current_data:
            self.bill_plainTextEdit.insertPlainText(f"{i[0]}")
            self.bill_plainTextEdit.insertPlainText('  ' * (11- len(str(i[0]))) + f"{i[1]}")
            self.bill_plainTextEdit.insertPlainText('  ' * (11- len(str(i[1]))) + f"{i[2]}")
            self.bill_plainTextEdit.insertPlainText('  ' * (11- len(str(i[2]))) + f"{i[3]}")
            self.bill_plainTextEdit.insertPlainText("\n")


    def But(self):
        pass



class MyWindow(QMainWindow):

    def closeEvent(self, event):
        event.accept()



app = QApplication(sys.argv)
ex = UserInterface()
window = MyWindow()
window.setCentralWidget(ex)
window.show()
sys.exit(app.exec_())