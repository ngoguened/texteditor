from input_phoneme import InputPhoneme
from phonemeKeyboard.phonemes import PhonemeEnums
from dict_phoneme_interpreter import DictPhonemeInterpreter
import unittest

class InputPhonemeTest(unittest.TestCase):
    # hh -> h phoneme
    def test_one_phoneme(self):
        input_phoneme = InputPhoneme(interpreter=DictPhonemeInterpreter())
        input_phoneme.update_phonemes('h')
        assert input_phoneme.chars == ['h'] and not input_phoneme.phonemes
        input_phoneme.update_phonemes('h')
        assert not input_phoneme.chars and input_phoneme.phonemes[0].phoneme == PhonemeEnums.h

    # hh ai -> "hey" str
    def test_one_word(self):
        input_phoneme = InputPhoneme(interpreter=DictPhonemeInterpreter())
        word = input_phoneme.update_phonemes('h')
        assert not word
        word = input_phoneme.update_phonemes('h')
        assert not word
        word = input_phoneme.update_phonemes('a')
        assert not word
        word = input_phoneme.update_phonemes('i')
        assert word == "hey"

    # completed word -> empty everything
    def test_word_completion_clears(self):
        input_phoneme = InputPhoneme(interpreter=DictPhonemeInterpreter())
        input_phoneme.update_phonemes('au')
        word = input_phoneme.complete()
        assert word == "oo"
        assert not input_phoneme.chars
        assert not input_phoneme.phonemes

    # nonalpha -> error: model should have picked up nonalpha chars
    def test_nonalpha_fails(self):
        input_phoneme = InputPhoneme(interpreter=DictPhonemeInterpreter())
        self.assertRaises(ValueError, input_phoneme.update_phonemes, ' ')
    
    def test_cycle_word_lst(self):
        input_phoneme = InputPhoneme(interpreter=DictPhonemeInterpreter())
        input_phoneme.update_phonemes('h')
        input_phoneme.update_phonemes('h')
        input_phoneme.update_phonemes('a')
        word = input_phoneme.update_phonemes('i')
        assert word == "hey"
        input_phoneme.cycle_word_lst(True)
        assert input_phoneme.update_word() != "hey"
        input_phoneme.cycle_word_lst(False)
        assert input_phoneme.update_word() == "hey"


if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
