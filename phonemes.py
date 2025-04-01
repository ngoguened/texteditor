"""
The data structure that generates phonemes from a list of characters.
"""

from enum import Enum

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