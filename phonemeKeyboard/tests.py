"""Testing"""
import unittest
import logging
import os

import phonemes
import curses

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
    def test_capitalized(self):
        char_stream = phonemes.ListCharStream(lst=['F'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        phoneme = phoneme_stream.get()
        assert phoneme.capitalized and phoneme.phoneme == phonemes.PhonemeEnums.f
    def test_stream(self):
        char_stream = phonemes.ListCharStream(lst=['h','h','.','a','i'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        assert phoneme_stream.get().phoneme == phonemes.PhonemeEnums.h
        assert phoneme_stream.get() == "."
        assert phoneme_stream.get().phoneme == phonemes.PhonemeEnums.aɪ
    # Will loop until punctuation if wrong char is typed.

class TestWordStream(unittest.TestCase):
    def test_init(self):
        char_stream = phonemes.ListCharStream(lst=['a'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        word_stream = phonemes.WordStream(phonemestream=phoneme_stream)
        assert word_stream.phonemestream.charstream.lst == ['a']
    def test_get(self):
        char_stream = phonemes.ListCharStream(lst=['h','h','a','i'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        word_stream = phonemes.WordStream(phonemestream=phoneme_stream)
        assert word_stream.get() == "h"
    def test_stream(self):
        char_stream = phonemes.ListCharStream(lst=['h','h','a','i'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        word_stream = phonemes.WordStream(phonemestream=phoneme_stream)
        word = word_stream.get() + word_stream.get()
        assert word == "hi", word
    def test_capitalized(self):
        char_stream = phonemes.ListCharStream(lst=['H','h','a','i'])
        phoneme_stream = phonemes.PhonemeStream(charstream=char_stream)
        word_stream = phonemes.WordStream(phonemestream=phoneme_stream)
        word = word_stream.get() + word_stream.get()
        assert word == "Hi", word

if __name__ == '__main__':
    unittest.main()
    print("All tests pass\n")
