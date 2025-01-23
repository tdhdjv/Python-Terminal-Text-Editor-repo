from __future__ import annotations
from typing import TYPE_CHECKING

import curses

if TYPE_CHECKING:
    from window import Window

class Screen:
    def __init__(self, stdscr:"curses._CursesWindow") -> None:
        self.stdscr = stdscr
        self.windows:list[Window] = []
        curses.update_lines_cols()
        self._ncols = curses.COLS
        self._nlines = curses.LINES

    def resize(self) -> None:
        curses.update_lines_cols()
        self._ncols = curses.COLS
        self._nlines = curses.LINES

        for window in self.windows:
            window.resize()

    def render(self, debug=False) -> None:
        for window in self.windows:
            window.render(debug)

    def add_window(self, window) -> None:
        self.windows.append(window)

    def __str__(self) -> str:
        string = ''
        return string