"""
The data structure is a list of previous lines and next lines.
"""

import phonemeKeyboard.phonemes
import pickle
import curses

class WindowedLines:
    """Stores the current line, previous lines, next lines, and the cursor position."""
    def __init__(self, cursor_position=0, window_size=(10,16)) -> None:
        self.curr_line = []
        self.cursor_position = cursor_position
        self.saved_cursor_x_position = cursor_position
        self.prev_lines= []
        self.next_lines = []

        self.window_size = window_size
        self.top_window_row = 0
        self.top_window_col = 0

        self.mark = None

        self.phoneme_mode = False
    
    def __repr__(self) -> str:
        return f"WindowedLines({self.curr_line=}, {self.cursor_position=})"

    def get_phoneme_mode(self) -> bool:
        return self.phoneme_mode
    
    def toggle_phoneme_mode(self):
        self.phoneme_mode = not self.phoneme_mode

    def update_window_cols(self) -> None:
        """Update the window's first column relative to the cursor."""
        if self.cursor_position > self.window_size[1]+self.top_window_col:
            self.top_window_col += self.cursor_position-(self.window_size[1]+self.top_window_col)
        elif self.cursor_position < self.top_window_col:
            self.top_window_col -= self.top_window_col-self.cursor_position
        while self.top_window_col > 0 and self.window_size[1] > self.cursor_position-self.top_window_col:
            self.top_window_col-=1

    def update_window_rows(self) -> None:
        """Update the window's first row relative to row-changing operations."""

        if self.top_window_row >= len(self.prev_lines):
            self.top_window_row = len(self.prev_lines)
        elif self.window_size[0] < len(self.prev_lines[self.top_window_row:])+len(self.next_lines[-(self.window_size[0]-len(self.prev_lines[self.top_window_row:])-1):])+1:
            self.top_window_row+=1
        

    def print_window(self) -> str:
        """Makes a string of the current window"""
        out=""
        prev_lines_window = self.prev_lines[self.top_window_row:]
        curr_line_and_cursor = [self.curr_line]
        next_lines_window = self.next_lines[-(self.window_size[0]-len(prev_lines_window)-1):][::-1]

        for line in prev_lines_window + curr_line_and_cursor + next_lines_window:
            windowed_line=''.join(line[self.top_window_col:])
            if len(windowed_line) > self.window_size[1]:
                windowed_line = windowed_line[:self.window_size[1]]
            else:
                while len(windowed_line) < self.window_size[1]:
                    windowed_line+=" "
            out+=(windowed_line+"\n")
        return out[:-1]
    
    def set_mark(self) -> None:
        self.mark = [len(self.prev_lines), self.cursor_position, self.curr_line]

    def clear_mark(self) -> None:
        self.mark = None

    def delete_region(self) -> None:
        if self.mark[0] > len(self.prev_lines):
            keep_right = self.mark[2][self.mark[1]:]
            while self.mark[0] > len(self.prev_lines):
                self.next_lines.pop()
                self.mark[0] -= 1
            self.curr_line = self.curr_line[:self.cursor_position] + keep_right

        if self.mark[0] < len(self.prev_lines):
            keep_left = self.mark[2][:self.mark[1]]
            while self.mark[0] < len(self.prev_lines):
                self.prev_lines.pop()
            self.curr_line = keep_left + self.curr_line[self.cursor_position:]

        else:
            if self.mark[1] > self.cursor_position:
                self.curr_line = self.curr_line[:self.cursor_position] + self.curr_line[self.mark[1]:]
            else:
                self.curr_line = self.curr_line[:self.mark[1]] + self.curr_line[self.cursor_position:]
        self.cursor_position = min(self.cursor_position, self.mark[1])
        self.mark = None


    def left(self) -> None:
        """Moves the cursor left by shifting the cursor position left."""
        if self.cursor_position > 0:
            self.cursor_position -= 1
        self.saved_cursor_x_position = self.cursor_position
        self.update_window_cols()

    def right(self) -> None:
        """Moves the cursor right by shifting the cursor position right."""
        if self.cursor_position < len(self.curr_line):
            self.cursor_position += 1
        self.saved_cursor_x_position = self.cursor_position
        self.update_window_cols()

    def up(self) -> None:
        """Moves the cursor up by retrieving the next line from next_lines."""
        if self.prev_lines:
            self.next_lines.append(self.curr_line)
            self.curr_line = self.prev_lines.pop()
            self.cursor_position = min(len(self.curr_line), self.saved_cursor_x_position)
        else:
            self.cursor_position = 0
        
        self.update_window_cols()
        self.update_window_rows()

    def down(self) -> None:
        """Moves the cursor down by retrieving the previous lines from prev_lines."""
        if self.next_lines:
            self.prev_lines.append(self.curr_line)
            self.curr_line = self.next_lines.pop()
            self.cursor_position = min(len(self.curr_line), self.saved_cursor_x_position)
        else:
            self.cursor_position = len(self.curr_line)
        self.update_window_cols()
        self.update_window_rows()

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in prev_lines."""
        if self.mark:
            self.delete_region()

        if char == '\n':
            self.prev_lines.append(self.curr_line[:self.cursor_position])
            self.curr_line = self.curr_line[self.cursor_position:]
            self.cursor_position = 0
        else:
            if len(self.curr_line) <= self.cursor_position:
                self.curr_line.append(char)
            else:
                self.curr_line = self.curr_line[:self.cursor_position] + [char] + self.curr_line[self.cursor_position:]
                self.curr_line[self.cursor_position] = char

            self.cursor_position += 1
        self.saved_cursor_x_position = self.cursor_position
        self.update_window_cols()
        self.update_window_rows()

    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        if self.mark:
            self.delete_region()
            return
        
        if self.cursor_position == 0:
            if self.prev_lines:
                prev_line = self.prev_lines.pop()
                self.curr_line = prev_line + self.curr_line
                self.cursor_position = len(prev_line)
        else:
            self.curr_line = self.curr_line[:self.cursor_position-1] + self.curr_line[self.cursor_position:]
            self.cursor_position -= 1
        self.saved_cursor_x_position = self.cursor_position
        self.update_window_cols()
        self.update_window_rows()

    def write_file(self, file_name:str) -> None:
        f = open(file_name ,"w", encoding="UTF-8")
        for line in self.prev_lines:
            f.write(''.join(line)+'\n')
        f.write(''.join(self.curr_line))
        if self.next_lines:
            f.write('\n')
        for line in self.next_lines[::-1]:
            f.write(''.join(line)+'\n')
        f.close()

    def read_file(self, file_name:str) -> None:
        if not file_name:
            return
        try:
            f = open(file_name ,"r", encoding="UTF-8")
            lines = f.readlines()
            lines = [l.translate({ord('\n'): None}) for l in lines]
        except FileNotFoundError:
            f = open(file_name, "x", encoding="UTF-8")
            lines = []
        if lines:
            self.curr_line, self.next_lines = list(lines[0]), [list(l) for l in lines[1:]][::-1]
        else:
            self.curr_line, self.next_lines = [], []
        self.prev_lines = []

        self.cursor_position = self.top_window_col = self.top_window_row = 0

class View:
    def __init__(self):
        self.window:curses.window = None
        self.keypad = False
        self.phoneme_panel:curses.window = None

    def run(self):
        self.window = curses.initscr()
    
    def get_window_size(self) -> tuple[int]:
        return (self.window.getmaxyx()[0],self.window.getmaxyx()[1]-1)

    def toggle_panel(self, model:WindowedLines) -> curses.window:
        if model.get_phoneme_mode():
            self.phoneme_panel = self.window.subwin(self.window.getmaxyx()[0]-5, 0)
            self.phoneme_panel.refresh()
        else:
            self.phoneme_panel = None
        return self.phoneme_panel
    
    def getch(self) -> int:
        return self.window.getch()

    def add_str_to_window(self, text:str):
        self.window.addstr(text)
        self.window.refresh()

    def toggle_keypad(self):
        self.keypad = not self.keypad
        self.window.keypad(self.keypad)

    def update_panel(self, text:str):
        if self.phoneme_panel:
            self.phoneme_panel.addstr(text)
            self.phoneme_panel.refresh()

    def update(self, model:WindowedLines, panel_text:str):
        self.window.erase()
        self.window.addstr(model.print_window())
        self.window.move(len(model.prev_lines)-model.top_window_row,min(model.cursor_position, model.window_size[1]))
        self.window.refresh()
        self.update_panel(text=panel_text)

class Controller:
    """The connection between the model and the view"""
    def __init__(self, model:WindowedLines, view:View):
        self.model = model
        self.view = view

    def run(self, filename:str=""):
        "the loop connecting the model to user input, displayed using a curses view."
        self.view.toggle_keypad()
        curses.noecho()
        curses.cbreak()
        curses.raw()
        with open('saved_dictionary.pkl', 'rb') as f:
            word_dict = pickle.load(f)

        self.model.read_file(filename)
        self.view.add_str_to_window(self.model.print_window())

        char_stream = phonemeKeyboard.phonemes.KeypadCharStream(view=self.view)
        phoneme_stream = phonemeKeyboard.phonemes.PhonemeStream(charstream=char_stream)
        word_stream = phonemeKeyboard.phonemes.WordStream(phonemestream=phoneme_stream, dictionary=word_dict)

        while True:
            if self.model.get_phoneme_mode():
                key_input = ord(word_stream.get())
            else:
                key_input = self.view.getch()

            if key_input == curses.KEY_LEFT:
                self.model.left()
            elif key_input == curses.KEY_RIGHT:
                self.model.right()
            elif key_input == curses.KEY_ENTER:
                self.model.insert('\n')
            elif key_input == curses.KEY_BACKSPACE:
                self.model.delete()
            elif key_input == curses.KEY_UP:
                self.model.up()
            elif key_input == curses.KEY_DOWN:
                self.model.down()
            elif key_input == curses.KEY_F2:
                if not self.model.mark:
                    self.model.set_mark()
                else:
                    self.model.clear_mark()
            elif key_input == 9: # TAB
                for _ in range(4):
                    self.model.insert(' ')
            elif key_input == 19: # CTRL+S
                self.model.write_file(filename)
            elif key_input == 16: # CTRL+P
                self.model.toggle_phoneme_mode()
                self.view.toggle_panel(self.model)
            elif key_input == 3: # CTRL+C
                break
            else:
                self.model.insert(chr(key_input))

            self.view.update(model=self.model, panel_text=word_stream.get_phoneme_data())

        curses.nocbreak()
        self.view.toggle_keypad()
        curses.echo()
        curses.endwin()
        