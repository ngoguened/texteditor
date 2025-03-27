import unittest
from phoneme_interpreter_interface import PhonemeInterpreterInterface

default_nick_llm = PhonemeInterpreterInterface()
class TestInterpreterInterface(unittest.TestCase): # Is this test class even worth having? It feels trivial.
    """Test the default interpreter"""

    def test_default_init(self):
        assert not default_nick_llm.context and not default_nick_llm.llm

    def test_default_interpret(self):
        assert not default_nick_llm.interpret("")
    
class TestImplementedInterperter(unittest.TestCase):
    """Test the interpreter implementation"""

    def test_interpret(self):
        pass

    def test_set_context(self):
        pass

    def test_add_context(self):
        pass

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
