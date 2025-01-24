import sys

import curses

from editor import Editor

def cmain(stdscr:"curses._CursesWindow") -> int:
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    editor = Editor()
    editor.run(stdscr)
    

def main() -> int:
    return curses.wrapper(cmain)

if __name__ == '__main__':
    sys.exit(main())