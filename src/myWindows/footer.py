import curses

from utils.color import Color
from utils.color import ColorLibrary
from display.anchored_window import AnchoredWindow
from display.anchored_window import AnchorLayout
from utils import text_manager as txtman
from cursor import Cursor

class Footer(AnchoredWindow):
    def __init__(self, parent, **kwargs) -> None:
        self.active = False
        super().__init__(parent, **kwargs)
        self.title = AnchoredWindow(self, anchor_layout_x=AnchorLayout.NEG, anchor_y=1.0, anchor_x=0.0, margin_right=1)
        self.prompt = AnchoredWindow(self, anchor_layout_x=AnchorLayout.POS, anchor_y=1.0, anchor_x=1.0, margin_left=-1)

    def change_question(self, question:str):
        string = f"[{question}]"
        self.title.change_margin(margin_right=len(string)+1)
        self.prompt.change_margin(margin_left=-len(string)-1)

        self.title.text = string

    def ask_question(self, key:str) -> str:
        if key == '\n':
            return self.prompt.text
        else:
            self.prompt.edit_text(key)

