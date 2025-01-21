from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cursor import Cursor

def get_line(line_num:int, text:str, keepends:bool = False) -> str:
    """If line_num is bigger than the lines in the text then it will return a empty string"""
    if line_num < 0:
        return ''
    try:
        text.splitlines(line_num, keepends=keepends)[line_num]
    except IndexError:
        return ''
    
def get_line_count(text:str) -> int:
    lines = text.splitlines()
    if len(lines) == 0:
        return 1
    return len(lines)

def pos_to_string_index(text:str, y, x) -> int:
    index = -1
    for _ in range(y):
        index = text.find('\n', index+1)
        if index == -1:
            return -1
    return index + x + 1

def get_char(text:str, y, x) -> str:
    if y < 0 or x < 0:
        return ''
    lines = text.splitlines(True)
    try:
        return lines[y][x]
    except:
        return ''
    
def delete(text:str, y, x) -> str:
    string_index = pos_to_string_index(text, y, x)
    if string_index == -1:
        return
    return text[:string_index] +  text[string_index+1:]
    
def delete_cursor(text:str, cursor:Cursor) -> str:
    y, x = cursor.y, cursor.x
    return delete(text, y, x)

def delete_select(text:str, y1, x1, y2, x2) -> str:
    pos1 = pos_to_string_index(text, y1, x1)
    pos2 = pos_to_string_index(text, y2, x2)
    if pos1 == -1 or pos2 == -1 or pos2-pos1 < 0:
        return
    return text[:pos1] +  text[pos2+1:]
    
def insert(text:str, y, x, string:str) -> str:
    string_index = pos_to_string_index(text, y, x)
    if string_index == -1:
        return
    return text[:string_index] + string + text[string_index:]

def insert_cursor(text:str, cursor:Cursor, string:str) -> str:
    y, x = cursor.y, cursor.x
    return insert(text, y, x, string)
    