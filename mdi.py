import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow, QDialog, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QTabWidget, QWidget,  QTableWidget, QTableWidgetItem, QTableView, QLineEdit, QFormLayout
from PyQt6.QtGui import QAction
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlQuery

def connectionDB():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("perpustakaan.db")

    if not db.open():
        return False
    return True

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
        print(query)
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

        form_layout.addRow(QLabel("ID Buku:"), self.id_buku)
        form_layout.addRow(QLabel("Nama Buku:"), self.nama_buku)
        form_layout.addRow(QLabel("Stok:"), self.stok)

        layout.addLayout(form_layout)
        layout.addLayout(h_layout)

        self.load_book_data()

    def load_book_data(self):
        book = self.books[self.current_book_index]
        self.id_buku.setText(str(book["id_buku"]))
        self.nama_buku.setText(book["nama_buku"])
        self.stok.setText(str(book["stok"]))

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
        self.members = db.get_data("SELECT * FROM user")
        print(self.members)
        self.current_member_index = 0

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

        button_first.clicked.connect(self.go_to_first_member)
        button_prev.clicked.connect(self.go_to_previous_member)
        button_next.clicked.connect(self.go_to_next_member)
        button_last.clicked.connect(self.go_to_last_member)

        form_layout = QFormLayout()
        self.id_user = QLineEdit(self)
        self.nama = QLineEdit(self)
        self.alamat = QLineEdit(self)

        form_layout.addRow(QLabel("ID Anggota:"), self.id_user)
        form_layout.addRow(QLabel("Nama:"), self.nama)
        form_layout.addRow(QLabel("Alamat:"), self.alamat)

        layout.addLayout(form_layout)
        layout.addLayout(h_layout)

        self.load_member_data()

    def load_member_data(self):
        member = self.members[self.current_member_index]
        self.id_user.setText(str(member["id_user"]))
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
        dialog.setGeometry(200, 200, 980, 760)

        model = QSqlTableModel(self)
        model.setTable("buku")
        model.select()

        table_view = QTableView()
        table_view.setModel(model)

        layout = QVBoxLayout()
        layout.addWidget(table_view)

        dialog.setLayout(layout)
        dialog.exec()

    def dialog_anggota(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Anggota")
        dialog.exec()

    def dialog_pinjaman(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Pinjaman")
        dialog.exec()

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

    
