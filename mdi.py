import sys, re, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTabWidget, QWidget, QTableWidget, QTableWidgetItem, QTableView, QLineEdit, QFormLayout, QComboBox, QDateEdit, QListView, QCheckBox
from PyQt6.QtGui import QAction, QStandardItem, QStandardItemModel
from src.utils import handler
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtSql import QSqlQuery

def connectionDB():
    db_name = "perpustakaan.db"
    db = QSqlDatabase.addDatabase("QSQLITE")
    dir = os.getcwd()
    ls = os.listdir(dir)
    if not db_name in ls:
        db.setDatabaseName(db_name)
        db.open()
        query = QSqlQuery()
        # Create Table
        query.exec("CREATE TABLE buku (id_buku INTEGER PRIMARY KEY AUTOINCREMENT, nama_buku TEXT, stok INTEGER, tahun_terbit INTEGER)")
        query.exec("CREATE TABLE anggota (id_anggota INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, alamat TEXT)")
        query.exec("CREATE TABLE peminjaman (id_pinjaman INTEGER PRIMARY KEY AUTOINCREMENT, anggota_id INTEGER, jumlah INTEGER)")
        query.exec("CREATE TABLE peminjaman_detail (id_peminjaman_detail INTEGER PRIMARY KEY AUTOINCREMENT, pinjaman_id INTEGER, buku_id INTEGER, tgl_pinjam DATE, tgl_kembali DATE)")
        # Insert Data
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('Ayat-Ayat Cinta', 120, 2004);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('Bumi Manusia', 80, 1980);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('Dilan 1990', 150, 2014);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('Perahu Kertas', 90, 2009);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('Negeri 5 Menara', 110, 2009);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('AADC: Refrain', 70, 2014);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('Hujan', 130, 2011);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('5 CM', 95, 2005);");
        query.exec("INSERT INTO buku (nama_buku, stok, tahun_terbit) VALUES ('Rindu', 85, 2017);");

        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('John Doe', 'Jl. Merdeka No. 123');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Jane Smith', 'Jl. Jenderal Sudirman No. 456');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Ahmad Abdullah', 'Jl. Cipto Mangunkusumo No. 789');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Siti Aisyah', 'Jl. Pahlawan No. 101');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Ravi Patel', 'Jl. Diponegoro No. 222');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Elena Rodriguez', 'Jl. Gajah Mada No. 333');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Chen Wei', 'Jl. Asia Baru No. 505');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Maria Silva', 'Jl. Kusuma Bangsa No. 707');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Kenji Tanaka', 'Jl. Sakura No. 888');");
        query.exec("INSERT INTO anggota (nama, alamat) VALUES ('Anisa Setiawan', 'Jl. Purnama No. 999');");


        db.commit()
    else:
        db.setDatabaseName(db_name)
        db.open()

