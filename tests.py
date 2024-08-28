"""Testing"""
import unittest
import text_editor

model = text_editor.Model()
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

    def test_window(self):
        """Test that the window works properly"""
        model=text_editor.Model(window_size=(1,5))
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

        model=text_editor.Model(window_size=(2,5))
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


        model=text_editor.Model(window_size=(5,5))
        for char in "f\n\nf":
            model.insert(char)
        model.left()
        model.delete()
        assert model.lines.present(model.prev_id) and model.lines.present(model.lines.fetch_next(model.prev_id))

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
