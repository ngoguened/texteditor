from input_phoneme import InputPhoneme
from phonemeKeyboard.phonemes import Phoneme, PhonemeEnums
import unittest
import pickle

with open('saved_dictionary.pkl', 'rb') as f:
    word_dict = pickle.load(f)

class TestInputPhoneme(unittest.TestCase):      
    # hh -> h phoneme
    def test_one_phoneme(self):
        input_phoneme = InputPhoneme(word_dict=word_dict)
        input_phoneme.update_phonemes('h')
        assert input_phoneme.chars == ['h'] and not input_phoneme.phonemes
        input_phoneme.update_phonemes('h')
        assert not input_phoneme.chars and input_phoneme.phonemes[0].phoneme == PhonemeEnums.h

    # hh ai -> "hye" str
    def test_one_word(self):
        input_phoneme = InputPhoneme(word_dict=word_dict)
        word = input_phoneme.update_phonemes('h')
        assert not word
        input_phoneme.update_phonemes('h')
        assert not word
        input_phoneme.update_phonemes('a')
        assert not word
        word = input_phoneme.update_phonemes('i')
        assert word == "hye"

    # nonalpha -> empty everything
    def test_nonalpha_clears(self):
        input_phoneme = InputPhoneme(word_dict=word_dict)
        input_phoneme.update_phonemes('h')
        input_phoneme.update_phonemes(',')
        assert not input_phoneme.chars

    # h nonalpha -> error: model should have picked up nonalpha chars
    # 

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
