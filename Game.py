import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from Board import Board
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QSpinBox


class Game(QMainWindow):

    def __init__(self, height, width, count, player_name):
        super().__init__()
        self.board = Board(height, width, count, player_name)
        self.board.setGeometry(100, 100, 2000, 1500)
        self.board.show()


class Form(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(520, 600)

        self.width = 2
        self.height = 2
        self.colors_count = 1
        self.name = ""

        self.lbl_height = QLabel("Enter height", self)
        self.lbl_height.move(20, 20)
        self.lbl_height.resize(480, 50)
        self.height_box = QSpinBox(self)
        self.height_box.move(20, 70)
        self.height_box.resize(480, 70)
        self.height_box.setMinimum(2)
        self.height_box.setMaximum(13)

        self.lbl_width = QLabel("Enter width", self)
        self.lbl_width.move(20, 140)
        self.lbl_width.resize(480, 70)
        self.width_box = QSpinBox(self)
        self.width_box.move(20, 190)
        self.width_box.resize(480, 70)
        self.width_box.setMinimum(2)
        self.width_box.setMaximum(25)

        self.lbl_colors = QLabel("Enter number of colors", self)
        self.lbl_colors.move(20, 260)
        self.lbl_colors.resize(480, 70)
        self.colors_box = QSpinBox(self)
        self.colors_box.move(20, 310)
        self.colors_box.resize(480, 70)
        self.colors_box.setMinimum(1)
        self.colors_box.setMaximum(13)

        self.lbl_name = QLabel("Enter your name", self)
        self.lbl_name.move(20, 380)
        self.lbl_name.resize(480, 70)
        self.name_box = QLineEdit(self)
        self.name_box.move(20, 430)
        self.name_box.resize(480, 70)

        self.button = QPushButton('START', self)
        self.button.move(20, 510)
        self.button.resize(480, 70)
        self.button.clicked.connect(self.on_click)

    def on_click(self):
        self.height = self.height_box.value()
        self.width = self.width_box.value()
        self.colors_count = self.colors_box.value()
        self.name = self.name_box.text()

        self.close()

        self.game = Game(self.height, self.width, self.colors_count, self.name)
        self.setCentralWidget(self.game)
        self.game.setGeometry(100, 100, 2000, 1500)
        self.game.show()


class Start(QMainWindow):

    def __init__(self):
        super().__init__()
        self.form = Form()

        self.form.setGeometry(100, 100, 2000, 1500)
        self.form.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    start = Start()

    sys.exit(app.exec_())
