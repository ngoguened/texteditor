"""
The data structure that generates phonemes from a list of characters.
"""

from enum import Enum
import curses

class PhonemeEnums(Enum):
    p = 128
    t = 129
    k = 130
    tʃ = 131
    f = 132
    θ = 133
    s = 134
    ʃ = 135
    x = 136
    h = 137
    b = 138
    d = 139
    g = 140
    dʒ = 141
    v = 142
    ð = 143
    z = 144
    ʒ = 145
    m = 146
    n = 147
    ŋ = 148
    j = 149
    w = 150
    r = 151
    l = 152
    ɪ = 153
    ɛ = 154
    æ = 155
    ɑ = 156
    ʌ = 157
    ʊ = 158
    ɔ = 159
    ɜr = 160
    i = 161
    eɪ = 162
    oʊ = 163
    u = 164
    aɪ = 165
    ɔɪ = 166
    aʊ = 167
    ɪr = 168
    ɛr = 169
    ɑr = 170
    ɔr = 171
    Or = 172
    ʊr = 173
    ər = 174
    ə = 175


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

class Phoneme:
    def __init__(self, phoneme:PhonemeEnums, capitalized:bool=False):
        self.phoneme = phoneme
        self.capitalized = capitalized

class ListCharStream:
    def __init__(self, lst):
        self.lst = lst
        self.phoneme_data = []

    def get(self):
        if self.lst:
            out = self.lst.pop(0)
            self.phoneme_data.append(out)
            return out
        return None

class KeypadCharStream:
    def __init__(self, view):
        self.view = view
        self.phoneme_data = []

    def get(self):
        self.view.keypad(True)
        key_input = self.view.getch()
        self.phoneme_data.append(chr(key_input))
        self.view.keypad(False)
        return chr(key_input)
    
    def consume_chars(self, chars, phoneme:Phoneme):
        self.phoneme_data = self.phoneme_data[:-len(chars)]
        self.phoneme_data.append(phoneme.phoneme.name)

    def consume_phonemes(self, phonemes):
        self.phoneme_data = self.phoneme_data[:-len(phonemes)]
    
    def get_phoneme_data(self) -> str:
        return ''.join(self.phoneme_data)

class PhonemeStream:
    def __init__(self, charstream):
        self.charstream = charstream

    def get(self):
        chars = ""
        while True:
            c = self.charstream.get()
            if not c:
                return None
            chars += c
            if c.isalpha():
                if chars.lower() in PHONEME_DICT:
                    out = Phoneme(phoneme=PHONEME_DICT[chars.lower()], capitalized=chars[0].isupper())
                    self.charstream.consume_chars(chars, out)
                    return out
            else:
                return c
            
    def get_phoneme_data(self) -> str:
        return self.charstream.get_phoneme_data()

class WordStream:
    def __init__(self, phonemestream:PhonemeStream, dictionary:dict):
        self.phonemestream = phonemestream
        self.dictionary = dictionary # Tuple(PhonemeEnum):string
        self.word_buffer = None
    
    def get(self):
        phonemes_and_punctuation = []
        while not self.word_buffer:
            phoneme_or_punctuation = self.phonemestream.get()
            if not phoneme_or_punctuation:
                return None
            phonemes_and_punctuation.append(phoneme_or_punctuation)
            if isinstance(phoneme_or_punctuation, Phoneme):
                curr_phonemes = [p.phoneme for p in phonemes_and_punctuation]
                if tuple(curr_phonemes) in self.dictionary:
                    self.phonemestream.charstream.consume_phonemes(curr_phonemes)
                    self.word_buffer = self.dictionary[tuple(curr_phonemes)]
                    if phonemes_and_punctuation[0].capitalized:
                        self.word_buffer = self.word_buffer[0].capitalize() + self.word_buffer[1:]
            else:
                self.word_buffer = phoneme_or_punctuation
        ret, self.word_buffer = self.word_buffer[0], self.word_buffer[1:]
        return ret

    def get_phoneme_data(self) -> str:
        return self.phonemestream.get_phoneme_data()
