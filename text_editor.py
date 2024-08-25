"""Text Editor"""

# import curses

class Model:
    """
    The model for the text editor.
    API supports up/down/left/right movement of cursor and insert/delete.
    TODO: Add highlighting.
    TODO: Read/Write files.
    """
    def __init__(self, cursor_position=0, prev_id=None, next_id=None,
                 curr_id=0, iterator=1, window=(10,16)) -> None:
        self.text = []
        self.cache = {}
        self.cursor_position = cursor_position

        self.prev_id = prev_id
        self.next_id = next_id
        self.curr_id = curr_id
        self.iterator = iterator

        self.window_rows = [None]*window[0]
        self.window_cols = [0, window[1]]

    def update_window_cols(self) -> None:
        """Update the window columns relative to the cursor."""
        if self.cursor_position > self.window_cols[1]:
            self.window_cols[0]+=1
            self.window_cols[1]+=1
        elif self.cursor_position < self.window_cols[0]:
            self.window_cols[0]-=1
            self.window_cols[1]-=1

    def update_window_rows(self, operation=None) -> None:
        """Update the window rows relative to the stored pointers in window_rows."""
        if operation not in ["up", "down", "insert", "delete", None]:
            raise ValueError()
        if self.curr_id not in self.window_rows:
            if operation == "down":
                self.window_rows = self.window_rows[1:]+[self.curr_id]
            elif operation == "up":
                self.window_rows = [self.curr_id]+self.window_rows[:len(self.window_rows)-1]

            elif operation == "insert":
                for idx, row in enumerate(self.window_rows):
                    if row is None:
                        self.window_rows[idx] = self.curr_id
                        return
                self.window_rows = self.window_rows[1:]+[self.curr_id]
        else:
            if operation == "delete":
                for idx, row in enumerate(self.window_rows):
                    if row not in self.cache and self.window_rows[0] is not None:
                        removed_id = self.window_rows[:idx]+self.window_rows[idx+1:]
                        if self.window_rows[0] in self.cache and self.cache[self.window_rows[0]][1] is not None:
                            self.window_rows = [self.cache[self.window_rows[0]][1]]+removed_id
                        else:
                            if self.window_rows[len(self.window_rows)-1] is not None:
                                self.window_rows = removed_id+[self.cache[self.window_rows[len(self.window_rows)-1]][2]]


    def right(self) -> None:
        """Moves the cursor right by shifting the cursor position right."""
        if self.cursor_position < len(self.text):
            self.cursor_position += 1
            self.update_window_cols()

    def left(self) -> None:
        """Moves the cursor left by shifting the cursor position left."""
        if self.cursor_position > 0:
            self.cursor_position -= 1
            self.update_window_cols()


    def up(self) -> None:
        """Moves the cursor up by retrieving the cached data for prev_id and 
        updating relevant fields."""
        if self.prev_id is not None:
            [prev_text, prev_prev_id, prev_next_id] = self.cache[self.prev_id]
            self.curr_id = self.prev_id
            self.text = prev_text
            self.cursor_position = min(len(prev_text), self.cursor_position)
            self.update_window_cols()
            self.prev_id = prev_prev_id
            self.next_id = prev_next_id
            self.update_window_rows("up")
        else:
            self.cursor_position = 0
            self.update_window_cols()

    def down(self) -> None:
        """Moves the cursor down by retrieving the cached data for next_id and 
        updating relevant fields."""
        if self.next_id is not None:
            [next_text, next_prev_id, next_next_id] = self.cache[self.next_id]
            self.curr_id = self.next_id
            self.text = next_text
            self.cursor_position = min(len(next_text), self.cursor_position)
            self.update_window_cols()
            self.prev_id = next_prev_id
            self.next_id = next_next_id
            self.update_window_rows("down")
        else:
            self.cursor_position = len(self.text)
            self.update_window_cols()

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in the cache and create a 
        new id for the current line."""
        if char == '\n':
            self.cache[self.curr_id][0] = self.text[:self.cursor_position+1]
            self.cache[self.curr_id][2] = self.iterator
            self.text = self.text[self.cursor_position+1:]
            self.cursor_position = 0
            self.update_window_cols()
            self.prev_id = self.curr_id

            if self.next_id in self.cache:
                self.cache[self.next_id][1] = self.iterator
            self.cache[self.iterator] = [self.text, self.prev_id, self.next_id]
            self.curr_id = self.iterator
            self.iterator += 1
            self.update_window_rows("insert")
        else:
            if len(self.text) <= self.cursor_position:
                self.text.append(char)
            else:
                self.text[self.cursor_position] = char

            self.cursor_position += 1
            self.update_window_cols()
            self.cache[self.curr_id] = [self.text, self.prev_id, self.next_id]

    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        if self.cursor_position == 0 and self.prev_id is not None:
            [prev_text, prev_prev_id, _] = self.cache.pop(self.prev_id)
            self.text = prev_text+self.text
            self.cursor_position = len(prev_text)-1
            self.update_window_rows()
            self.prev_id = prev_prev_id
            self.update_window_rows("delete")
        else:
            self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.update_window_cols()
        self.cache[self.curr_id] = [self.text, self.prev_id, self.next_id]




class Controller:
    """TODO"""

def main():
    """Testing"""
    model = Model()

    #check insert works correctly
    model.insert('a')
    assert model.text == ['a']
    model.insert('b')
    assert model.text == ['a','b']
    model.insert('c')
    assert model.text == ['a','b','c']

    #check delete works correctly
    model.delete()
    assert model.text == ['a','b']
    model.delete()
    assert model.text == ['a']
    model.delete()
    assert model.text == []
    model.delete()
    assert model.text == []

    #check line caching works correctly
    model.insert('a')
    model.insert('b')
    model.insert('\n')
    assert model.text == []
    assert model.cache[0][0] == ['a','b']
    model.insert('c')
    model.insert('\n')
    model.insert('d')
    assert model.text == ['d']
    assert model.cache[0][0] == ['a','b']
    assert model.cache[1][0] == ['c']
    model.left()
    model.delete()
    assert model.text == ['c','d']
    assert 1 not in model.cache
    model.left()
    model.delete()
    assert model.text == ['a','b','c','d']

    model.down()
    model.insert('\n')
    model.insert('f')
    model.up()
    assert model.text == ['a','b','c','d']
    while model.cursor_position != 4:
        model.right()
    model.insert('\n')
    model.insert('e')
    assert model.text == ['e']
    model.down()
    assert model.text == ['f']

    #Check the window
    model=Model(window=(1,5))
    assert model.window_rows == [None] and model.window_cols == [0,5]
    for char in "Hello\nWorld!":
        model.insert(char)
    assert model.window_cols == [1,6]
    assert model.window_rows == [1]
    for _ in range(6):
        model.left()
    assert model.window_cols == [0,5]

    model.up()
    assert model.window_rows == [0]
    model.up()
    assert model.window_rows == [0]
    model.down()
    assert model.window_rows == [1]
    model.delete()
    assert model.window_rows == [1]
    model.insert('\n')
    assert model.window_rows == [2]
    model.up()
    assert model.window_rows == [1]

    model=Model(window=(2,5))
    for char in "Hello\nthere,\nWorld!":
        model.insert(char)
    assert model.window_rows == [1,2]
    model.up()
    model.up()
    assert model.window_rows == [0,1]
    model.down()
    for _ in range(5):
        model.left()
    model.delete()
    assert model.window_rows == [1,2]
    model.insert('\n')
    print(model.cache)
    assert model.window_rows == [2,3]

    print("All tests pass")


if __name__ == "__main__":
    main()
    