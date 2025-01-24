from __future__ import annotations
from enum import Enum

import curses

from .window import Window

class AnchorLayout(Enum):
    NEG = 0
    CENTER = 1
    POS = 2

#window but you can use anchors so that the screen is resize accordingly
class AnchoredWindow (Window):
    def __init__(self, parent:Window, anchor_x:float = 0.0, anchor_y:float = 0.0,
                margin_left:int = 0, margin_right:int = 0, margin_top:int = 0, margin_bottom:int = 0,
                  anchor_layout_x:AnchorLayout = AnchorLayout.CENTER, anchor_layout_y:AnchorLayout = AnchorLayout.CENTER) -> None:
        
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom

        self.anchor_layout_x = anchor_layout_x
        self.anchor_layout_y = anchor_layout_y

        self._parent = parent

        size = self.calc_size()

        self._no_marg_ncols = size[0] - (self.margin_right + self.margin_left)
        self._no_marg_nlines = size[1] - (self.margin_bottom + self.margin_top)

        self._ncols = size[0]
        self._nlines = size[1]

        pos = self.calc_pos()

        self.x = pos[0]
        self.y = pos[1]

        super().__init__(parent, x = self.x, y = self.y, ncols = self._ncols, nlines = self._nlines)

    def calc_pos(self) -> tuple[int, int]:
        x = 0
        y = 0

        parent_ncols = self._parent._ncols
        parent_nlines = self._parent._nlines

        anchor_pos_dict_x = {AnchorLayout.NEG: 0                                          - self.margin_left,
                            AnchorLayout.CENTER: (parent_ncols  - self._no_marg_ncols)//2 - self.margin_left,
                            AnchorLayout.POS: parent_ncols - self._no_marg_ncols          - self.margin_left}
        
        anchor_pos_dict_y = {AnchorLayout.NEG: 0                                           - self.margin_top,
                            AnchorLayout.CENTER: (parent_nlines - self._no_marg_nlines)//2 - self.margin_top,
                            AnchorLayout.POS: parent_nlines - self._no_marg_nlines         - self.margin_top}
        
        x = anchor_pos_dict_x[self.anchor_layout_x]
        y = anchor_pos_dict_y[self.anchor_layout_y]

        return [x, y]

    def calc_size(self) -> tuple[int, int]:
        parent_ncols = self._parent._ncols
        parent_nlines = self._parent._nlines
            
        ncols = int(parent_ncols*self.anchor_x) + self.margin_right + self.margin_left
        nlines = int(parent_nlines*self.anchor_y) + self.margin_top + self.margin_bottom

        return [ncols, nlines]
    
    def resize(self):
        size = self.calc_size()
        self._ncols = size[0]
        self._nlines = size[1]

        self._no_marg_ncols = size[0] - (self.margin_right + self.margin_left)
        self._no_marg_nlines = size[1] - (self.margin_bottom + self.margin_top)

        pos = self.calc_pos()

        self.x = pos[0]
        self.y = pos[1]

        self.reshape(x = self.x, y = self.y, ncols = self._ncols, nlines = self._nlines)
        for child in self.children:
            child.resize()

    def change_margin(self, margin_left:int|None = None, margin_right:int|None= None, margin_top:int|None= None, margin_bottom:int|None= None):
        if margin_left != None:
            self.margin_left = margin_left
        if margin_right != None:
            self.margin_right = margin_right
        if margin_top != None:
            self.margin_top = margin_top
        if margin_bottom != None:
            self.margin_bottom = margin_bottom
        self.resize()