"""
The data structure that generates phonemes from a list of characters.
"""

from enum import Enum
import curses

class PhonemeEnums(Enum):
    p = 1
    t = 2
    k = 3
    tʃ = 4
    f = 5
    θ = 6
    s = 7
    ʃ = 8
    x = 9
    h = 10
    b = 11
    d = 12
    g = 13
    dʒ = 14
    v = 15
    ð = 16
    z = 17
    ʒ = 18
    m = 19
    n = 20
    ŋ = 21
    j = 22
    w = 23
    r = 24
    l = 25
    ɪ = 26
    ɛ = 27
    æ = 28
    ɑ = 29
    ʌ = 30
    ʊ = 31
    ɔ = 32
    ɜr = 33
    i = 34
    eɪ = 35
    oʊ = 36
    u = 37
    aɪ = 38
    ɔɪ = 39
    aʊ = 40
    ɪr = 41
    ɛr = 42
    ɑr = 43
    ɔr = 44
    Or = 45
    ʊr = 46
    ər = 47
    ə = 48


PHONEME_DICT = {
    "p": PhonemeEnums.p,
    "t": PhonemeEnums.t,
    "k": PhonemeEnums.k,
    "c": PhonemeEnums.tʃ,
    "f": PhonemeEnums.f,
    "q": PhonemeEnums.θ,
    "s": PhonemeEnums.s,
    "hs": PhonemeEnums.ʃ,
    "x": PhonemeEnums.x,
    "hh": PhonemeEnums.h,
    "b": PhonemeEnums.b,
    "d": PhonemeEnums.d,
    "g": PhonemeEnums.g,
    "j": PhonemeEnums.dʒ,
    "v": PhonemeEnums.v,
    "hq": PhonemeEnums.ð,
    "z": PhonemeEnums.z,
    "hz": PhonemeEnums.ʒ,
    "m": PhonemeEnums.m,
    "nn": PhonemeEnums.n,
    "ng": PhonemeEnums.ŋ,
    "yj": PhonemeEnums.j,
    "w": PhonemeEnums.w,
    "r": PhonemeEnums.r,
    "l": PhonemeEnums.l,

    "i": PhonemeEnums.ɪ,
    "e": PhonemeEnums.ɛ,
    "ae": PhonemeEnums.æ,
    "o": PhonemeEnums.ɑ,
    "u": PhonemeEnums.ʌ,
    "av": PhonemeEnums.ʊ,
    "aj": PhonemeEnums.ɔ,
    "an": PhonemeEnums.ɜr,
    "yi": PhonemeEnums.i,
    "aq": PhonemeEnums.eɪ,
    "ao": PhonemeEnums.oʊ,
    "au": PhonemeEnums.u,
    "ai": PhonemeEnums.aɪ,
    "yy": PhonemeEnums.ɔɪ,
    "ar": PhonemeEnums.aʊ,
    "az": PhonemeEnums.ɪr,
    "aw": PhonemeEnums.ɛr,
    "ap": PhonemeEnums.ɑr,
    "ad": PhonemeEnums.ɔr,
    "af": PhonemeEnums.Or,
    "am": PhonemeEnums.ʊr,
    "ax": PhonemeEnums.ər,
    "ab": PhonemeEnums.ə,
}

class CharacterStream:
    def __init__(self):
        self.characters = []

    def get(self, view, debug:chr=None):
        if not debug:
            view.keypad(True)
            key_input = view.getch()
            view.keypad(False)
            self.characters.append(chr(key_input))
        else:
            self.characters.append(debug)

class Phoneme:
    def __init__(self, phoneme:PhonemeEnums, capitalized:bool=False):
        self.phoneme = phoneme
        self.capitalized = capitalized

class PhonemeStream:
    def __init__(self):
        self.phonemes = []

    def get(self, charStream:CharacterStream, view, debug=None):
        char_buffer = []
        if not charStream.characters:
            charStream.get(view, debug=debug)
        char_buffer.append(charStream.characters.pop(0))
        buffer_as_str = ''.join(char_buffer)
        buffer_as_str_lowercased = buffer_as_str.lower()
        if buffer_as_str_lowercased in PHONEME_DICT:
            self.phonemes.append(Phoneme(phoneme=PHONEME_DICT[buffer_as_str_lowercased], capitalized=buffer_as_str_lowercased != buffer_as_str))

