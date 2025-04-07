import unittest
import pickle
from phonemes import Phoneme, PhonemeEnums
from phoneme_interpreter_interface import PhonemeInterpreterInterface
from test_phoneme_interpreter import TestPhonemeInterpreter

with open('saved_dictionary.pkl', 'rb') as f:
    word_dict = pickle.load(f)

class InterpretersTest(unittest.TestCase):
    """Test each implemented interpreter"""
    def test_interpret(self):
        interpreter:PhonemeInterpreterInterface = TestPhonemeInterpreter()
        assert "hi" in interpreter.interpret([
            Phoneme(phoneme=PhonemeEnums.h), Phoneme(phoneme=PhonemeEnums.aɪ)
            ])
            
    def test_empty_interpret(self):
        interpreter:PhonemeInterpreterInterface = TestPhonemeInterpreter()
        assert not interpreter.interpret([])

    def test_no_words_to_interpret(self):
        interpreter:PhonemeInterpreterInterface = TestPhonemeInterpreter()
        assert not interpreter.interpret([Phoneme(phoneme=PhonemeEnums.h)])

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
