from __future__ import annotations
from typing import TYPE_CHECKING

import curses

if TYPE_CHECKING:
    from screen import Screen

class Window:
    def __init__(self, parent:Window|Screen, x:int = 0, y:int = 0, ncols:int = 0, nlines:int = 0,)  -> None:
        self.x = x
        self.y = y
        self.ncols = ncols
        self.nlines = nlines
        self.parent = parent

        self.children:list[Window] = []

        if isinstance(self.parent, Window):
            self.parent.add_child(self)
        else:
            self.parent.add_window(self)

    def get_absolute_pos(self) -> tuple[int, int]:
        if isinstance(self.parent, Window):
            parent_abs_pos = self.parent.get_absolute_pos()
            return (self.x+parent_abs_pos[0], self.y+parent_abs_pos[1])
        else:
            return (self.x, self.y)

    def add_child(self, child:Window):
        self.children.append(child)

    def reshape(self, ncols:int, nlines:int, x:int|None = None, y:int|None = None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

        self.nlines = nlines
        self.ncols = ncols

    def resize(self):
        pass

    def render(self, stdscr:"curses._CursesWindow"):
        for child in self.children:
            child.render(stdscr)
        abs_pos = self.get_absolute_pos()
        for i in range(self.ncols):
            for j in range(self.nlines):
                stdscr.addch(abs_pos[1]+j, abs_pos[0]+i, 'a')