import sqlite3
import sys

import cur
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class Change_wnd(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.pushButton_3.clicked.connect(self.add_row)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee WHERE ID=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень обжарки", "молотый/в зёрнах", "Описание вкуса", "Цена", "Объём упаковки"])
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
            self.modified[self.titles[item.column()]] = item.text()

    def add_row(self):
        cur = self.con.cursor()
        try:
            cur.execute("INSERT INTO coffee(Title, Roast, Form, Description, Price, Volume) VALUES('', 0, 0, '', 0, 0)").fetchall()
            result = cur.execute("SELECT * FROM coffee").fetchall()
            self.spinBox.setValue(len(result))
            self.update_result()
        except Exception as e:
            print(f'Произошла ошибка: {e}')


    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                                for key in self.modified.keys()])
            que += "WHERE ID = ?"
            print(que)
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Change_wnd()
    ex.show()
    sys.exit(app.exec())