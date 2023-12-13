from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtCore import QDate

from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, 
    QMainWindow, QPushButton, 
    QStackedLayout, QVBoxLayout, 
    QWidget, QTableWidget, 
    QTableWidgetItem, QFormLayout, 
    QLineEdit, QPlainTextEdit, QComboBox,
    QDateEdit, QSlider, QPushButton, 
    QDialog, QMessageBox, QComboBox)


def interface_daftar_pinjaman(self):
    tab_pinjaman = QWidget()
    pinjaman_layout = QFormLayout()
    self.stacklayout.addWidget(tab_pinjaman)

def interface_tambah_pinjaman(self):
    tab_tambah_pinjaman = QWidget()
    tambah_pinjaman_layout = QFormLayout()

    query_peminjam = QSqlQuery()
    query_peminjam.prepare("SELECT * FROM user")
    query_peminjam.exec()

    query_buku = QSqlQuery()
    query_buku.prepare("SELECT * FROM buku")
    query_buku.exec()
    
    # Form
    self.peminjam = QComboBox()
    while query_peminjam.next():
        id = str(query_peminjam.value(0))
        nama = query_peminjam.value(1)
        self.peminjam.addItem(nama,id)
    
    self.tanggal_pinjam = QDateEdit(QDate.currentDate())
    self.tanggal_kembali = QDateEdit(QDate.currentDate())

    self.buku = QComboBox()
    while query_buku.next():
        id = str(query_buku.value(0))
        nama = query_buku.value(1)
        self.buku.addItem(nama,id)

    submit_button = QPushButton('Simpan')
    submit_button.clicked.connect(self.insert_peminjaman)

    tambah_pinjaman_layout.addRow("Peminjam:" ,self.peminjam)
    tambah_pinjaman_layout.addRow("Tanggal Pinjam:" ,self.tanggal_pinjam)
    tambah_pinjaman_layout.addRow("Tanggal Kembali:" ,self.tanggal_kembali)
    tambah_pinjaman_layout.addRow("Buku :" ,self.buku)
    tambah_pinjaman_layout.addRow(submit_button)

    tab_tambah_pinjaman.setLayout(tambah_pinjaman_layout)
    self.stacklayout.addWidget(tab_tambah_pinjaman)