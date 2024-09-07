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
        assert model.lines.curr_line == ['a']
        model.insert('b')
        assert model.lines.curr_line == ['a','b']
        model.insert('c')
        assert model.lines.curr_line == ['a','b','c']
        model.delete()
        assert model.lines.curr_line == ['a','b']
        model.delete()
        assert model.lines.curr_line == ['a']
        model.delete()
        assert model.lines.curr_line == []
        model.delete()
        assert model.lines.curr_line == [] 

    def test_lines(self):
        """check line storage works correctly"""
        model.insert('a')
        model.insert('b')
        model.insert('\n')
        assert model.lines.curr_line == []
        assert model.lines.prev_lines == [['a','b']]
        model.insert('c')
        model.insert('\n')
        model.insert('d')
        assert model.lines.curr_line == ['d']
        assert model.lines.prev_lines == [['a','b'],['c']]
        model.left()
        model.delete()
        assert model.lines.curr_line == ['c','d']
        model.left()
        model.delete()
        assert model.lines.curr_line == ['a','b','c','d']

        model.down()
        model.insert('\n')
        model.insert('f')
        model.up()
        assert model.lines.curr_line == ['a','b','c','d']
        while model.lines.cursor_position != 4:
            model.right()
        model.insert('\n')
        model.insert('e')
        assert model.lines.curr_line == ['e']
        model.down()
        assert model.lines.curr_line == ['f']

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
        assert new_model.top_window_row == 0
        new_model.down()
        assert new_model.top_window_row == 1, new_model.lines.prev_lines
        new_model.delete()
        assert new_model.top_window_row == 0
        new_model.insert('\n')
        assert new_model.top_window_row == 1
        new_model.up()
        assert new_model.top_window_row == 0

        new_model=text_editor.WindowedLines(window_size=(2,5))
        for char in "Hello\nthere,\nWorld!":
            new_model.insert(char)
        assert new_model.top_window_row == 1, new_model.lines.prev_lines
        new_model.up()
        new_model.up()
        assert new_model.top_window_row == 0
        new_model.down()
        for _ in range(5):
            new_model.left()
        new_model.delete()
        assert new_model.top_window_row == 0
        new_model.insert('\n')
        assert new_model.top_window_row == 1, f"{len(new_model.lines.prev_lines[new_model.top_window_row:])+len(new_model.lines.next_lines[:new_model.window_size[0]-new_model.top_window_row-1])+1}"

        new_model=text_editor.WindowedLines(window_size=(3,5))
        for char in "a\nb\nc\nd":
            new_model.insert(char)
        new_model.up()
        new_model.up()
        new_model.up()
        new_model.up()
        new_model.up()

    def test_read_write(self):
        model.write_file("tst.txt")
        model.read_file("tst.txt")
        assert model.lines.curr_line == ['a','b','c','d'], model.lines.curr_line
        assert model.lines.next_lines == [['e'],['f']], model.lines.next_lines
        
        os.remove("tst.txt")

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
