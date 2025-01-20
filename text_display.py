import text_edits
from cursor import Cursor

import curses
from curses import window

class TextDisplay :

    def __init__(self, n_lines:int, n_rows:int, offset:int, stdscr:window) -> None:
        self.scroll_y = 0
        self.scroll_x = 0
        self.n_lines = n_lines
        self.n_rows = n_rows

        self.cursor = Cursor()
        self.text = ''
        self.NUMBER_DISPLAY_COLS = 5

        self.number_display = stdscr.subwin(n_lines, self.NUMBER_DISPLAY_COLS, offset, 0)
        self.body_display = stdscr.subwin(n_lines, n_rows-self.NUMBER_DISPLAY_COLS, offset, 5)

    def display(self) -> None:
        #set the scroll accroding to the cursor position
        self.scroll()
        
        self.body_display.clear()
        self.number_display.clear()

        #display the text
        displayed_text = self.get_shown_str(self.text)
        self.body_display.addstr(0, 0, displayed_text)
        
        #display the numbers
        start_num = self.scroll_y+1
        for i in range(self.n_lines):
            self.number_display.addstr(i, 0, str(start_num+i))
            self.number_display.addch(i, 3, curses.ACS_VLINE)
        self.number_display.refresh()

        #move the cursor
        y, x = self.cursor.y, self.cursor.x
        x -= self.scroll_x
        y -= self.scroll_y
        self.body_display.move(y, x)

        #highlighted texts
        py, px = self.cursor.previous_y, self.cursor.previous_x
        py -= self.scroll_y
        px -= self.scroll_x
        self.body_display.refresh()

    def get_key(self) -> str:
        return self.body_display.getkey()

    def edit_text(self, key:str) -> None:
        if key == "KEY_LEFT":
            self.cursor.left(self.text)
        elif key == "KEY_RIGHT":
            self.cursor.right(self.text)
        elif key == "KEY_SRIGHT":
            self.cursor.selecting = True
            self.cursor.right(self.text)
        elif key == "KEY_UP":
            self.cursor.up(self.text)
        elif key == "KEY_DOWN":
            self.cursor.down(self.text)
        elif key == 'CTL_LEFT':
            self.cursor.left_word(self.text)
        elif key == 'CTL_RIGHT':
            self.cursor.right_word(self.text)
        elif key == '\x17':
            y2, x2 = self.cursor.y, self.cursor.x
            self.cursor.left_word(self.text)
            y1, x1 = self.cursor.y, self.cursor.x
            self.text = text_edits.delete_select(self.text, y1, x1, y2, x2)
        elif key == '\b':
            if(self.cursor.x != 0 or self.cursor.y != 0):
                self.cursor.left(self.text)
                self.text = text_edits.delete_cursor(self.text, self.cursor)
        elif key == '\t':
            #TODO FIX
            self.text = text_edits.insert_cursor(self.text, self.cursor, '   ')
            for _ in range(3):
                self.cursor.right(self.text)
        elif len(key) == 1:
            self.text = text_edits.insert_cursor(self.text, self.cursor, key)
            self.cursor.right(self.text)

    def load_text(self, text:str) -> None:
        self.text = text
    
    def scroll(self):
        start_y = self.scroll_y
        end_y = self.scroll_y + self.n_lines

        if self.cursor.y > end_y-1:
            self.scroll_y = self.cursor.y - self.n_lines+1
        if self.cursor.y < start_y:
            self.scroll_y = self.cursor.y

        start_x = self.scroll_x
        end_x = self.scroll_x + self.n_rows - self.NUMBER_DISPLAY_COLS

        if self.cursor.x > end_x-1:
            self.scroll_x = self.cursor.x - self.n_rows + self.NUMBER_DISPLAY_COLS + 1
        if self.cursor.x < start_x:
            self.scroll_x = self.cursor.x

    def get_shown_str(self, text:str):
        start_y = self.scroll_y
        end_y = self.scroll_y+self.n_lines
        string = ''
        for line in text.splitlines(True)[start_y:end_y]:
            string += line[self.scroll_x: self.scroll_x+self.n_rows-5]
        string = string.removesuffix('\n')

        return string