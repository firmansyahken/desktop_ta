# buku
    # -id_buku
    # -nama_buku
    # -stok
    # -tahun_terbit
# anggota
    # -id_anggota
    # -nama
    # -alamat
# peminjaman
    # -id_pinjaman
    # -anggota_id
    # -jumlah
# peminjaman_detail
    # -id_peminjaman_detail
    # -pinjaman_id
    # -buku_id
    # -tgl_pinjam
    # -tgl_kembali
import os
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

def connectionDB():
    db = QSqlDatabase.addDatabase("QSQLITE")
    dir = os.getcwd()
    ls = os.listdir(dir)
    if not "ad.db" in ls:
        db.setDatabaseName("ad.db")
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
        db.open()
        print ("ok")

connectionDB()