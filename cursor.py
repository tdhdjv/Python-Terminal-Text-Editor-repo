from __future__ import annotations
from typing import TYPE_CHECKING
import text_edits

class Cursor:
    def __init__(self, x = 0, y = 0):
        self.ghost_x = x
        self.x = x
        self.y = y

        self.selecting = False
        self.previous_x = x
        self.previous_y = y

    def select(self):
        self.selecting = True

    def deselect(self):
        self.selecting = False
        self.previous_x = self.x
        self.previous_y = self.y
        
    def clamp(self, text:str) -> None:
        max_col = len(text_edits.get_line(text, self.y))
        max_row = text.count('\n')

        if self.x < 0:
            self.y -= 1
            max_col = len(text_edits.get_line(text, self.y))
            self.x = max_col
        
        if self.x > max_col:
            self.x = max_col
        
        if self.y > max_row:
            self.y = max_row
            max_col = len(text_edits.get_line(text, self.y))
            self.x = max_col

        self.y = max(0, self.y)
        if not self.selecting:
            self.previous_x = self.x
            self.previous_y = self.y

    def up(self, text:str) -> None:
        self.y -= 1
        self.x = self.ghost_x
        self.clamp(text)

    def down(self, text:str) -> None:
        self.y += 1
        self.x = self.ghost_x
        self.clamp(text)

    def left(self, text:str) -> None:
        self.x -= 1
        self.clamp(text)
        self.ghost_x = self.x

    def right(self, text:str) -> None:
        self.x += 1
        if self.x > len(text_edits.get_line(text, self.y)):
            self.y += 1
            self.x = 0
        self.clamp(text)
        self.ghost_x = self.x

    def left_word(self, text:str) -> None:
        self.left(text)
        #word check
        char = text_edits.get_char(text, self.y, self.x-1)
        
        if char.isalpha():
            while(char.isalpha()):
                self.left(text)
                char = text_edits.get_char(text, self.y, self.x-1)
            return
        
        #repeated char check
        repeated_word = text_edits.get_char(text, self.y, self.x)
        if repeated_word == '':
            return
        while char == repeated_word:
            self.left(text)
            char = text_edits.get_char(text, self.y, self.x-1)

    def right_word(self, text:str) -> None:
        self.right(text)
        #word check
        char = text_edits.get_char(text, self.y, self.x+1)
        if char.isalpha():
            while(char.isalpha()):
                self.right(text)
                char = text_edits.get_char(text, self.y, self.x)
            return
        
        #repeated char check
        repeated_word = text_edits.get_char(text, self.y, self.x)
        while char == repeated_word and char != '':
            self.right(text)
            char = text_edits.get_char(text, self.y, self.x)