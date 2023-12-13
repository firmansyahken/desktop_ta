import sys
from src.utils import handler, validation
from src import user, buku, pinjaman
from src.components import tab
from PyQt6.QtCore import QDate
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, 
    QMainWindow, QStackedLayout, QVBoxLayout, 
    QWidget, QTableWidgetItem, QFormLayout, QPushButton, 
    QMessageBox)

def connectionDB():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("perpustakaan.db")

    if not db.open():
        return False
    return True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 500)
        self.setMaximumSize(800, 600)
        self.setWindowTitle("My App")
        self.connection = connectionDB()

        pagelayout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(self.button_layout)
        pagelayout.addLayout(self.stacklayout)

        tab.tab_menu(self)

        pinjaman.interface_daftar_pinjaman(self)
        buku.interface_daftar_buku(self)
        user.interface_daftar_anggota(self)
        buku.interface_tambah_buku(self)
        pinjaman.interface_tambah_pinjaman(self)
        user.interface_tambah_anggota(self)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
    
    def insert_peminjaman(self):
        user_id = self.peminjam.currentData()
        buku_id = self.buku.currentData()
        tgl_pinjam = self.tanggal_pinjam.date().toString("yyyy-MM-dd")
        tgl_kembali = self.tanggal_kembali.date().toString("yyyy-MM-dd")

        db = handler.DatabaseHandler()
        check = db.get_data("SELECT COUNT(user_id) FROM peminjaman WHERE user_id = :id", {"id": user_id})
        
        if check[0]['COUNT(user_id)'] > 0:
            peminjam = db.get_data("SELECT * FROM peminjaman WHERE user_id = :id", {"id": user_id})
            id_peminjam = peminjam[0]["id_pinjaman"]

            detail = {"id_peminjaman": id_peminjam, "id_buku": int(buku_id), "tgl_pinjam": tgl_pinjam, "tgl_kembali": tgl_kembali}
            peminjaman_detail = db.insert_data("peminjaman_detail",data=detail)

            db.update_data("peminjaman_detail", {"jumlah": peminjam[0]["jumlah"] + 1}, f"id_peminjam = {id_peminjam}")

        else:
            data_peminjaman = {"user_id": user_id, "jumlah": 1}
            peminjaman = db.insert_data("peminjaman", data=data_peminjaman)

            id_peminjam = db.get_data("SELECT id_pinjaman FROM peminjaman WHERE user_id = :id", {"id": user_id})
            id = id_peminjam[0]["id_pinjaman"]

            detail = {"id_peminjaman": id, "id_buku": int(buku_id), "tgl_pinjam": tgl_pinjam, "tgl_kembali": tgl_kembali}
            peminjaman_detail = db.insert_data("peminjaman_detail",data=detail)

    def insert_user(self):
        nama = self.nama.text()
        alamat = self.alamat.toPlainText()
        message_box = QMessageBox()
        db = handler.DatabaseHandler()
        validate = validation.Validation()

        # Validation
        if validate.required(nama):
            message_box.setText("Isi terlebih dahulu")
            return message_box.exec()
        elif not validate.char(nama):
            message_box.setText("Inputan harus berupa karakter")
            return message_box.exec()
        elif not validate.minmax(nama, 4, 50):
            message_box.setText("Inputan minimal 4 dan maximal 50 karakter")
            return message_box.exec()
        
        if validate.required(alamat):
            message_box.setText("Isi terlebih dahulu")
            return message_box.exec()
        elif not validate.minmax(nama, 4, 50):
            message_box.setText("Inputan minimal 4 dan maximal 50 karakter")
            return message_box.exec()
        
        data = {"nama": nama, "alamat": alamat}
        result = db.insert_data("user", data)

        if result:
            self.nama.clear()
            self.alamat.clear()
            message_box.setText("Data berhasil ditambahkan")
        else:
            message_box.setText("Data gagal ditambahkan")
        message_box.exec()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
