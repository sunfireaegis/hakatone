import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QFileDialog, QLabel, QScrollArea, QWidget, \
    QTableWidgetItem, QPushButton, QInputDialog
import sys


print("Hello World")
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('1.ui', self)

        self.con = sqlite3.connect("course_base.db")

        self.lineEdit.textChanged[str].connect(self.new_text)
        self.pushButton.clicked.connect(self.search_competences)
        self.comboBox.activated[str].connect(self.new_itm)

        self.position = ''
        self.lst_courses = []

        self.item = ''
        self.update_tableWidget()

        self.position = {}

    def new_text(self, text):
        self.position = text
        # print(self.position)

    def search_competences(self):
        cur = self.con.cursor()
        val = cur.execute(f"SELECT name FROM jobs").fetchall()
        print(val)
        val = [i[0] for i in val]
        if self.position in val:
            result = cur.execute(f'SELECT list FROM jobs WHERE name = "{self.position}"').fetchall()
            result = result[0][0].split('/')
        self.competencies = [''] + result
        self.update_comboBox()

    def update_comboBox(self):
        self.comboBox.addItems(self.competencies)

    def new_itm(self, item):
        self.item = item
        self.search_courses()

    def search_courses(self):
        cur = self.con.cursor()

        val = cur.execute(f"SELECT comp FROM final").fetchall()
        val = [i[0] for i in val]
        print(val)
        print(self.item)
        if self.item in val:
            val = cur.execute(f'SELECT courses FROM final WHERE comp = "{self.item}"').fetchall()
            val = val[0][0].split('/')
            print(val)
        self.lst_courses = val
        self.update_tableWidget()

    def update_tableWidget(self):
        if self.item != '':
            print(len(self.lst_courses))
            self.tableWidget.setRowCount(len(self.lst_courses))
            for i, val in enumerate(self.lst_courses):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
