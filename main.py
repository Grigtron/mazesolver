from window import *
from cell import *


def main():
    win = Window(800,600)

    c = Cell(win)
    c.has_bottom_wall = False
    c.draw(50, 50, 100, 100)

    d = Cell(win)
    d.has_top_wall = False
    d.draw(50, 100, 100, 150)

    Cell.draw_move(c, d, undo=True)

    win.wait_for_close()



main()