from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum

import curses

from window import Window

class AnchorLayout(Enum):
    NEG = 0
    CENTER = 1
    POS = 2

#window but you can use anchors so that the screen is resize accordingly
class AnchoredWindow (Window):
    def __init__(self, parent:Window, anchor_x:float = 0.0, anchor_y:float = 0.0, margin_x:int = 0, margin_y:int = 0,
                  anchor_layout_x:AnchorLayout = AnchorLayout.CENTER, anchor_layout_y:AnchorLayout = AnchorLayout.CENTER) -> None:
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.margin_x = margin_x
        self.margin_y = margin_y

        self.anchor_layout_x = anchor_layout_x
        self.anchor_layout_y = anchor_layout_y

        size = self.calc_size()
        pos = self.calc_pos()

        super.__init__(parent, x = pos[0], y = pos[1], ncols = size[0], nlines = size[1])

    def calc_pos(self) -> tuple[int, int]:
        x = 0
        y = 0

        anchor_pos_dict_x = {AnchorLayout.NEG: 0                                   + self.margin_x,
                            AnchorLayout.CENTER: (self.parent.ncols-self.ncols)//2 + self.margin_x,
                            AnchorLayout.POS: self.parent.ncols-self.ncols         + self.margin_x}
        
        anchor_pos_dict_y = {AnchorLayout.NEG: 0                                     + self.margin_y,
                            AnchorLayout.CENTER: (self.parent.nlines-self.nlines)//2 + self.margin_y,
                            AnchorLayout.POS: self.parent.nlines-self.nlines         + self.margin_y}
        
        x = anchor_pos_dict_x[self.anchor_layout_x]
        y = anchor_pos_dict_y[self.anchor_layout_y]

        return [x, y]

    def calc_size(self) -> tuple[int, int]:
        ncols = round(self.parent.ncols*self.anchor_x) - self.margin_x*2
        nlines = round(self.parent.nlines*self.anchor_y) - self.margin_y*2

        return [ncols, nlines]
    
    def resize(self):
        size = self.calc_size()
        pos = self.calc_pos()
        self.reshape(x = pos[0], y = pos[1], ncols = size[0], nlines = size[1])