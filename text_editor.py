"""Text Editor"""

# import keyboard

class Model:
    """
    The model for the text editor.
    API supports up/down/left/right movement of cursor and insert/delete.
    TODO: Add highlighting.
    """
    def __init__(self, cursor_position=0, prev_id=None,
                 next_id=None, curr_id=0, iterator=1) -> None:
        self.text = []
        self.cursor_position = cursor_position

        self.prev_id = prev_id
        self.next_id = next_id
        self.curr_id = curr_id
        self.iterator = iterator

        self.cache = {}


    def right(self) -> None:
        """Moves the cursor right by shifting the cursor position right."""
        if self.cursor_position < len(self.text):
            self.cursor_position += 1

    def left(self) -> None:
        """Moves the cursor left by shifting the cursor position left."""
        if self.cursor_position > 0:
            self.cursor_position -= 1

    def up(self) -> None:
        """Moves the cursor up by retrieving the cached data for prev_id and 
        updating relevant fields."""
        if self.prev_id is not None:
            [prev_text, prev_prev_id, prev_next_id] = self.cache[self.prev_id]
            self.curr_id = self.prev_id
            self.text = prev_text
            self.cursor_position = min(len(prev_text), self.cursor_position)
            self.prev_id = prev_prev_id
            self.next_id = prev_next_id
        else:
            self.cursor_position = 0

    def down(self) -> None:
        """Moves the cursor down by retrieving the cached data for next_id and 
        updating relevant fields."""
        if self.next_id is not None:
            [next_text, next_prev_id, next_next_id] = self.cache[self.next_id]
            self.curr_id = self.next_id
            self.text = next_text
            self.cursor_position = min(len(next_text), self.cursor_position)
            self.prev_id = next_prev_id
            self.next_id = next_next_id
        else:
            self.cursor_position = len(self.text)

    def insert(self, char='') -> None:
        """Inserts char to the current line of text. If the char is \n, it 
        will store everything behind the cursor in the cache and create a 
        new id for the current line."""
        if char == '\n':
            self.cache[self.curr_id][0] = self.text[:self.cursor_position+1]
            self.cache[self.curr_id][2] = self.iterator
            self.text = self.text[self.cursor_position+1:]
            self.cursor_position = 0
            self.prev_id = self.curr_id

            if self.next_id in self.cache:
                self.cache[self.next_id][1] = self.iterator
            self.cache[self.iterator] = [self.text, self.prev_id, self.next_id]
            self.curr_id = self.iterator
            self.iterator += 1
        else:
            if len(self.text) <= self.cursor_position:
                self.text.append(char)
            else:
                self.text[self.cursor_position] = char

            self.cursor_position += 1
            self.cache[self.curr_id] = [self.text, self.prev_id, self.next_id]


    def delete(self) -> None:
        """Deletes char from current line of text. If it is at the end of the line and there 
        is a previous line, it will merge the two lines."""
        if self.cursor_position == 0 and self.prev_id is not None:
            [prev_text, prev_prev_id, _] = self.cache.pop(self.prev_id)
            self.text = prev_text+self.text
            self.cursor_position = len(prev_text)
            self.prev_id = prev_prev_id
        else:
            self.text = self.text[:self.cursor_position-1] + self.text[self.cursor_position:]
            if self.cursor_position > 0:
                self.cursor_position -= 1
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

    print("All tests pass")


if __name__ == "__main__":
    main()
    