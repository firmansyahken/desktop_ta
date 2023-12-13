from src.utils import handler
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, 
    QMainWindow, QPushButton, 
    QStackedLayout, QVBoxLayout, 
    QWidget, QTableWidget, 
    QTableWidgetItem, QFormLayout, 
    QLineEdit, QPlainTextEdit, QComboBox,
    QDateEdit, QSlider, QPushButton, 
    QDialog, QMessageBox, QComboBox)

def interface_daftar_buku(self):
    tab_buku = QWidget()
    buku_layout = QVBoxLayout()

    db = handler.DatabaseHandler()
    books = db.get_data("SELECT * FROM buku")
    table = QTableWidget()

    row_count = len(books)
    column_count = len(books[0]) if row_count > 0 else 0

    table.setRowCount(row_count)
    table.setColumnCount(column_count)

    if row_count > 0:
        header_labels = [str(item) for item in books[0].keys()]
        table.setHorizontalHeaderLabels(header_labels)

    for row, book in enumerate(books):
        for col, value in enumerate(book.values()):
            item = QTableWidgetItem(str(value))
            table.setItem(row, col, item)

    buku_layout.addWidget(table)
    tab_buku.setLayout(buku_layout)
    self.stacklayout.addWidget(tab_buku)

def interface_tambah_buku(self):
    tab_tambah_buku = QWidget()
    tambah_buku_layout = QVBoxLayout()
    # code
    self.stacklayout.addWidget(tab_tambah_buku)