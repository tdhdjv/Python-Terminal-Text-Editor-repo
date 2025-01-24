from __future__ import annotations
from typing import TYPE_CHECKING

import curses
import _curses

from utils import text_manager as txtman
from cursor import Cursor
if TYPE_CHECKING:
    from screen import Screen

class Window:

    def __init__(self, parent:Window|Screen, x:int = 0, y:int = 0, ncols:int = 0, nlines:int = 0, border = False)  -> None:
        self.x = x
        self.y = y
        self._ncols = ncols
        self._nlines = nlines
        self._parent = parent
        self._border = border
        self._visible = True

        self.text = ''
        self.active = False
        self.scroll_x = 0
        self.scroll_y = 0
        self.cursor = Cursor()
        self.children:list[Window] = []

        self.win:'curses._CursesWindow' = curses.newpad(self._nlines,self._ncols)

        if isinstance(self._parent, Window):
            self._parent.add_child(self)
        else:
            self._parent.add_window(self)

    def get_absolute_pos(self) -> tuple[int, int]:
        if isinstance(self._parent, Window):
            parent_abs_pos = self._parent.get_absolute_pos()
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

        self._nlines = nlines
        self._ncols = ncols
        self.win.resize(self._nlines, self._ncols)

    def resize(self):
        pass

    def render(self, debug:bool = False):
        if self._ncols == 0 or self._nlines == 0 or not self._visible:
            return

        if self._border or debug:
            self.win.box()

        if debug:
            try:
                self.win.insstr(0, 2, f"size({self._ncols}, {self._nlines}), pos({self.x}, {self.y})")
                self.win.insstr(self._nlines-1, 2, f"win size({curses.COLS}, {curses.LINES})")
            except:
                pass
        elif self.text:
            #set the scroll accroding to the cursor position
            self.scroll()
            
            #display the text
            displayed_text = self.get_shown_str(self.text)
            self.add_str(displayed_text, x=0, y=0)
            
            if self.active:
                #move the cursor
                y, x = self.cursor.y, self.cursor.x
                x -= self.scroll_x
                y -= self.scroll_y

                self.win.chgat(y, x, 1, curses.A_REVERSE)

        abs_pos = self.get_absolute_pos()
        self.win.noutrefresh(0, 0, abs_pos[1], abs_pos[0], abs_pos[1]+self._nlines-1, abs_pos[0]+self._ncols-1)

        for child in self.children:
            child.render(debug)

    def clear(self):
        self.win.clear()
        for child in self.children:
            child.clear()

    def clear_text(self):
        self.text = ''
        self.cursor.clamp(self.text)

    def add_str(self, string:str, x:int = 0, y:int = 0):
        self.win.addstr(y, x, string)

    def add_char(self, char:"_curses._ChType", x:int = 0, y:int = 0):
        self.win.addch(y, x, char)

    def edit_text(self, key:str) -> None:
        if key == 'KEY_LEFT':
            self.cursor.left()
        elif key == 'KEY_RIGHT':
            self.cursor.right()
        elif key == 'KEY_SRIGHT':
            self.cursor.selecting = True
            self.cursor.right()
        elif key == 'KEY_UP':
            self.cursor.up()
        elif key == 'KEY_DOWN':
            self.cursor.down()
        elif key == '\x17':
            y2, x2 = self.cursor.y, self.cursor.x
            self.cursor.left_word(self.text)
            y1, x1 = self.cursor.y, self.cursor.x
            self.text = txtman.delete_select(self.text, y1, x1, y2, x2)
        elif key == '\b':
            if(self.cursor.x != 0 or self.cursor.y != 0):
                self.cursor.left(self.text)
                self.text = txtman.delete_cursor(self.text, self.cursor)
        elif key == '\t':
            #TODO FIX
            self.text = txtman.insert_cursor(self.text, self.cursor, '   ')
            for _ in range(3):
                self.cursor.right()
        elif key == '\n':
            self.text = txtman.insert_cursor(self.text, self.cursor, key)
            self.cursor.down()
            self.cursor.x = 0
        elif isinstance(key, str) and len(key) == 1:
            self.text = txtman.insert_cursor(self.text, self.cursor, key)
            self.cursor.right()
        self.cursor.clamp(self.text)

    def scroll(self):
        start_y = self.scroll_y
        end_y = self.scroll_y + self._nlines

        if self.cursor.y > end_y-1:
            self.scroll_y = self.cursor.y - self._nlines+1
        if self.cursor.y < start_y:
            self.scroll_y = self.cursor.y

        start_x = self.scroll_x
        end_x = self.scroll_x + self._ncols

        if self.cursor.x > end_x-1:
            self.scroll_x = self.cursor.x - self._ncols + 1
        if self.cursor.x < start_x:
            self.scroll_x = self.cursor.x

    def get_shown_str(self, text:str):
        start_y = self.scroll_y
        end_y = self.scroll_y+self._nlines
        string = ''
        for line in text.splitlines(True)[start_y:end_y]:
            string += line[self.scroll_x: self.scroll_x+self._ncols]
        string = string.removesuffix('\n')

        return string
    