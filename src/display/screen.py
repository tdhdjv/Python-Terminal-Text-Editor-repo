from __future__ import annotations
from typing import TYPE_CHECKING

import curses

if TYPE_CHECKING:
    from window import Window

class Screen:
    def __init__(self, stdscr:"curses._CursesWindow") -> None:
        self.stdscr = stdscr
        self.windows:list[Window] = []

    def resize(self) -> None:
        curses.update_lines_cols()
        for window in self.windows:
            window.resize()

    def render(self) -> None:
        for window in self.windows:
            window.render(self.stdscr)

    def add_window(self, window) -> None:
        self.windows.append(window)

    def __str__(self) -> str:
        string = ''
        return string