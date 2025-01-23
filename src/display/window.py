from __future__ import annotations
from typing import TYPE_CHECKING

import curses

from utils.color import Color
from utils.color import ColorLibrary

if TYPE_CHECKING:
    from screen import Screen

class Window:
    def __init__(self, stdscr: "curses._CursesWindow", parent:Window|Screen, x:int = 0, y:int = 0, ncols:int = 0, nlines:int = 0, border = False)  -> None:
        self.x = x
        self.y = y
        self._ncols = ncols
        self._nlines = nlines
        self._parent = parent
        self._border = border
        self._visible = True

        self.text:str = ''
        self.children:list[Window] = []

        if isinstance(self._parent, Window):
            self._parent.add_child(self)
        else:
            self._parent.add_window(self)
        
        self.win = stdscr.subwin(0, 0, 0, 0)
        self.update_window()

    def get_absolute_pos(self) -> tuple[int, int]:
        if isinstance(self._parent, Window):
            parent_abs_pos = self._parent.get_absolute_pos()
            return (self.x+parent_abs_pos[0], self.y+parent_abs_pos[1])
        else:
            return (self.x, self.y)

    def update_window(self) -> None:
        x1 = self.x
        y1 = self.y
        x2 = self.x + self._ncols
        y2 = self.y + self._nlines

        parent_cols = self._parent._ncols
        parent_lines = self._parent._nlines

        x1 = min(max(0, x1), parent_cols)
        y1 = min(max(0, y1), parent_lines)
        x2 = min(x2, parent_cols)
        y2 = min(y2, parent_lines)

        cut_off_col = x2-x1
        cut_off_line = y2-y1

        if cut_off_line <= 0 or cut_off_line <= 0:
            self._visible = False
        else:
            self._visible = True
        
        #we move the window to 0,0 inorder to not fail the window resizing
        self.win.mvwin(0, 0)
        self.win.resize(cut_off_line, cut_off_col)
        self.win.mvwin(y1, x1)
        self.win.resize(cut_off_line, cut_off_col)

    def add_child(self, child:Window):
        self.children.append(child)

    def reshape(self, ncols:int, nlines:int, x:int|None = None, y:int|None = None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y

        self._nlines = nlines
        self._ncols = ncols
        self.update_window()

    def resize(self):
        pass

    def render(self, debug:bool = False):
        for child in self.children:
            child.render(debug)
        if not self._visible:
            return
        text_offset_x = 0
        text_offset_y = 0

        if self._border or debug:
            self.win.box()
            text_offset_x = 1
            text_offset_y = 1
        if debug:
            self.win.insstr(0, 2, f"size({self._ncols}, {self._nlines}), pos({self.x}, {self.y})")
            self.win.insstr(1, 1, f"win size({curses.COLS}, {curses.LINES})")

        for n, line in enumerate(self.text.splitlines()):
            try:
                self.win.addstr(n+text_offset_y, text_offset_x, line)
            except curses.error:
                break