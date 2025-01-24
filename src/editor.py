from enum import Enum

import curses

from utils import command
from utils.color import Color
from utils.color import ColorLibrary
from display.screen import Screen
from display.anchored_window import AnchoredWindow
from display.anchored_window import AnchorLayout
from myWindows.text_display import TextDisplay
from myWindows.footer import Footer

class EditorMode(Enum):
    DEFAULT = 0
    INSERT = 1
    COMMAND = 2
    ENTER_FILE_PATH = 3

class Editor:
    def __init__(self) -> None:
        self.mode = -1
        self.filepath = ''
        self.saved = True
        self.running = True

    def run(self, stdscr:'curses._CursesWindow'):
        stdscr.bkgd(' ', ColorLibrary.pair_color(Color.parse("#fff"), Color.parse("#000")))
        screen = Screen(stdscr)
        self.stdscr = stdscr
        self.header = AnchoredWindow(screen, anchor_x = 1.0, anchor_y = 0.0, margin_bottom=1, anchor_layout_y = AnchorLayout.NEG)
        self.footer = Footer(screen, anchor_x = 1.0, anchor_y = 0.0, margin_top=1, anchor_layout_y = AnchorLayout.POS)
        self.text_display = TextDisplay(screen, anchor_x = 1.0, anchor_y = 1.0, margin_top=-1, margin_bottom = -1, anchor_layout_y = AnchorLayout.CENTER)

        self.header.win.bkgd(' ', ColorLibrary.pair_color(Color.parse("#fff"), Color.parse("#312A75")))
        self.footer.win.bkgd(' ', ColorLibrary.pair_color(Color.parse("#fff"), Color.parse("#333")))
        self.text_display.win.bkgd(' ', ColorLibrary.pair_color(Color.parse("#888"), Color.parse("#111")))
        
        self.switch_EditorMode(EditorMode.INSERT)

        #infinite loop
        while self.running:
            screen.clear()
            string = 'new'
            if self.filepath:
                string = self.filepath
            if not self.saved:
                string = '*'+string
            self.header.text = string
            stdscr.refresh()
            screen.render()
            
            key = stdscr.getkey()
            if key == 'KEY_RESIZE':
                screen.resize()
            elif self.mode == EditorMode.DEFAULT:
                self.do_default_mode(key)
            elif self.mode == EditorMode.INSERT:
                self.do_insert_mode(key)
            elif self.mode == EditorMode.COMMAND:
                self.do_command_mode(key)
            elif self.mode == EditorMode.ENTER_FILE_PATH:
                self.do_enter_file_path_mode(key)

        return 0
    
    def do_enter_file_path_mode(self, key:str):
        if key == '\x1b':
            self.switch_EditorMode(EditorMode.DEFAULT)
            self.footer.change_question("FAILED TO SAVE")
        else:
            answer = self.footer.ask_question(key)
            if answer:
                self.filepath = answer
                command.call('s', self)
                self.switch_EditorMode(EditorMode.COMMAND)

    def do_default_mode(self, key:str):
        if key == 'i':
            self.switch_EditorMode(EditorMode.INSERT)
        elif key == ':':
            self.switch_EditorMode(EditorMode.COMMAND)
    
    def do_command_mode(self, key:str):
        if key == '\x1b':
            self.switch_EditorMode(EditorMode.DEFAULT)
        else:
            self.footer.change_question('COMMAND')
            answer = self.footer.ask_question(key)
            if answer:
                command_name, keyword = self.parse_answer(answer)
                #try to call command and if it doesn't exist show "INVALID COMMAND"
                try:
                    command.call(command_name, *keyword)
                except (TypeError, KeyError):
                    self.footer.change_question("INVALID COMMAND!")
                self.footer.prompt.text = ''
                    
        if self.footer.prompt.text == '' and self.mode == EditorMode.COMMAND:
            self.switch_EditorMode(EditorMode.DEFAULT)

    def do_insert_mode(self, key:str):
        if key == '\x1b':
            self.switch_EditorMode(EditorMode.DEFAULT)
        else:
            self.text_display.body.edit_text(key)
            self.saved = False

    def switch_EditorMode(self, editor_mode:EditorMode):
        self.mode = editor_mode
        self.text_display.body.active = False
        self.footer.prompt.text = ''
        self.footer.prompt.active = False

        if self.mode == EditorMode.INSERT:
            self.footer.change_question('INSERT')
            self.text_display.body.active = True
        elif self.mode == EditorMode.COMMAND:
            self.footer.change_question('COMMAND')
            self.footer.prompt.active = True
            self.footer.prompt.edit_text(":")
        elif self.mode == EditorMode.DEFAULT:
            self.footer.change_question('DEFAULT')
        elif self.mode == EditorMode.ENTER_FILE_PATH:
            self.footer.change_question('ENTER FILEPATH')
            self.footer.prompt.active = True
    
    def parse_answer(self, answer:str) -> tuple[str, tuple]:
        answer = answer.removeprefix(':')
        words = answer.split()
        if len(words) == 0:
            return '', ''
        command_name = words[0]
        keywords = words[1:]
        keywords.insert(0, self)
        return command_name, keywords

    @command.command('q', 'quit')
    def quit(self):
        self.running = False

    @command.command('w','write', 's', 'save')
    def save(self):
        #try to save in file path
        if self.filepath:
            with open(self.filepath, 'w') as f:
                f.write(self.text_display.body.text)
                self.saved = True
        else:
            self.switch_EditorMode(EditorMode.ENTER_FILE_PATH)

    @command.command('l', 'load', 'r', 'read')
    def load(self, filepath):
        self.filepath = filepath
        if self.filepath:
            with open(self.filepath, 'r') as f:
                self.text_display.body.text = f.read()
                self.saved = True
        self.switch_EditorMode(EditorMode.INSERT)
        
    @command.command('n', 'new')
    def load(self):
        self.filepath = ''
        self.saved = True
        self.text_display.body.text = ''
        self.switch_EditorMode(EditorMode.INSERT)