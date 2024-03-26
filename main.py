from PyQt5 import QtWidgets
from PyQt5 import uic
import sqlite3
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication, QPushButton, QTableWidgetItem, QMainWindow, QTableWidget
import sys
file_name = "coffee.sqlite"
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(file_name)
        self.db.open()
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        result = cur.execute("""SELECT coffee.ID, coffee.Title, roasts.Title, coffee.Form, coffee.Description, coffee.Price, coffee.Volume  FROM coffee INNER JOIN roasts ON roasts.ID = coffee.Roast""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "молотый/в зёрнах", "Описание вкуса", "Цена", "Объём упаковки"])
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.show()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
    window.db.close()