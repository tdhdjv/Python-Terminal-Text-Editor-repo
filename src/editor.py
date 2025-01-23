import os

import curses

class EditorMode:
    INSERT = 0
    COMMAND = 1

class Editor :
    def __init__(self) -> None:
        self.mode = EditorMode.COMMAND
        self.filepath = ''
        self.saved = True
        self.running = True

    def run(self, stdscr:'curses._CursesWindow') -> None:
        pass