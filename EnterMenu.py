import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QTableWidget, QWidget, QTableWidgetItem, QMainWindow, QLineEdit, \
    QPushButton, QFileDialog, QComboBox, QPlainTextEdit, QMessageBox, QLabel, QFrame,  QGridLayout, QButtonGroup, \
    QVBoxLayout, QScrollArea, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QFont
from PyQt5 import uic, sip
from PyQt5.QtCore import Qt
import sqlite3
from math import ceil

class EnterMenu(QMainWindow):

    def __init__(self):
        super().__init__()

        
