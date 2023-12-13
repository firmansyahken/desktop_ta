from PyQt6.QtWidgets import QWidget, QPushButton

def tab_menu(self):
    btn = QPushButton("Daftar Pinjaman")
    btn.pressed.connect(lambda: self.stacklayout.setCurrentIndex(0))
    self.button_layout.addWidget(btn)

    btn = QPushButton("Daftar Buku")
    btn.pressed.connect(lambda: self.stacklayout.setCurrentIndex(1))
    self.button_layout.addWidget(btn)

    btn = QPushButton("Daftar Anggota")
    btn.pressed.connect(lambda: self.stacklayout.setCurrentIndex(2))
    self.button_layout.addWidget(btn)

    btn = QPushButton("Tambah Buku")
    btn.pressed.connect(lambda: self.stacklayout.setCurrentIndex(3))
    self.button_layout.addWidget(btn)

    btn = QPushButton("Tambah Pinjaman")
    btn.pressed.connect(lambda: self.stacklayout.setCurrentIndex(4))
    self.button_layout.addWidget(btn)

    btn = QPushButton("Tambah Anggota")
    btn.pressed.connect(lambda: self.stacklayout.setCurrentIndex(5))
    self.button_layout.addWidget(btn)