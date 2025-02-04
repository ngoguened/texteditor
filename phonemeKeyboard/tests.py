"""Testing"""
import unittest
import logging
import os

import phonemes
import curses

class TestListCharStream(unittest.TestCase):
    def test_init(self):
        character_stream = phonemes.ListCharStream(lst=[])
        assert not character_stream.lst

    def test_get(self):
        character_stream = phonemes.ListCharStream(lst=['a','b'])
        assert character_stream.get() == 'a'
        assert character_stream.get() == 'b'
        assert not character_stream.get()
    
class TestKeypadCharStream(unittest.TestCase):
    def test_init(self):
        keypad_stream = phonemes.KeypadCharStream(view=None, debug='a')
        assert not keypad_stream.view
    def test_get(self):
        keypad_stream = phonemes.KeypadCharStream(view=None, debug='a')
        assert keypad_stream.get() == 'a'

class TestPhonemeStream(unittest.TestCase):
    def test_init(self):
        char_stream = phonemes.ListCharStream(lst=['a'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        assert phoneme_stream.charstream.lst == ['a']
    def test_get(self):
        char_stream = phonemes.ListCharStream(lst=['f'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        phoneme = phoneme_stream.get()
        assert not phoneme.capitalized and phoneme.phoneme == phonemes.PhonemeEnums.f

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
