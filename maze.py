from window import *
from cell import *
import time
import random


class Maze:
    def __init__(self,
                 x1,
                 y1,
                 num_rows,
                 num_cols,
                 cell_size_x,
                 cell_size_y,
                 win=None,
                 ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        self._create_cells()
    
    def _create_cells(self):
        for x in range(0, self._num_cols):
            column = []
            for y in range(0, self._num_rows):
                column.append(Cell(self._win))
            self._cells.append(column)
        
        for x in range(0, self._num_cols):
            for y in range(0, self._num_rows):
                self._draw_cell(x, y)
    
    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + (i * self._cell_size_x)
        y1 = self._y1 + (j * self._cell_size_y)
        x2 = self._x1 + self._cell_size_x
        y2 = self._y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)