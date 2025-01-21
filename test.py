import sys

import curses

def cmain(stdsrc:"curses._CursesWindow") -> int:
    a1 = stdsrc.subwin(10,10, 0,0)
    a2 = a1.subwin(20, 20, 0, 0)
    a2.addch(20,20,'a')
    stdsrc.get_wch()
    return 0

def main() -> int:
    return curses.wrapper(cmain)

if __name__ == '__main__':
    sys.exit(main())