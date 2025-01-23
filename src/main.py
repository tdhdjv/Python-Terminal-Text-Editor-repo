import sys

import curses

from utils.color import Color
from utils.color import ColorLibrary
from display import Screen
from display import AnchoredWindow
from display import AnchorLayout

def cmain(stdscr:"curses._CursesWindow") -> int:
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    curses.update_lines_cols()

    stdscr.nodelay(True)
    stdscr.clear()
    
    stdscr.bkgd(' ', ColorLibrary.pair_color(Color.parse("#fff"), Color.parse("#000")))

    screen = Screen(stdscr)
    header = AnchoredWindow(stdscr, screen, anchor_x = 1.0, anchor_y = 0.0, margin_bottom = 2, anchor_layout_y = AnchorLayout.NEG)
    footer = AnchoredWindow(stdscr, screen, anchor_x = 1.0, anchor_y = 0.0, margin_top = 2, anchor_layout_y = AnchorLayout.POS)
    
    header.text = 'HELLO'
    header.win.bkgdset(' ', ColorLibrary.pair_color(Color.parse("#fff"), Color.parse("#312A75")))
    footer.win.bkgdset(' ', ColorLibrary.pair_color(Color.parse("#fff"), Color.parse("#312A75")))
    #infinite loop
    while True:
        try:
            key = stdscr.get_wch()
            if key == 'q':
                return 0
            if key == curses.KEY_RESIZE:
                screen.resize()
        except curses.error:
            pass
        stdscr.clear()
        screen.render(False)
        stdscr.refresh()

def main() -> int:

    return curses.wrapper(cmain)

if __name__ == '__main__':
    sys.exit(main())