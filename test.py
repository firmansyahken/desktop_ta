from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

def connectionDB():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("ad.db")
    q = QSqlQuery()
    db.open()
    q.prepare("CREATE DATABASE test")
    q.prepare("CREATE TABLE user(id int(10))")
    q.exec()
    # if not db.open():
        # QSqlDataba

connectionDB()