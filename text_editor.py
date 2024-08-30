"""
The data structure is a dictionary of text lines with pointers to the previous and next line. 
For example, the string:

0 "Hello, 
1  World!"

will be stored as:
{ 0: [['H','e','l','l','o',','], None, 1], 
  1: [['W','o','r','l','d','!'], 0, None]}

As new lines and text get added and removed, the data structure updates accordingly.
"""

import curses

class Lines:
    """Stores the text, the previous id, and the next id of each line."""
    def __init__(self, cursor_position=0,prev_id=None, next_id=None,
                 curr_id=0, iterator=1) -> None:
        self.dict = {}
        self.curr_line = []
        self.cursor_position = cursor_position

        # ids are keys for each stored line.
        self.curr_id = curr_id # the id for the current line being manipulated.
        self.prev_id = prev_id # the id for the previous line.
        self.next_id = next_id # the id for the next line.

        self.iterator = iterator # Allocates monotonically increasing identifiers to guarantee new ids are unique.

    def left(self) -> None:
        """Moves the cursor left by shifting the cursor position left."""
        if self.cursor_position > 0:
            self.cursor_position -= 1

    def right(self) -> None:
        """Moves the cursor right by shifting the cursor position right."""
        if self.cursor_position < len(self.curr_line):
            self.cursor_position += 1
    
    def up(self) -> None:
        """Moves the cursor up by retrieving the data for prev_id and 
        updating relevant fields."""
        if self.prev_id is not None:
            [prev_line, prev_prev_id, prev_next_id] = self.dict[self.prev_id]
            self.curr_id = self.prev_id
            self.curr_line = prev_line
            self.cursor_position = min(len(prev_line), self.cursor_position)
            self.prev_id = prev_prev_id
            self.next_id = prev_next_id
        else:
            self.cursor_position = 0

    def down(self) -> None:
        """Moves the cursor down by retrieving the data for next_id and 
        updating relevant fields."""
        if self.next_id is not None:
            [next_line, next_prev_id, next_next_id] = self.dict[self.next_id]
            self.curr_id = self.next_id
            self.curr_line = next_line
            self.cursor_position = min(len(next_line), self.cursor_position)
            self.prev_id = next_prev_id
            self.next_id = next_next_id
        else:
            self.cursor_position = len(self.curr_line)

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in lines and create a 
        new id for the current line."""
        if char == '\n':
            self.dict[self.curr_id] = [self.curr_line[:self.cursor_position],self.prev_id,self.iterator]
            self.curr_line = self.curr_line[self.cursor_position:]
            self.cursor_position = 0
            self.prev_id = self.curr_id

            if self.next_id in self.dict:
                self.dict[self.next_id] = [self.dict[self.next_id][0], self.iterator, self.dict[self.next_id][2]]
            self.dict[self.iterator] = [self.curr_line, self.prev_id, self.next_id]
            self.curr_id = self.iterator
            self.iterator += 1
        else:
            if len(self.curr_line) <= self.cursor_position:
                self.curr_line.append(char)
            else:
                self.curr_line[self.cursor_position] = char

            self.cursor_position += 1
            self.dict[self.curr_id] = [self.curr_line, self.prev_id, self.next_id]

    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        if self.cursor_position == 0:
            if self.prev_id is not None:
                [prev_line, prev_prev_id, _] = self.dict.pop(self.prev_id)
                self.curr_line = prev_line+self.curr_line
                self.cursor_position = len(prev_line)
                self.prev_id = prev_prev_id
                if self.prev_id in self.dict:
                    self.dict[self.prev_id] = [self.dict[self.prev_id][0], self.dict[self.prev_id][1], self.curr_id]
        else:
            self.curr_line = self.curr_line[:self.cursor_position-1] + self.curr_line[self.cursor_position:]
            if self.cursor_position > 0:
                self.cursor_position -= 1
        self.dict[self.curr_id] = [self.curr_line, self.prev_id, self.next_id]

class WindowedLines:
    """
    The model for the text editor. Takes a lines class and adds a window.
    API supports up/down/left/right movement of cursor and insert/delete.
    TODO: Add highlighting.
    """

    # window update constants:
    UP = 0
    DOWN = 1
    INSERT = 2
    DELETE = 3

    def __init__(self, window_size=(10,16)) -> None:
        self.lines = Lines()

        self.window_size = window_size
        self.top_window_row = self.lines.curr_id
        self.top_window_col = 0

    def update_window_cols(self) -> None:
        """Update the window's first column relative to the cursor."""
        if self.lines.cursor_position == 0:
            self.top_window_col = 0
        if self.lines.cursor_position > self.window_size[1]+self.top_window_col:
            self.top_window_col+=1
        elif self.lines.cursor_position < self.top_window_col:
            self.top_window_col-=1

    def update_window_rows(self, operation=None) -> None:
        """Update the window's first row relative to row-changing operations."""
        if operation == self.UP:
            if self.lines.next_id == self.top_window_row:
                self.top_window_row = self.lines.curr_id
        elif operation in [self.INSERT,self.DOWN]:
            tmp = self.top_window_row
            for _ in range(self.window_size[0]-1):
                if tmp is None or self.lines.dict[tmp][2] is None or tmp == self.lines.curr_id:
                    return
                tmp = self.lines.dict[tmp][2]
            if tmp != self.lines.curr_id:
                self.top_window_row = self.lines.dict[self.top_window_row][2]
        elif operation == self.DELETE:
            if not self.top_window_row in self.lines.dict:
                self.top_window_row = self.lines.curr_id
        else:
            raise ValueError()


    def print_window(self) -> str:
        """Makes a string of the current window"""
        out=""
        iterate_row = self.top_window_row
        iterate_col = self.top_window_col
        for _ in range(self.window_size[0]):
            for i in range(iterate_col, iterate_col+self.window_size[1]):
                if iterate_row in self.lines.dict and i in range(len(self.lines.dict[iterate_row][0])):
                    out+=self.lines.dict[iterate_row][0][i]
                else:
                    out+=" "
                if iterate_row == self.lines.curr_id and self.lines.cursor_position == i:
                    out = out[:-1]
                    out+=chr(219)
            if iterate_row in self.lines.dict:
                iterate_row = self.lines.dict[iterate_row][2]
            out +="\n"
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
        """Moves the cursor up by retrieving the data for prev_id and 
        updating relevant fields."""
        self.lines.up()
        self.update_window_cols()
        self.update_window_rows(self.UP)

    def down(self) -> None:
        """Moves the cursor down by retrieving the data for next_id and 
        updating relevant fields."""
        self.lines.down()
        self.update_window_cols()
        self.update_window_rows(self.DOWN)

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in lines and create a 
        new id for the current line."""
        self.lines.insert(char)
        self.update_window_cols()
        self.update_window_rows(self.INSERT)

    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        self.lines.delete()
        self.update_window_cols()
        self.update_window_rows(self.DELETE)

    def write_file(self, file_name:str) -> None:
        f = open(file_name ,"w", encoding="UTF-8")
        f.write(f"{self.lines.cursor_position}\n{self.lines.prev_id}\n{self.lines.next_id}\n{self.lines.curr_id}\n{self.lines.iterator}\n{self.lines.dict}\n{self.lines.curr_line}\n{self.top_window_row}\n{self.top_window_col}")
        f.close()

    def read_file(self, file_name:str) -> None:
        with open(file_name ,"r", encoding="UTF-8") as f:
            params = f.readlines()
        try:
            next_id = int(params[2])
        except ValueError:
            next_id = None
        try:
            prev_id = int(params[1])
        except ValueError:
            prev_id = None

        self.lines.cursor_position=int(params[0])
        self.lines.prev_id=prev_id
        self.lines.next_id=next_id
        self.lines.curr_id=int(params[3])
        self.lines.iterator=int(params[4])
        self.lines.dict = eval(params[5])
        self.lines.curr_line = list(params[6])
        self.top_window_row = int(params[7])
        self.top_window_col = int(params[8])

class Controller:
    """The connection between the model and the view"""
    def __init__(self, model:WindowedLines=WindowedLines(),view=curses.initscr()):
        self.model = model
        self.view = view

    def run(self):
        "the loop connecting the model to user input, displayed using a curses view."
        self.model.read_file("tst.txt")
        self.view.keypad(True)
        curses.noecho()
        curses.cbreak()

        self.view.addstr(self.model.print_window())
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