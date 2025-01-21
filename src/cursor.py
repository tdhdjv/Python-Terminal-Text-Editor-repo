from __future__ import annotations
from typing import Iterable

import utils.text_manager as txtman

class Cursor:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        #used for when you move up or down to a line with fewer words but you need to remember the original x pos
        self.ghost_x = x

    def up(self, text:str = None) -> None:
        self.y += 1
        self.x = self.ghost_x
        self.clamp(text)
    
    def down(self, text:str = None) -> None:    
        self.y -= 1
        self.x = self.ghost_x
        self.clamp(text)
    
    
    def left(self, text:str = None) -> None:
        self.x -= 1
        self.clamp(text)
        self.ghost_x = self.x
    
    def right(self, text:str = None) -> None:
        self.x += 1
        self.clamp(text)
        self.ghost_x = self.x
    
    def clamp(self, text:str = None) -> None:
        if text:
            line = text_manager.get_line(self.y, text)
            line_count = text_manager.get_line_count(text)

            if self.x < 0:
                self.y -= 1
                #change value of the ```line``` as the y coord has changed
                line = text_manager.get_line(self.y, text)

                self.x = len(line)

            if self.x > len(line_count):
                self.y += 1
                #change value of the ```line``` as the y coord has changed
                line = text_manager.get_line(self.y, text)

                self.x = 0

            if self.y < 0:
                self.y = 0
                self.x = 0

            if self.y >= line_count:
                self.x = len(line)
                self.y = line_count-1

        else:
            self.x = max(self.x, 0)
            self.y = max(self.y, 0)

    def valid_pos(self, text:str = None) -> bool:
        if text:
            line = txtman.get_line(self.y, text)
            line_count = txtman.get_line_count(text)
            return 0 <= self.x <= len(line) and 0 <= self.y <= line_count-1
        else:
            return self.x >= 0 and self.y >= 0

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'
    
    def __add__(self, value) -> Cursor:
        if isinstance(value, Iterable) and len(value) == 2:
            return Cursor(self.x+value[0], self.y+value[1])
        raise Exception(f"{value} is not a valid type for adding to cursor position")