class DatabaseHandler:
    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        values = ', '.join([f":{key}" for key in data.keys()])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        return self.execute_query(insert_query, data)

    def update_data(self, table_name, data, condition):
        set_clause = ', '.join([f"{key} = :{key}" for key in data.keys()])
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        return self.execute_query(update_query, data)

    def delete_data(self, table_name, condition):
        delete_query = f"DELETE FROM {table_name} WHERE {condition}"
        return self.execute_query(delete_query)

    def get_data(self, query, bind_values=None):
        result = []
        query_obj = QSqlQuery()
        query_obj.prepare(query)

        if bind_values:
            for key, value in bind_values.items():
                query_obj.bindValue(f":{key}", value)

        if query_obj.exec():
            while query_obj.next():
                row = {}
                for i in range(query_obj.record().count()):
                    row[query_obj.record().fieldName(i)] = query_obj.value(i)
                result.append(row)
        else:
            print("Error:", query_obj.lastError().text())

        return result

    def execute_query(self, query, bind_values=None):
        query_obj = QSqlQuery()
        query_obj.prepare(query)

        if bind_values:
            for key, value in bind_values.items():
                query_obj.bindValue(f":{key}", value)

        return query_obj.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        self.connection = connectionDB()

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tab_widget)

        self.create_navigation_tabs()

        self.setWindowTitle("Perpustakaan")
        self.setGeometry(100, 100, 980, 720)

    def create_navigation_tabs(self):
        self.add_tab("Buku", self.tab_buku)
        self.add_tab("Anggota", self.tab_anggota)
        self.add_tab("Pinjaman", self.tab_pinjaman)

    def add_tab(self, tab_name, interface_function):
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        interface_function(tab_layout)
        tab_widget.setLayout(tab_layout)
        self.tab_widget.addTab(tab_widget, tab_name)

    def tab_buku(self, layout):
        h_layout = QHBoxLayout()
        v_layout = QVBoxLayout()

        db = DatabaseHandler()  
        self.books = db.get_data("SELECT * FROM buku")
        self.current_book_index = 0

        button_first = QPushButton("First")
        button_next = QPushButton("Next")
        button_manage = QPushButton("Kelola Buku")
        button_prev = QPushButton("Previous")
        button_last = QPushButton("Last")

        h_layout.addWidget(button_first)
        h_layout.addWidget(button_prev)
        h_layout.addWidget(button_manage)
        h_layout.addWidget(button_next)
        h_layout.addWidget(button_last)

        button_first.clicked.connect(self.go_to_first_book)
        button_prev.clicked.connect(self.go_to_previous_book)
        button_manage.clicked.connect(self.dialog_buku)
        button_next.clicked.connect(self.go_to_next_book)
        button_last.clicked.connect(self.go_to_last_book)

        form_layout = QFormLayout()
        self.id_buku = QLineEdit(self)
        self.nama_buku = QLineEdit(self)
        self.stok = QLineEdit(self)
        self.tahun_terbit = QLineEdit(self)

        form_layout.addRow(QLabel("ID Buku:"), self.id_buku)
        form_layout.addRow(QLabel("Nama Buku:"), self.nama_buku)
        form_layout.addRow(QLabel("Stok:"), self.stok)
        form_layout.addRow(QLabel("Tahun Terbit:"), self.tahun_terbit)

        form_h_layout = QHBoxLayout()
        form_h_layout.addSpacing(200)
        form_h_layout.addLayout(form_layout)
        form_h_layout.addSpacing(200)

        v_layout.addStretch()
        v_layout.addLayout(form_h_layout)
        v_layout.addStretch()

        layout.addLayout(v_layout)
        layout.addLayout(h_layout)

        self.load_book_data()

    def load_book_data(self):
        if len(self.books) < 1:
            return 
        book = self.books[self.current_book_index]
        self.id_buku.setText(str(book["id_buku"]))
        self.nama_buku.setText(book["nama_buku"])
        self.stok.setText(str(book["stok"]))
        self.tahun_terbit.setText(str(book["tahun_terbit"]))

    def go_to_first_book(self):
        self.current_book_index = 0
        self.load_book_data()

    def go_to_previous_book(self):
        if self.current_book_index > 0:
            self.current_book_index -= 1
            self.load_book_data()

    def go_to_next_book(self):
        if self.current_book_index < len(self.books) - 1:
            self.current_book_index += 1
            self.load_book_data()

    def go_to_last_book(self):
        self.current_book_index = len(self.books) - 1
        self.load_book_data()

    def tab_anggota(self, layout):
        h_layout = QHBoxLayout()

        db = DatabaseHandler()  
        self.members = db.get_data("SELECT * FROM anggota")
        self.current_member_index = 0

        button_first = QPushButton("First")
        button_next = QPushButton("Next")
        button_manage = QPushButton("Kelola Anggota")
        button_prev = QPushButton("Previous")
        button_last = QPushButton("Last")

        h_layout.addWidget(button_first)
        h_layout.addWidget(button_prev)
        h_layout.addWidget(button_manage)
        h_layout.addWidget(button_next)
        h_layout.addWidget(button_last)

        button_first.clicked.connect(self.go_to_first_member)
        button_prev.clicked.connect(self.go_to_previous_member)
        button_manage.clicked.connect(self.dialog_anggota)
        button_next.clicked.connect(self.go_to_next_member)
        button_last.clicked.connect(self.go_to_last_member)

        form_layout = QFormLayout()
        self.id_anggota = QLineEdit(self)
        self.nama = QLineEdit(self)
        self.alamat = QLineEdit(self)

        form_layout.addRow(QLabel("ID Anggota:"), self.id_anggota)
        form_layout.addRow(QLabel("Nama:"), self.nama)
        form_layout.addRow(QLabel("Alamat:"), self.alamat)

        form_h_layout = QHBoxLayout()
        form_h_layout.addSpacing(200)
        form_h_layout.addLayout(form_layout)
        form_h_layout.addSpacing(200)

        v_layout = QVBoxLayout()
        v_layout.addStretch()
        v_layout.addLayout(form_h_layout)
        v_layout.addStretch()

        layout.addLayout(v_layout)
        layout.addLayout(h_layout)

        self.load_member_data()

    def load_member_data(self):
        if len(self.members) < 1:
            return 
        member = self.members[self.current_member_index]
        self.id_anggota.setText(str(member["id_anggota"]))
        self.nama.setText(member["nama"])
        self.alamat.setText(str(member["alamat"]))

    def go_to_first_member(self):
        self.current_member_index = 0
        self.load_member_data()

    def go_to_previous_member(self):
        if self.current_member_index > 0:
            self.current_member_index -= 1
            self.load_member_data()

    def go_to_next_member(self):
        if self.current_member_index < len(self.members) - 1:
            self.current_member_index += 1
            self.load_member_data()

    def go_to_last_member(self):
        self.current_member_index = len(self.members) - 1
        self.load_member_data()

    def tab_pinjaman(self, layout):
        button = QPushButton("Kelola Pinjaman")
        button.clicked.connect(self.dialog_pinjaman)
        layout.addWidget(button)

    def dialog_buku(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Buku")
        dialog.setGeometry(200, 200, 540, 439)

        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        self.input_judul = QLineEdit()
        self.cari1 = QPushButton("Cari")
        self.input_tahun = QLineEdit()
        self.cari2 = QPushButton("Cari")

        filter_layout.addWidget(QLabel("Judul"))
        filter_layout.addWidget(self.input_judul)
        filter_layout.addWidget(self.cari1)
        filter_layout.addWidget(QLabel("Tahun Terbit"))
        filter_layout.addWidget(self.input_tahun)
        filter_layout.addWidget(self.cari2)

        self.cari1.clicked.connect(lambda: self.searchFilter(self.input_judul.text(), "nama_buku"))
        self.cari2.clicked.connect(lambda: self.searchFilter(self.input_tahun.text(), "tahun_terbit"))

        self.model = QSqlTableModel()
        self.model.setTable("buku")
        self.model.select()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        manage_widget = QWidget()
        manage_layout = QHBoxLayout(manage_widget)
        update_button = QPushButton("Update")
        update_button.clicked.connect(lambda: self.update_data("buku"))
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.model.revertAll())
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.dialog_tambah_buku)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_data("buku"))

        manage_layout.addWidget(update_button)
        manage_layout.addWidget(cancel_button)
        manage_layout.addWidget(add_button)
        manage_layout.addWidget(delete_button)

        layout = QVBoxLayout()
        layout.addWidget(filter_widget)
        layout.addWidget(self.table_view)
        layout.addWidget(manage_widget)

        dialog.setLayout(layout)
        dialog.exec()

    def dialog_tambah_buku(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Tambah Buku")

        form_layout = QFormLayout()
        self.nama_buku_input = QLineEdit()
        self.stok_input = QLineEdit()
        self.tahun_terbit_input = QLineEdit()
        button_save = QPushButton("Simpan")
        button_save.clicked.connect(self.save_buku)

        form_layout.addRow("Nama Buku: ",self.nama_buku_input)
        form_layout.addRow("Stok Buku: ",self.stok_input)
        form_layout.addRow("Tahun Terbit: ",self.tahun_terbit_input)
        form_layout.addRow(button_save)
        
        dialog.setLayout(form_layout)
        dialog.exec()

    def save_buku(self):
        db = DatabaseHandler()
        nama_buku_value = self.nama_buku_input.text()
        stok_value = self.stok_input.text()
        tahun_terbit_value = self.tahun_terbit_input.text()

        data = {
            "nama_buku": nama_buku_value,
            "stok": int(stok_value),
            "tahun_terbit": tahun_terbit_value
        }

        db.insert_data("buku", data)
        self.nama_buku_input.clear()
        self.stok_input.clear()
        self.tahun_terbit_input.clear()
        self.handle_update_display("buku")


    def dialog_anggota(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Anggota")
        dialog.setGeometry(200, 200, 540, 439)

        filter_widget = QWidget()
        filter_layout = QHBoxLayout(filter_widget)
        self.input_nama = QLineEdit()
        self.cari1 = QPushButton("Cari")
        self.input_alamat = QLineEdit()
        self.cari2 = QPushButton("Cari")

        filter_layout.addWidget(QLabel("Nama"))
        filter_layout.addWidget(self.input_nama)
        filter_layout.addWidget(self.cari1)
        filter_layout.addWidget(QLabel("Alamat"))
        filter_layout.addWidget(self.input_alamat)
        filter_layout.addWidget(self.cari2)

        self.cari1.clicked.connect(lambda: self.searchFilter(self.input_nama.text(), "nama"))
        self.cari2.clicked.connect(lambda: self.searchFilter(self.input_alamat.text(), "alamat"))

        self.model = QSqlTableModel()
        self.model.setTable("anggota")
        self.model.select()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)

        manage_widget = QWidget()
        manage_layout = QHBoxLayout(manage_widget)
        update_button = QPushButton("Update")
        update_button.clicked.connect(lambda: self.update_data("anggota"))
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(lambda: self.model.revertAll())
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.dialog_tambah_anggota)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_data("anggota"))

        manage_layout.addWidget(update_button)
        manage_layout.addWidget(cancel_button)
        manage_layout.addWidget(add_button)
        manage_layout.addWidget(delete_button)

        layout = QVBoxLayout()
        layout.addWidget(filter_widget)
        layout.addWidget(self.table_view)
        layout.addWidget(manage_widget)

        dialog.setLayout(layout)
        dialog.exec()
    
    def dialog_tambah_anggota(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Tambah Anggota")

        form_layout = QFormLayout()
        self.nama_input = QLineEdit()
        self.alamat_input = QLineEdit()
        button_save = QPushButton("Simpan")
        button_save.clicked.connect(self.save_anggota)

        form_layout.addRow("Nama Lengkap: ",self.nama_input)
        form_layout.addRow("Alamat: ",self.alamat_input)
        form_layout.addRow(button_save)
        
        dialog.setLayout(form_layout)
        dialog.exec()
    
    def save_anggota(self):
        db = DatabaseHandler()
        nama_value = self.nama_input.text()
        alamat_value = self.alamat_input.text()

        data = {
            "nama": nama_value,
            "alamat": alamat_value
        }

        db.insert_data("anggota", data)
        self.nama_input.clear()
        self.alamat_input.clear()
        self.handle_update_display("anggota")

    def update_data(self, table_name):
        self.model.submitAll()
        self.handle_update_display(table_name)

    def delete_data(self, table_name):
        self.model.removeRow(self.table_view.currentIndex().row())
        self.model.submitAll()
        # self.model = QSqlTableModel()
        # self.model.setTable(table_name)
        # self.model.select()
        # self.table_view.setModel(self.model)
        self.handle_update_display(table_name)
    
    def handle_update_display(self, table_name):
        db = DatabaseHandler()
        self.model = QSqlTableModel()
        self.model.setTable(table_name)
        self.model.select()
        self.table_view.setModel(self.model)
        if table_name == "buku":
            self.books = db.get_data("SELECT * FROM buku")
            self.current_book_index = 0
            self.load_book_data()
        elif table_name == "anggota":
            self.members = db.get_data("SELECT * FROM anggota")
            self.current_member_index = 0
            self.load_member_data()
            
    def dialog_pinjaman(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Pinjaman")
        dialog.exec()

    def searchFilter(self, inputan, field):
        s = re.sub("[\W_]+", "", inputan)
        filter_str = f"{field} LIKE '%{s}%'"
        self.model.setFilter(filter_str)

    def close_tab(self, index):
        widget = self.tab_widget.widget(index)
        if widget:
            widget.deleteLater()
            self.tab_widget.removeTab(index)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()