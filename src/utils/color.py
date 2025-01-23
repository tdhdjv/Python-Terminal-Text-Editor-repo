from __future__ import annotations
from typing import NamedTuple

import curses

class Color(NamedTuple):
    r:int
    g:int
    b:int
    def parse(code:str) -> Color:
        if len(code) == 0 or code[0] != '#':
            raise Exception(f"Invalid Hex code was given! (code: {code})")
        #3 value hex code
        if len(code) == 4:
            r = int(code[1]*2, 16)
            g = int(code[2]*2, 16)
            b = int(code[3]*2, 16)
            return Color(r, g, b)
        
        #6 value hex code
        if len(code) == 7:
            r = int(code[1:3], 16)
            g = int(code[3:5], 16)
            b = int(code[5:7], 16)
            return Color(r, g, b)
        
        raise Exception(f"Invalid Hex code was given! (code: {code})")
    
#have state
class ColorLibrary:
    _registered_color:dict[Color, int] = {}
    _registered_color_pair:dict[tuple[int, int], int] = {}

    def color_to_curses(color:Color) -> tuple[int, int, int]:
        multiplier = 1000/255
        return int(color.r*multiplier), int(color.g*multiplier), int(color.b*multiplier)

    def get_color_pair_id(fg:Color, bg:Color):
        ColorLibrary.register_color_pair(fg, bg)

        fg_id = ColorLibrary.get_color_id(fg)
        bg_id = ColorLibrary.get_color_id(bg)

        color_pair_id = ColorLibrary._registered_color_pair[(fg_id, bg_id)]
        return color_pair_id
    
    def pair_color(fg:Color, bg:Color):
        return curses.color_pair(ColorLibrary.get_color_pair_id(fg, bg))

    def get_color_id(color: Color|None) -> int:
        color_id = -1
        if color == None:
            return color_id
        
        ColorLibrary.register_color(color)
        color_id = ColorLibrary._registered_color[color]
        return color_id

    def register_color(color:Color) -> None:
        #check if the color is already registered
        if color in ColorLibrary._registered_color.keys():
            return
        
        if curses.can_change_color():
            n = min(ColorLibrary._registered_color.values() ,default = curses.COLORS) - 1
            r, g, b = ColorLibrary.color_to_curses(color)
            curses.init_color(n, r, g, b)
            ColorLibrary._registered_color[color] = n

    def register_color_pair(fg:Color|None, bg:Color|None) -> None:
        fg_id = ColorLibrary.get_color_id(fg)
        bg_id = ColorLibrary.get_color_id(bg)

        if (fg_id, bg_id) in ColorLibrary._registered_color_pair:
            return
        n = min(ColorLibrary._registered_color_pair.values(), default=curses.COLOR_PAIRS)-1
        curses.init_pair(n, fg_id, bg_id)
        ColorLibrary._registered_color_pair[(fg_id, bg_id)] = n

    def __str__() -> str:
        string = ''
        string += "Registered Colors:\n"
        for color, id in ColorLibrary._registered_color.items():
            string += f"<{id}> {color}\n"
        
        string += "Registerd Color_Pairs:\n"
        for pair, id in ColorLibrary._registered_color_pair.items():
            string += f"<{id}> {pair}\n"

        string.removesuffix('\n')
        
        return string

