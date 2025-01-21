import sys

import curses

from display.screen import Screen
from display.window import Window
from display.anchored_window import AnchoredWindow

def cmain(stdsrc:"curses._CursesWindow") -> int:
    screen = Screen(stdsrc)
    screen.add_window(AnchoredWindow(screen, anchor_x = 1.0, anchor_layout_y = 1.0))
    screen.render()
    while True:
        key = stdsrc.get_wch()
        if key == 'q':
            return 0
        if key == curses.KEY_RESIZE:
            screen.resize()

def main() -> int:
    return curses.wrapper(cmain)

if __name__ == '__main__':
    sys.exit(main())