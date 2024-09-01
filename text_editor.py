"""
The data structure is a list of previous lines and next lines.
"""

import curses

class Lines:
    """Stores the current line, previous lines, next lines, and the cursor position."""
    def __init__(self, cursor_position=0) -> None:
        self.curr_line = []
        self.cursor_position = cursor_position
        self.prev_lines= []
        self.next_lines = []

    def left(self) -> None:
        """Moves the cursor left by shifting the cursor position left."""
        if self.cursor_position > 0:
            self.cursor_position -= 1

    def right(self) -> None:
        """Moves the cursor right by shifting the cursor position right."""
        if self.cursor_position < len(self.curr_line):
            self.cursor_position += 1

    def up(self) -> None:
        """Moves the cursor up by retrieving the next line from next_lines."""
        if self.prev_lines:
            self.next_lines.append(self.curr_line)
            self.curr_line = self.prev_lines.pop()
            self.cursor_position = min(len(self.curr_line), self.cursor_position)
        else:
            self.cursor_position = 0

    def down(self) -> None:
        """Moves the cursor down by retrieving the previous lines from prev_lines."""
        if self.next_lines:
            self.prev_lines.append(self.curr_line)
            self.curr_line = self.next_lines.pop()
            self.cursor_position = min(len(self.curr_line), self.cursor_position)
        else:
            self.cursor_position = len(self.curr_line)

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in prev_lines."""
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

    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        if self.cursor_position == 0:
            if self.prev_lines:
                prev_line = self.prev_lines.pop()
                self.curr_line = prev_line + self.curr_line
                self.cursor_position = len(prev_line)
        else:
            self.curr_line = self.curr_line[:self.cursor_position-1] + self.curr_line[self.cursor_position:]
            self.cursor_position -= 1

class WindowedLines:
    """
    The model for the text editor. Takes a lines class and adds a window.
    API supports up/down/left/right movement of cursor and insert/delete.
    TODO: Add highlighting.
    """

    def __init__(self, window_size=(10,16)) -> None:
        self.lines = Lines()

        self.window_size = window_size
        self.top_window_row = 0
        self.top_window_col = 0

    def update_window_cols(self) -> None:
        """Update the window's first column relative to the cursor."""
        if self.lines.cursor_position > self.window_size[1]+self.top_window_col:
            self.top_window_col += self.lines.cursor_position-(self.window_size[1]+self.top_window_col)
        elif self.lines.cursor_position < self.top_window_col:
            self.top_window_col -= self.top_window_col-self.lines.cursor_position
        while self.top_window_col > 0 and self.window_size[1] > self.lines.cursor_position-self.top_window_col:
            self.top_window_col-=1

    def update_window_rows(self) -> None:
        """Update the window's first row relative to row-changing operations."""

        if self.top_window_row > len(self.lines.prev_lines):
            self.top_window_row = len(self.lines.prev_lines)
        elif self.window_size[0] < len(self.lines.prev_lines[self.top_window_row:])+len(self.lines.next_lines[:self.window_size[0]-self.top_window_row-1])+1:
            self.top_window_row+=1

    def print_window(self) -> str:
        """Makes a string of the current window"""
        out=""
        prev_lines_window = self.lines.prev_lines[self.top_window_row:]
        curr_line_and_cursor = [self.lines.curr_line]
        next_lines_window = self.lines.next_lines[:self.window_size[0]-self.top_window_row-1]

        for line in prev_lines_window + curr_line_and_cursor + next_lines_window:
            windowed_line=''.join(line[self.top_window_col:])
            if len(windowed_line) > self.window_size[1]:
                windowed_line = windowed_line[:self.window_size[1]]
            else:
                while len(windowed_line) < self.window_size[1]:
                    windowed_line+=" "
            out+=(windowed_line+"\n")
        return out[:-1]


    def right(self) -> None:
        """Moves the cursor right by shifting the cursor position right."""
        self.lines.right()
        self.update_window_cols()

    def left(self) -> None:
        """Moves the cursor left by shifting the cursor position left."""
        self.lines.left()
        self.update_window_cols()

    def up(self) -> None:
        """Moves the cursor up by retrieving the next line from next_lines."""
        self.lines.up()
        self.update_window_cols()
        self.update_window_rows()

    def down(self) -> None:
        """Moves the cursor down by retrieving the previous lines from prev_lines."""
        self.lines.down()
        self.update_window_cols()
        self.update_window_rows()

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in prev_lines."""
        self.lines.insert(char)
        self.update_window_cols()
        self.update_window_rows()

    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        self.lines.delete()
        self.update_window_cols()
        self.update_window_rows()

    # def write_file(self, file_name:str) -> None:
    #     f = open(file_name ,"w", encoding="UTF-8")
    #     f.write(f"{self.lines.cursor_position}\n{self.lines.prev_id}\n{self.lines.next_id}\n{self.lines.curr_id}\n{self.lines.iterator}\n{self.lines.dict}\n{self.lines.curr_line}\n{self.top_window_row}\n{self.top_window_col}\n")
    #     f.close()

    # def read_file(self, file_name:str) -> None:
    #     with open(file_name ,"r", encoding="UTF-8") as f:
    #         params = f.readlines()
    #     try:
    #         next_id = int(params[2])
    #     except ValueError:
    #         next_id = None
    #     try:
    #         prev_id = int(params[1])
    #     except ValueError:
    #         prev_id = None

    #     self.lines.cursor_position=int(params[0])
    #     self.lines.prev_id=prev_id
    #     self.lines.next_id=next_id
    #     self.lines.curr_id=int(params[3])
    #     self.lines.iterator=int(params[4])
    #     self.lines.dict = eval(params[5])
    #     self.lines.curr_line = list(params[6])
    #     self.top_window_row = int(params[7])
    #     self.top_window_col = int(params[8])

class Controller:
    """The connection between the model and the view"""
    def __init__(self, model:WindowedLines=WindowedLines(),view=curses.initscr()):
        self.model = model
        self.view = view

    def run(self, filename:str=""):
        "the loop connecting the model to user input, displayed using a curses view."
        self.view.keypad(True)
        curses.noecho()
        curses.cbreak()

        if filename != "":
            self.model.read_file(filename)
            self.view.addstr(self.model.print_window())
        else:
            self.view.addstr("")
        
        self.view.refresh()

        while True:
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
                break
            else:
                self.model.insert(chr(key_input))

            self.view.erase()
            self.view.addstr(self.model.print_window())
            self.view.refresh()

        curses.nocbreak()
        self.view.keypad(False)
        curses.echo()
        curses.endwin()

def main():
    controller = Controller()
    controller.run()

if __name__ == "__main__":
    main()