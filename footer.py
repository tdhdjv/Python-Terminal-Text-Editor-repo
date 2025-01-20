import curses
from curses import window

import text_edits
from cursor import Cursor

class Footer:
    def __init__(self, n_lines:int, n_rows:int, footer_lines:int, std_scr:window) -> None:
        self.n_rows = n_rows
        self.scroll_x = 0

        self.footer = std_scr.subwin(footer_lines+1, n_rows, n_lines-footer_lines-1, 0)
        self.cursor = Cursor()

    def ask_question(self, question:str) -> str:
        command_prompt = ''
        while True:
            self.cursor.clamp(command_prompt)

            #scroll
            self.scroll(len(question))

            #display text
            self.footer.clear()
            self.footer.hline(curses.ACS_HLINE, curses.COLS-1)
            self.footer.addstr(1, 0, question + ": "+ command_prompt[self.scroll_x:self.scroll_x+self.n_rows-len(question)-2])
            self.footer.refresh()

            #move
            x = self.cursor.x + len(question) + 2
            x -= self.scroll_x
            self.footer.move(1, x)

            key = self.footer.getkey()
            if key == "KEY_LEFT":
                self.cursor.left(command_prompt)
            elif key == "KEY_RIGHT":
                self.cursor.right(command_prompt)
            elif key == 'CTL_LEFT':
                self.cursor.left_word(command_prompt)
            elif key == 'CTL_RIGHT':
                self.cursor.right_word(command_prompt)
            elif key == '\x17':
                y2, x2 = self.cursor.y, self.cursor.x
                self.cursor.left_word(command_prompt)
                y1, x1 = self.cursor.y, self.cursor.x
                command_prompt = text_edits.delete_select(command_prompt, y1, x1, y2, x2)
            elif key == '\b':
                if(self.cursor.x != 0 or self.cursor.y != 0):
                    self.cursor.left(command_prompt)
                    command_prompt = text_edits.delete_cursor(command_prompt, self.cursor)
            elif key == '\n':
                return command_prompt
            elif key == '\t':
                pass
            elif len(key) == 1:
                command_prompt = text_edits.insert_cursor(command_prompt, self.cursor, key)
                self.cursor.right(command_prompt)

    def scroll(self, question_len:int):
        start_x = self.scroll_x
        end_x = self.scroll_x + self.n_rows - question_len - 2

        if self.cursor.x > end_x-1:
            self.scroll_x = self.cursor.x - self.n_rows + 3 + question_len
        if self.cursor.x < start_x:
            self.scroll_x = self.cursor.x

    def display_text(self, text:str):
        text = ''.join(text.splitlines())
        self.footer.clear()
        self.footer.hline(curses.ACS_HLINE, self.n_rows)
        self.footer.addstr(1, 0, text[:self.n_rows])
        self.footer.refresh()