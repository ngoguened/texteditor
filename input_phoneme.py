from phonemeKeyboard.phonemes import Phoneme, PhonemeEnums, PHONEME_DICT

class InputPhoneme:
    def __init__(self, word_dict):
        self.phonemes:list[Phoneme] = []
        self.chars:list[str] = []
        self.word_dict = word_dict

    def lower_and_join_chars(self) -> str:
        return ''.join([c.lower() for c in self.chars])

    def update_word(self) -> str:
        phoneme_enums:tuple[PhonemeEnums] = tuple([p.phoneme for p in self.phonemes])
        if phoneme_enums in self.word_dict:
            word:str = self.word_dict[phoneme_enums]
            if self.phonemes[0].capitalized:
                word = word.capitalize()
            return word
        return None

    def update_phonemes(self, char:str) -> str:
        if not char.isalpha():
            raise ValueError("Non-alphabetical characters cannot generate a phoneme.")
        self.chars.append(char)
        if self.lower_and_join_chars() in PHONEME_DICT:
            self.phonemes.append(Phoneme(phoneme=PHONEME_DICT[self.lower_and_join_chars()], capitalized=self.chars[0].isupper()))
            self.chars = []
            return self.update_word()
        elif len(self.chars) > 2:
            raise ValueError("There cannot be more than 2 values in chars.")

    def get_panel_text(self) -> str:
        return ''.join([phoneme.phoneme.name for phoneme in self.phonemes]) + ''.join(self.chars)
    
    def complete(self) -> str:
        out = self.update_word()
        self.phonemes = []
        self.chars = []
        return out

    def is_chars_empty(self) -> bool:
        return not self.chars

    def is_phonemes_empty(self) -> bool:
        return not self.phonemes