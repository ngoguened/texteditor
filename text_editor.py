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

class Lines:
    """Stores the text, the previous id, and the next id of each line."""
    def __init__(self) -> None:
        self.dict = {}
    
    def store(self, curr_id, line, prev_id, next_id) -> None:
        self.dict[curr_id] = [line, prev_id, next_id]

    def fetch_all(self, key) -> list[list[str], int, int]:
        return self.dict[key]
    
    def fetch_line(self, key) -> list[str]:
        return self.dict[key][0]

    def fetch_prev(self, key) -> list[str]:
        return self.dict[key][1]
    
    def fetch_next(self, key) -> list[str]:
        return self.dict[key][2]
    
    def pop(self, key) -> list[list[str], int, int]:
        return self.dict.pop(key)
    
    def present(self, key) -> bool:
        return key in self.dict
    

# import curses

class Model:
    """
    The model for the text editor.
    API supports up/down/left/right movement of cursor and insert/delete.
    TODO: Add highlighting.
    TODO: Read/Write files.
    """

    # window update constants:
    UP = 0
    DOWN = 1
    INSERT = 2
    DELETE = 3

    def __init__(self, cursor_position=0, prev_id=None, next_id=None,
                 curr_id=0, iterator=1, window_size=(10,16)) -> None:
        self.curr_line = []
        self.lines = Lines()
        self.cursor_position = cursor_position

        # ids are keys for each stored line.
        self.curr_id = curr_id # the id for the current line being manipulated.
        self.prev_id = prev_id # the id for the previous line.
        self.next_id = next_id # the id for the next line.

        self.iterator = iterator # Allocates monotonically increasing identifiers to guarantee new ids are unique.

        self.window_size = window_size
        self.top_window_row = self.curr_id
        self.top_window_col = 0

    def update_window_cols(self) -> None:
        """Update the window's first column relative to the cursor."""
        if self.cursor_position > self.window_size[1]+self.top_window_col:
            self.top_window_col+=1
        elif self.cursor_position < self.top_window_col:
            self.top_window_col-=1

    def update_window_rows(self, operation=None) -> None:
        """Update the window's first row relative to row-changing operations."""
        if operation == self.UP:
            if self.next_id == self.top_window_row:
                self.top_window_row = self.curr_id
        elif operation in [self.INSERT,self.DOWN]:
            tmp = self.top_window_row
            for _ in range(self.window_size[0]-1):
                if tmp is None or self.lines.fetch_next(tmp) is None or tmp == self.curr_id:
                    return
                tmp = self.lines.fetch_next(tmp)
            if tmp != self.curr_id:
                self.top_window_row = self.lines.fetch_next(self.top_window_row)
        elif operation == self.DELETE:
            if not self.lines.present(self.top_window_row):
                self.top_window_row = self.curr_id
        else:
            raise ValueError()


    def print_window(self) -> str:
        """Makes a string of the current window"""
        out=""
        iterate_row = self.top_window_row
        iterate_col = self.top_window_col
        for _ in range(self.window_size[0]):
            for i in range(iterate_col, iterate_col+self.window_size[1]):
                if i in range(len(self.lines.fetch_line(iterate_row))):
                    out+=self.lines.fetch_line(iterate_row)[i]
                else:
                    out+=" "
            if iterate_row is not None:
                iterate_row = self.lines.fetch_next(iterate_row)
            out +="\n"
        return out[:-1]


    def right(self) -> None:
        """Moves the cursor right by shifting the cursor position right."""
        if self.cursor_position < len(self.curr_line):
            self.cursor_position += 1
            self.update_window_cols()

    def left(self) -> None:
        """Moves the cursor left by shifting the cursor position left."""
        if self.cursor_position > 0:
            self.cursor_position -= 1
            self.update_window_cols()


    def up(self) -> None:
        """Moves the cursor up by retrieving the data for prev_id and 
        updating relevant fields."""
        if self.prev_id is not None:
            [prev_line, prev_prev_id, prev_next_id] = self.lines.fetch_all(self.prev_id)
            self.curr_id = self.prev_id
            self.curr_line = prev_line
            self.cursor_position = min(len(prev_line), self.cursor_position)
            self.update_window_cols()
            self.prev_id = prev_prev_id
            self.next_id = prev_next_id
            self.update_window_rows(self.UP)
        else:
            self.cursor_position = 0
            self.update_window_cols()

    def down(self) -> None:
        """Moves the cursor down by retrieving the data for next_id and 
        updating relevant fields."""
        if self.next_id is not None:
            [next_line, next_prev_id, next_next_id] = self.lines.fetch_all(self.next_id)
            self.curr_id = self.next_id
            self.curr_line = next_line
            self.cursor_position = min(len(next_line), self.cursor_position)
            self.update_window_cols()
            self.prev_id = next_prev_id
            self.next_id = next_next_id
            self.update_window_rows(self.DOWN)
        else:
            self.cursor_position = len(self.curr_line)
            self.update_window_cols()

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in lines and create a 
        new id for the current line."""
        if char == '\n':
            self.lines.store(self.curr_id, self.curr_line[:self.cursor_position+1],self.lines.fetch_prev(self.curr_id),self.iterator)
            self.curr_line = self.curr_line[self.cursor_position+1:]
            self.cursor_position = 0
            self.update_window_cols()
            self.prev_id = self.curr_id

            if self.lines.present(self.next_id):
                self.lines.store(self.next_id, self.lines.fetch_line(self.next_id), self.iterator, self.lines.fetch_next(self.next_id))
            self.lines.store(self.iterator, self.curr_line, self.prev_id, self.next_id)
            self.curr_id = self.iterator
            self.iterator += 1
            self.update_window_rows(self.INSERT)
        else:
            if len(self.curr_line) <= self.cursor_position:
                self.curr_line.append(char)
            else:
                self.curr_line[self.cursor_position] = char

            self.cursor_position += 1
            self.update_window_cols()
            self.lines.store(self.curr_id, self.curr_line, self.prev_id, self.next_id)

    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        if self.cursor_position == 0 and self.prev_id is not None:
            [prev_line, prev_prev_id, _] = self.lines.pop(self.prev_id)
            self.curr_line = prev_line+self.curr_line
            self.cursor_position = len(prev_line)-1
            self.update_window_cols()
            self.prev_id = prev_prev_id
            self.update_window_rows(self.DELETE)
        else:
            self.curr_line = self.curr_line[:self.cursor_position-1] + self.curr_line[self.cursor_position:]
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.update_window_cols()
        self.lines.store(self.curr_id, self.curr_line, self.prev_id, self.next_id)

class Controller:
    """TODO"""

def main():
    """Testing"""
    model = Model()

    #check insert works correctly
    model.insert('a')
    assert model.curr_line == ['a']
    model.insert('b')
    assert model.curr_line == ['a','b']
    model.insert('c')
    assert model.curr_line == ['a','b','c']

    #check delete works correctly
    model.delete()
    assert model.curr_line == ['a','b']
    model.delete()
    assert model.curr_line == ['a']
    model.delete()
    assert model.curr_line == []
    model.delete()
    assert model.curr_line == []

    #check line caching works correctly
    model.insert('a')
    model.insert('b')
    model.insert('\n')
    assert model.curr_line == []
    assert model.lines.dict[0][0] == ['a','b']
    model.insert('c')
    model.insert('\n')
    model.insert('d')
    assert model.curr_line == ['d']
    assert model.lines.dict[0][0] == ['a','b']
    assert model.lines.dict[1][0] == ['c']
    model.left()
    model.delete()
    assert model.curr_line == ['c','d']
    assert 1 not in model.lines.dict
    model.left()
    model.delete()
    assert model.curr_line == ['a','b','c','d']

    model.down()
    model.insert('\n')
    model.insert('f')
    model.up()
    assert model.curr_line == ['a','b','c','d']
    while model.cursor_position != 4:
        model.right()
    model.insert('\n')
    model.insert('e')
    assert model.curr_line == ['e']
    model.down()
    assert model.curr_line == ['f']

    #Check the window
    model=Model(window_size=(1,5))
    assert model.top_window_row == 0 and model.top_window_col == 0
    for char in "Hello\nWorld!":
        model.insert(char)
    
    assert model.top_window_col == 1
    for _ in range(6):
        model.left()
    assert model.top_window_col == 0

    model.up()
    assert model.top_window_row == 0
    model.up()
    assert model.top_window_row == 0
    model.down()
    assert model.top_window_row == 1
    model.delete()
    assert model.top_window_row == 1
    model.insert('\n')
    assert model.top_window_row == 2
    model.up()
    assert model.top_window_row == 1

    model=Model(window_size=(2,5))
    for char in "Hello\nthere,\nWorld!":
        model.insert(char)
    assert model.top_window_row == 1
    model.up()
    model.up()
    assert model.top_window_row == 0
    model.down()
    for _ in range(5):
        model.left()
    model.delete()
    assert model.top_window_row == 1
    model.insert('\n')
    assert model.top_window_row == 1

    print("All tests pass")


if __name__ == "__main__":
    main()
    