import unittest
from phonemeKeyboard.phonemes import Phoneme, PhonemeEnums
import pickle

with open('saved_dictionary.pkl', 'rb') as f:
    word_dict = pickle.load(f)

class TestInterpreters(unittest.TestCase):
    """Test each implemented interpreter"""
    def test_interpret(self):
        interpreters = []
        for interpreter in interpreters:
            assert interpreter.interpret([Phoneme(phoneme=PhonemeEnums.h), Phoneme(phoneme=PhonemeEnums.aɪ)])


if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
