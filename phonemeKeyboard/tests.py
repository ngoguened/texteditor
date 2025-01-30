"""Testing"""
import unittest
import logging
import os

import phonemes
import curses

class TestCharacterStream(unittest.TestCase):
    """Test the PhonemeGenerator"""
    def test_init(self):
        character_stream = phonemes.CharacterStream()
        assert not character_stream.characters

    def test_get(self):
        character_stream = phonemes.CharacterStream()
        view = None
        character_stream.get(view, debug='a')
        assert character_stream.characters == ['a']
    
class TestPhonemeStream(unittest.TestCase):
    def test_init(self):
        phoneme_stream = phonemes.PhonemeStream()
        assert not phoneme_stream.phonemes
    def test_get(self):
        phoneme_stream = phonemes.PhonemeStream()
        character_stream = phonemes.CharacterStream()
        view = None
        phoneme_stream.get(character_stream, view, debug='p')
        assert not character_stream.characters
        assert phoneme_stream.phonemes[0].phoneme == phonemes.PhonemeEnums.p
        assert not phoneme_stream.phonemes[0].capitalized
        
        phoneme_stream.get(character_stream, view, debug='P')
        assert phoneme_stream.phonemes[1].phoneme == phonemes.PhonemeEnums.p, phoneme_stream.phonemes
        assert phoneme_stream.phonemes[1].capitalized, phoneme_stream.phonemes


    view = curses.initscr()


if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
