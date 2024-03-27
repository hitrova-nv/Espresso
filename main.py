from PyQt5 import QtWidgets
from PyQt5 import uic
import sqlite3
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QApplication, QPushButton, QTableWidgetItem, QMainWindow, QTableWidget, QVBoxLayout, QLabel
import sys
from addEditCoffeeForm import Change_wnd
file_name = "coffee.sqlite"
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.change_button.clicked.connect(self.change_wnd)
        self.refresh.clicked.connect(self.refresh_table)
        self.wnd = None
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(file_name)
        self.db.open()
        self.refresh_table()
        self.show()

    def change_wnd(self):
        if self.wnd is None:
            self.wnd = Change_wnd()
        self.wnd.show()

    def refresh_table(self):
        con = sqlite3.connect(file_name)
        cur = con.cursor()
        result = cur.execute(
            """SELECT coffee.ID, coffee.Title, roasts.Title, coffee.Form, coffee.Description, coffee.Price, coffee.Volume  FROM coffee INNER JOIN roasts ON roasts.ID = coffee.Roast""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень обжарки", "молотый/в зёрнах", "Описание вкуса", "Цена", "Объём упаковки"])
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec()
    window.db.close()