from PyQt5.QtGui import QPainter, QColor, QFont
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton
from copy import deepcopy
from PyQt5.QtWidgets import QMainWindow


class Board(QMainWindow):
    colors = [0x66CCCC, 0x66CC66, 0xCC66CC,
              0xCCCC66, 0x6666CC, 0xCC6666, 0xDAAA00,
              0xbdecb6, 0xFF4500, 0x7FFFD4, 0x0000CD,
              0xFFFF00, 0xBC8F8F]

    fibonacci = [0, 0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584]

    def add_fibonacci(self, n):
        count = len(self.fibonacci) - 1

        while count != n:
            self.fibonacci.append(self.fibonacci[count - 1] + self.fibonacci[count - 2])
            count += 1

    size = 100

    history = []

    to_light = []

    result = []
    print_res = False

    EMPTY_COLOR = QColor(0x11111122)

    TO_REMOVE = QColor(0x000000)

    def get_score(self):

        if self.score >= len(self.fibonacci):
            self.add_fibonacci(self.score)
        self.common_score += self.fibonacci[self.score]
        self.score = 0

    def __init__(self, height, width, count, player_name):

        super().__init__()
        self.name = player_name

        self.height = height
        self.width = width
        self.colors_count = count

        self.score = 0
        self.common_score = 0
        self.table = []
        self.make_table()



        self.setMouseTracking(True)
        self.is_not_over = True

        self.setFocusPolicy(Qt.StrongFocus)

    def make_table(self):

        for i in range(self.width):
            self.table.append([])
            for j in range(self.height):
                rand = random.randint(0, self.colors_count - 1)
                self.table[i].append(QColor(self.colors[rand]))

        if self.are_in_board(0, 0, 1, 0):
            self.table[1][0] = self.table[0][0]
        elif self.are_in_board(0, 0, 0, 1):
            self.table[0][1] = self.table[0][0]
        else:
            self.is_not_over = False

        self.history.append((deepcopy(self.table), 0))

    def write_result(self):

        with open('results.txt', 'a', encoding='utf-8') as f:
            f.write(self.name + ' ' + str(self.common_score) + '\n')

        with open('results.txt', 'r', encoding='utf-8') as f:
            input = f.read()
        lines = input.split('\n')
        lines.pop()
        list = []
        for l in lines:
            name, score = l.split(' ')
            list.append((name, score))

        list.sort(key=lambda x: int(x[1]), reverse=True)
        self.result = list

    def paintEvent(self, e):

        painter = QPainter()
        painter.begin(self)
        self.drawRectangles(painter)

        self.drawScore(e, painter)
        painter.end()

        if self.print_res:

            self.close()

            self.res = Result(self.result)
            self.res.setGeometry(100, 100, 2000, 1500)

            self.res.show()

    def drawScore(self, event, qp):

        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 20))

        if self.is_not_over:
            qp.drawText(self.size * self.width + 50, 10, 500, 500, Qt.AlignLeft, "UNDO: <-")
            qp.drawText(self.size * self.width + 50, 100, 500, 500, Qt.AlignLeft, "REDO: ->")

        if self.is_not_over:
            qp.drawText(10, self.size * self.height + 100, 5000000, 500, Qt.AlignLeft,
                        "Score: " + str(self.common_score))
        else:
            qp.drawText(10, self.size * self.height + 100, 5000000, 500, Qt.AlignLeft,
                        "Game over!\nYour score: " + str(self.common_score) + '\nPress Space')

        if self.print_cur_score:
            self.print_cur_score = False
            qp.drawText(self.size * self.width + 50, 200, 50000, 500, Qt.AlignLeft,
                        "Block score: " + str(self.cur_score))

    def drawRectangles(self, qp):

        for i in range(self.width):
            for j in range(self.height):
                if self.table[i][j] != self.EMPTY_COLOR:

                    color = self.table[i][j]
                    if (i, j) in self.to_light:
                        color = color.lighter()

                    qp.setBrush(color)
                    qp.drawRect(100 * i, 100 * j, self.size, self.size)

        self.to_light.clear()

    state_number = 0
    was_back = False

    def keyPressEvent(self, event):

        key = event.key()

        if key == Qt.Key_Space and not self.is_not_over:
            self.print_res = True
            self.update()

        if key == Qt.Key_Right and self.is_not_over:

            if self.state_number + 1 < len(self.history):
                self.state_number += 1
                self.table = deepcopy(self.history[self.state_number][0])
                self.common_score = deepcopy(self.history[self.state_number][1])
                self.update()

        if key == Qt.Key_Left and self.is_not_over:

            if self.state_number - 1 >= 0:
                self.was_back = True
                self.state_number -= 1
                self.table = deepcopy(self.history[self.state_number][0])
                self.common_score = deepcopy(self.history[self.state_number][1])
                self.update()

    def mouseReleaseEvent(self, e):

        if self.is_not_over:
            x = e.pos().x() // 100
            y = e.pos().y() // 100

            if 0 <= x < self.width and 0 <= y < self.height:

                count = len(self.find_color_neighbors(x, y))
                empty = self.table[x][y] != self.EMPTY_COLOR

                self.remove_cubes(x, y)
                self.fall()

                if count > 1 and empty:
                    if self.was_back:
                        self.history = deepcopy(self.history[0:self.state_number + 1])
                        self.was_back = False
                    self.get_score()
                    self.history.append((deepcopy(self.table), self.common_score))
                    self.state_number += 1

                self.check_empty_columns()
                self.is_not_over = self.check()

                same_color = self.find_color_neighbors(x, y)

                if len(same_color) > 1:
                    self.to_light = same_color

                    if len(same_color) >= len(self.fibonacci):
                        self.add_fibonacci(len(same_color))

                    self.cur_score = self.fibonacci[len(same_color)]
                    self.print_cur_score = True

    def find_color_neighbors(self, x, y):

        same_color = [(x, y)]
        for (x, y) in same_color:

            if 0 <= x < self.width and 0 <= y < self.height and self.table[x][y] != self.EMPTY_COLOR:

                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if abs(dx) != abs(dy) and self.width > dx + x >= 0 \
                                and 0 <= dy + y < self.height and self.table[x + dx][y + dy] == self.table[x][y] \
                                and (dx + x, y + dy) not in same_color:
                            same_color.append((dx + x, y + dy))
        return same_color

    print_cur_score = False
    cur_score = 0

    def mouseMoveEvent(self, e):

        y = e.pos().y() // 100
        x = e.pos().x() // 100
        same_color = self.find_color_neighbors(x, y)

        if len(same_color) > 1:

            self.to_light = same_color

            if len(same_color) >= len(self.fibonacci):
                self.add_fibonacci(len(same_color))

            self.cur_score = self.fibonacci[len(same_color)]
            self.print_cur_score = True

        self.update()

    def remove_cubes(self, i, j):

        if self.are_in_board(i, j, 0, 0) and self.table[i][j] != self.EMPTY_COLOR:

            same_color = self.find_color_neighbors(i, j)

            if len(same_color) > 1:

                for (x, y) in same_color:

                    self.score += 1
                    self.table[x][y] = self.TO_REMOVE

            self.update()

    def are_in_board(self, x, y, shift_x, shift_y):

        return 0 <= x + shift_x < self.width and 0 <= y + shift_y < self.height

    def fall(self):

        for i in range(self.width):
            for j in range(self.height):
                if self.table[i][j] == self.TO_REMOVE:
                    if 0 <= j - 1 < self.height:
                        self.table[i][j] = self.table[i][j - 1]
                        self.table[i][j - 1] = self.TO_REMOVE
                        self.fall()
                        return
                    else:
                        self.table[i][j] = self.EMPTY_COLOR

    def check(self):

        if not self.has_same_color():

            self.get_score()
            self.write_result()
            return False
        return True

    def has_same_color(self):

        for x in range(self.width):
            for y in range(self.height):
                if len(self.find_color_neighbors(x, y)) > 1:
                    return True
        return False

    def check_cell(self, x, y, color):

        if self.EMPTY_COLOR != color:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    if abs(j) != abs(i):
                        if self.are_in_board(x, y, i, j):
                            if color == self.table[x + i][y + j]:
                                return True
        return False

    def check_empty_columns(self):

        to_shift = []
        for x in range(self.width):
            if self.table[x][self.height - 1] == self.EMPTY_COLOR:
                to_shift.append(x)
        to_shift.reverse()
        for x in to_shift:
            self.shift(x)

    def shift(self, x):

        self.table.pop(x)
        self.table.append([self.EMPTY_COLOR for i in range(self.height)])


from Game import Start


class Result(QMainWindow):

    def __init__(self, result):
        super().__init__()
        self.result = result

        self.button = QPushButton('RESTART', self)
        self.button.move(1000, 1000)
        self.button.resize(200, 200)
        self.button.clicked.connect(self.on_click)

    def paintEvent(self, e):

        painter = QPainter()
        painter.begin(self)
        self.draw_results(painter)
        painter.end()

    def draw_results(self, qp):

        qp.setBrush(QColor(0xbdecb6))
        qp.drawRect(0, 0, 20000, 20000)

        qp.setPen(QColor(168, 34, 3))
        qp.setFont(QFont('Decorative', 20))

        qp.drawText(10, 10, 500, 500, Qt.AlignLeft, 'Best 10\n\nSCORE TABLE')

        count = 1

        for i in range(len(self.result)):
            qp.drawText(10, 70 * (i + 5) + 100, 500, 500, Qt.AlignLeft, self.result[i][0])
            qp.drawText(350, 70 * (i + 5) + 100, 5000000, 500, Qt.AlignLeft, self.result[i][1])
            if count == 10:
                break
            count += 1

    def on_click(self):
        self.close()
        self.start = Start()
