"""Testing"""
import unittest
import text_editor
import os

model = text_editor.WindowedLines()
class TestModel(unittest.TestCase):
    """Test the model"""

    def test_insert_delete(self):
        """check insert and delete work correctly"""
        model.insert('a')
        assert model.curr_line == ['a']
        model.insert('b')
        assert model.curr_line == ['a','b']
        model.insert('c')
        assert model.curr_line == ['a','b','c']
        model.delete()
        assert model.curr_line == ['a','b']
        model.delete()
        assert model.curr_line == ['a']
        model.delete()
        assert model.curr_line == []
        model.delete()
        assert model.curr_line == [] 

    def test_lines(self):
        """check line storage works correctly"""
        model.insert('a')
        model.insert('b')
        model.insert('\n')
        assert model.curr_line == []
        assert model.prev_lines == [['a','b']]
        model.insert('c')
        model.insert('\n')
        model.insert('d')
        assert model.curr_line == ['d']
        assert model.prev_lines == [['a','b'],['c']]
        model.left()
        model.delete()
        assert model.curr_line == ['c','d']
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

    def test_window(self):
        """Test that the window works properly"""
        new_model=text_editor.WindowedLines(window_size=(1,5))
        assert new_model.top_window_row == 0 and new_model.top_window_col == 0
        for char in "Hello\nWorld!":
            new_model.insert(char)
        assert new_model.top_window_col == 1
        for _ in range(6):
            new_model.left()
        assert new_model.top_window_col == 0

        new_model.up()
        assert new_model.top_window_row == 0
        new_model.up()
        assert new_model.top_window_row == 0, new_model.top_window_row
        new_model.down()
        assert new_model.top_window_row == 1, new_model.prev_lines
        new_model.delete()
        assert new_model.top_window_row == 0
        new_model.insert('\n')
        assert new_model.top_window_row == 1
        new_model.up()
        assert new_model.top_window_row == 0

        new_model=text_editor.WindowedLines(window_size=(2,5))
        for char in "Hello\nthere,\nWorld!":
            new_model.insert(char)
        assert new_model.top_window_row == 1, new_model.prev_lines
        new_model.up()
        new_model.up()
        assert new_model.top_window_row == 0
        new_model.down()
        for _ in range(5):
            new_model.left()
        new_model.delete()
        assert new_model.top_window_row == 0
        new_model.insert('\n')
        assert new_model.top_window_row == 1, f"{len(new_model.prev_lines[new_model.top_window_row:])+1}"

        new_model=text_editor.WindowedLines(window_size=(10,5))
        for char in "a\nb\nc\nd":
            new_model.insert(char)
        new_model.up()
        new_model.up()
        new_model.up()
        new_model.up()
        new_model.up()
        assert new_model.print_window() == "a    \nb    \nc    \nd    ", new_model.print_window()

        new_model=text_editor.WindowedLines(window_size=(4,5))
        for char in "a\nb\nc\nd\ne\nf\ng\nh\ni\nj\nk":
            new_model.insert(char)
        for _ in range(18):
            new_model.up()

    def test_read_write(self):
        model.write_file("tst.txt")
        model.read_file("tst.txt")
        assert model.curr_line == ['a','b','c','d'], model.curr_line
        assert model.next_lines == [['f'],['e']], model.next_lines
        
        os.remove("tst.txt")

        model.read_file("text_editor.py")
        model.down()

    def test_mark(self):
        new_model=text_editor.WindowedLines()
        for char in "Hello\nthere,\nWorld!":
            new_model.insert(char)
        assert new_model.mark is None
        new_model.set_mark()
        assert new_model.mark == [2, 6, new_model.curr_line]

        for _ in range(6):
            new_model.left()
        new_model.delete()
        assert new_model.mark is None
        assert new_model.curr_line == [], new_model.curr_line
        new_model.insert('a')
        new_model.left()
        new_model.set_mark()
        new_model.right()
        new_model.delete()
        assert new_model.curr_line == [], new_model.curr_line

        for _ in range(5):
            new_model.insert('a')
        for _ in range(5):
            new_model.left()
        assert new_model.mark is None
        new_model.set_mark()
        new_model.right()
        new_model.right()
        new_model.set_mark()
        new_model.delete()
        assert new_model.curr_line == ['a']*5, new_model.curr_line

    def test_saved_cursor_x_position(self):
        new_model=text_editor.WindowedLines()
        assert new_model.saved_cursor_x_position == new_model.cursor_position
        for char in "Helloooooooooooooooooo\nWorld!":
            new_model.insert(char)
        new_model.up()
        for _ in range(50):
            new_model.right()
        long = new_model.cursor_position
        assert new_model.saved_cursor_x_position == long
        new_model.down()
        assert new_model.saved_cursor_x_position != new_model.cursor_position
        new_model.up()
        assert new_model.saved_cursor_x_position == new_model.cursor_position
        new_model.down()
        new_model.left()
        new_model.up()
        assert new_model.saved_cursor_x_position != long


if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
