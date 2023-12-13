from PyQt6.QtWidgets import (
    QWidget, 
    QFormLayout, 
    QLineEdit,
    QPlainTextEdit, 
    QComboBox,
    QDateEdit, 
    QPushButton, 
    QMessageBox, 
    QComboBox)

def interface_daftar_anggota(self):
    rab_user = QWidget()
    user_layout = QFormLayout()
    self.stacklayout.addWidget(rab_user)

def interface_tambah_anggota(self):
    tab_tambah_anggota = QWidget()
    tambah_anggota_layout = QFormLayout()

    self.nama = QLineEdit()
    self.alamat = QPlainTextEdit()
    submit_button = QPushButton("Tambah")

    tambah_anggota_layout.addRow("Nama Lengkap: ", self.nama)
    tambah_anggota_layout.addRow("Alamat : ", self.alamat)
    tambah_anggota_layout.addRow(submit_button)

    submit_button.clicked.connect(self.insert_user)
    tab_tambah_anggota.setLayout(tambah_anggota_layout)
    self.stacklayout.addWidget(tab_tambah_anggota)

