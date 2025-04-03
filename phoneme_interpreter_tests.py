import unittest
import pickle
from phonemes import Phoneme, PhonemeEnums
from phoneme_interpreter_interface import PhonemeInterpreterInterface
from test_phoneme_interpreter import TestPhonemeInterpreter
from dict_phoneme_interpreter import DictPhonemeInterpreter

with open('saved_dictionary.pkl', 'rb') as f:
    word_dict = pickle.load(f)

class InterpretersTest(unittest.TestCase):
    """Test each implemented interpreter"""
    def test_interpret(self):
        interpreters:list[PhonemeInterpreterInterface] = [
            TestPhonemeInterpreter(), DictPhonemeInterpreter()
            ]
        for interpreter in interpreters:
            assert interpreter.interpret([
                Phoneme(phoneme=PhonemeEnums.h), Phoneme(phoneme=PhonemeEnums.aɪ)
                ])


if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
