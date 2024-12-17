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
                 seed=None,
                 ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        
        if seed:
            random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def get_cells(self):
        return self._cells
    
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
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0,0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, x, y):
        self._cells[x][y].visited = True
        while True:
            next_index_list = []
            if x + 1 < self._num_cols:
                if not self._cells[x+1][y].visited:
                    next_index_list.append((x+1, y))
            if y + 1 < self._num_rows:
                if not self._cells[x][y+1].visited:
                    next_index_list.append((x, y+1))
            if x - 1 >= 0:
                if not self._cells[x-1][y].visited:
                    next_index_list.append((x-1, y))
            if y - 1 >= 0:
                if not self._cells[x][y-1].visited:
                    next_index_list.append((x, y-1))
            
            if len(next_index_list) == 0:
                self._draw_cell(x,y)
                break

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            if next_index[0] == x + 1:
                self._cells[x][y].has_right_wall = False
                self._cells[x + 1][y].has_left_wall = False
        
            if next_index[0] == x - 1:
                self._cells[x][y].has_left_wall = False
                self._cells[x - 1][y].has_right_wall = False
           
            if next_index[1] == y + 1:
                self._cells[x][y].has_bottom_wall = False
                self._cells[x][y + 1].has_top_wall = False
           
            if next_index[1] == y - 1:
                self._cells[x][y].has_top_wall = False
                self._cells[x][y - 1].has_bottom_wall = False
            
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def _solve_r(self, x, y):
        self._animate()
        self._cells[x][y].visited = True

        if x == self._num_cols - 1 and y == self._num_rows - 1:
            return True

        if x + 1 < self._num_cols:
            if not self._cells[x][y].has_right_wall and not self._cells[x+1][y].visited:
                self._cells[x][y].draw_move(self._cells[x+1][y])
                check_solution = self._solve_r(x+1, y)
                if check_solution:
                    return True
                else:
                    self._cells[x][y].draw_move(self._cells[x+1][y], True)

        if y + 1 < self._num_rows:
            if not self._cells[x][y].has_bottom_wall and not self._cells[x][y+1].visited:
                self._cells[x][y].draw_move(self._cells[x][y+1])
                check_solution = self._solve_r(x, y+1)
                if check_solution:
                    return True
                else:
                    self._cells[x][y].draw_move(self._cells[x][y+1], True)

        if x - 1 >= 0:
            if not self._cells[x][y].has_left_wall and not self._cells[x-1][y].visited:
                self._cells[x][y].draw_move(self._cells[x-1][y])
                check_solution = self._solve_r(x-1, y)
                if check_solution:
                    return True
                else:
                    self._cells[x][y].draw_move(self._cells[x-1][y], True)
        
        if y - 1 >= 0:
            if not self._cells[x][y].has_top_wall and not self._cells[x][y-1].visited:
                self._cells[x][y].draw_move(self._cells[x][y-1])
                check_solution = self._solve_r(x, y-1)
                if check_solution:
                    return True
                else:
                    self._cells[x][y].draw_move(self._cells[x][y-1], True)
        
        return False

    def solve(self):
        return self._solve_r(0,0)
