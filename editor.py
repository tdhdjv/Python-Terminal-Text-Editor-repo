import command
from text_display import TextDisplay
from footer import Footer

import curses, sys
import os
from curses import wrapper, window

class EditorMode:
    INSERT = 0
    COMMAND = 1

class Editor :
    def __init__(self) -> None:
        self.mode = EditorMode.COMMAND
        self.filepath = ''
        self.saved = True
        self.running = True

    def do_insert_mode(self):
        self.command_display.display_text("INSERT")
        self.text_display.display()
        key = self.text_display.get_key()

        if key == '\x1b':
            self.mode = EditorMode.COMMAND
        elif key == '\x13':
            command.call('save', self)
        else:
            self.text_display.edit_text(key)
            self.saved = False
     
    def do_command_mode(self):
        keywords = self.command_display.ask_question("COMMAND").split()
        try:
            command_name = keywords[0]
            args = keywords[1:]
            args.insert(0, self)
            command.call(command_name, *args)
        except:
            pass

    def run(self, stdscr:window) -> None:
        #colors
        curses.start_color()
        curses.use_default_colors()
        
        curses.init_pair(1, curses.COLOR_WHITE, 236)
        curses.init_pair(2, curses.COLOR_WHITE, 233)
        curses.init_pair(3, curses.COLOR_BLACK, 30)
        curses.init_pair(4, 248, -1)

        #clear the screen
        stdscr.clear()

        #initialize text display
        self.file_path_display = stdscr.subwin(1, curses.COLS-1, 0, 0)
        self.text_display = TextDisplay(curses.LINES-4, curses.COLS-1, 1, stdscr)
        self.command_display = Footer(curses.LINES-1, curses.COLS-1, 1, stdscr)

        self.text_display.display()
        self.command_display.display_text("DEFAULT")

        self.file_path_display.addstr('new')
        self.file_path_display.bkgd(' ', curses.color_pair(1))
        self.file_path_display.refresh()  
        
        while self.running:
            if self.mode == EditorMode.INSERT:
                self.do_insert_mode()       
            if self.mode == EditorMode.COMMAND:
                self.do_command_mode()
            
            self.file_path_display.clear()
            displayed_string = self.filepath
            if displayed_string == '':
                displayed_string = "new"
            if not self.saved:
                displayed_string += '*'
            
            self.file_path_display.addstr(displayed_string)
            self.file_path_display.bkgd(' ', curses.color_pair(1))
            self.file_path_display.refresh()  
    @command.command('q')
    def q(self) :
        if not self.saved:
            while True:
                answer = self.command_display.ask_question(f'Save Changes made in {self.filepath} [Y/n]')
                if answer.lower() == 'n':
                    break
                if answer.lower() == 'y':
                    if self.filepath == '':
                        answer = self.command_display.ask_question("ENTER FILEPATH")
                        self.filepath = answer
                    with open(self.filepath, 'w') as f:
                        f.write(self.text_display.text)
                    break
        self.running = False

    @command.command('quit')
    def quit(self) :
        if not self.saved:
            while True:
                answer = self.command_display.ask_question(f'Save Changes made in {self.filepath} [Y/n]')
                if answer.lower() == 'n':
                    break
                if answer.lower() == 'y':
                    if self.filepath == '':
                        answer = self.command_display.ask_question("ENTER FILEPATH")
                        self.filepath = answer
                    with open(self.filepath, 'w') as f:
                        f.write(self.text_display.text)
                    break
        self.running = False

    @command.command('save')
    def save(self) :
        if self.filepath == '':
            answer = self.command_display.ask_question("ENTER FILEPATH")
            self.filepath = answer
        with open(self.filepath, 'w') as f:
            f.write(self.text_display.text)
            self.saved = True

    @command.command('new')
    def new(self) :
        if not self.saved:
            while True:
                answer = self.command_display.ask_question(f'Save Changes made in {self.filepath} [Y/n]')
                if answer.lower() == 'n':
                    break
                if answer.lower() == 'y':
                    if self.filepath == '':
                        answer = self.command_display.ask_question("ENTER FILEPATH")
                        self.filepath = answer
                    with open(self.filepath, 'w') as f:
                        f.write(self.text_display.text)
                    break
        self.filepath = ''
        self.text_display.text = ''
        self.text_display.display()
        self.saved = True
        self.mode = EditorMode.INSERT

    @command.command('load')
    def load(self, filepath) :
        if not os.path.exists(filepath):
            return
        if not self.saved:
            while True:
                answer = self.command_display.ask_question(f'Save Changes made in {self.filepath} [Y/n]')
                if answer.lower() == 'n':
                    break
                if answer.lower() == 'y':
                    if self.filepath == '':
                        answer = self.command_display.ask_question("ENTER FILEPATH")
                        self.filepath = answer
                    with open(self.filepath, 'w') as f:
                        f.write(self.text_display.text)
                    break
        self.filepath = filepath
        with open(self.filepath) as f:
            self.text_display.text = f.read()
            self.text_display.display()
        self.saved = True
        self.mode = EditorMode.INSERT

    @command.command('save_as')
    def save_as(self, filepath):
        self.filepath = filepath

        if os.path.exists(filepath):
            while True:
                answer = self.command_display.ask_question(f"OVERRIDE EXISTING FILE {filepath}? [Y/n]")
                if answer.lower() == 'n':
                    break
                if answer.lower() == 'y':
                    self.save()
                    break
        with open(self.filepath, 'w') as f:
            f.write(self.text_display.text)
            self.saved = True

    @command.command('i')
    def i(self):
        self.mode = EditorMode.INSERT

    @command.command('insert')
    def insert(self):
        self.mode = EditorMode.INSERT

editor = Editor()
wrapper(editor.run)