import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np


class GameOfLife(QWidget):
    def __init__(self, rows, cols, randomize=True, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols))
        self.cell_size = 10
        self.setFixedSize(self.cols * self.cell_size, self.rows * self.cell_size)

        # Create the QLabel widget and set its text to the rules of the game.
        self.rules_label = QLabel(self)
        self.rules_label.setText(
            "Game of Life rules:\n"
            "1. Any live cell with fewer than two live neighbors dies.\n"
            "2. Any live cell with two or three live neighbors lives on to the next generation.\n"
            "3. Any live cell with more than three live neighbors dies.\n"
            "4. Any dead cell with exactly three live neighbors becomes a live cell.\n"
            "The Game Will start in 10 seconds"
        )

        # Add the QLabel widget to the app's main window.
        layout = QVBoxLayout(self)
        layout.addWidget(self.rules_label)

        self.timer = QBasicTimer()
        self.is_running = False

    def randomize(self):
        self.board = np.random.randint(0, 2, (self.rows, self.cols))
        self.rules_label.hide()


    def step(self):
        new_board = np.zeros((self.rows, self.cols))
        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.get_neighbors(r, c)
                if self.board[r][c] == 0 and neighbors.count(1) == 3:
                    new_board[r][c] = 1
                elif self.board[r][c] == 1 and (neighbors.count(1) < 2 or neighbors.count(1) > 3):
                    new_board[r][c] = 0
                else:
                    new_board[r][c] = self.board[r][c]
        self.board = new_board
        self.update()

    def get_neighbors(self, row, col):
        neighbors = []
        for r in range(row-1, row+2):
            if r < 0 or r >= self.rows:
                continue
            for c in range(col-1, col+2):
                if c < 0 or c >= self.cols or (r == row and c == col):
                    continue
                if r >= 0 and r < self.rows and c >= 0 and c < self.cols:
                    neighbors.append(self.board[r][c])
        return neighbors

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(100, self)
            self.randomize()
            # Call the `randomize` method to randomly initialize the game board.
           # self.randomize()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            self.update()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.step()
            self.update()
        else:
            super().timerEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == 1:
                    painter.fillRect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size, QBrush(Qt.black))

    def mousePressEvent(self, event):
        c = event.x() // self.cell_size
        r = event.y() // self.cell_size
        if r >= 0 and r < self.rows and c >= 0 and c < self.cols:
            self.board[r][c] = 1 if self.board[r][c] == 0 else 0
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameOfLife(50, 50)
    game.show()
     # Add a QPushButton widget to the app.
    randomize_button = QPushButton('Randomize', game)

    # Connect the `clicked` signal of the QPushButton widget to the `randomize` method of the GameOfLife class.
    randomize_button.clicked.connect(game.randomize)
        # Use a QTimer object to schedule the `start` method to be called after 10 seconds.
    QTimer.singleShot(10000, game.start)
    sys.exit(app.exec_())
