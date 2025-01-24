import curses

from utils.color import Color
from utils.color import ColorLibrary
from display.anchored_window import AnchoredWindow
from display.anchored_window import AnchorLayout
from utils import text_manager as txtman

class TextDisplay(AnchoredWindow) :

    def __init__(self, parent, **kwargs) -> None:
        self.scroll_x = 0
        self.scroll_y = 0

        self.NUMBER_DISPLAY_COLS = 5

        super().__init__(parent, **kwargs)

        self.body = AnchoredWindow(self, anchor_x=1.0, anchor_y=1.0, anchor_layout_x=AnchorLayout.POS, margin_left=-self.NUMBER_DISPLAY_COLS)
        self.line_num = AnchoredWindow(self, anchor_x=0.0, anchor_y=1.0, anchor_layout_x=AnchorLayout.NEG, margin_right=self.NUMBER_DISPLAY_COLS)
        self.line_num.win.bkgd(' ', ColorLibrary.pair_color(Color.parse("#888"), Color.parse("#111")))

    def render(self, debug=False) -> None:
        if self._ncols == 0 or self._nlines == 0:
            return
        
        #display the numbers
        start_num = self.body.scroll_y+1
        end_num = txtman.get_line_count(self.body.text)
        amount = end_num-start_num + 1
        for i in range(min(self.line_num._nlines, amount)):
            self.line_num.add_str(str(start_num+i), x=self.NUMBER_DISPLAY_COLS-len(str(start_num+i))-1, y=i)
            #idk why this throws an error but fuck it
            try:
                self.line_num.add_char(curses.ACS_VLINE, x=self.NUMBER_DISPLAY_COLS-1, y=i)
            except:
                pass
        super().render(debug)
