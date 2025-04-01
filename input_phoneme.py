from phonemes import Phoneme, PHONEME_DICT
from phoneme_interpreter_interface import PhonemeInterpreterInterface

class InputPhoneme:
    def __init__(self, interpreter:PhonemeInterpreterInterface):
        self.phoneme_interpreter = interpreter
        self.phonemes:list[Phoneme] = []
        self.chars:list[str] = []
        self.word_lst:list[str] = []
        self.word_idx = 0

    def lower_and_join_chars(self) -> str:
        return ''.join([c.lower() for c in self.chars])

    def update_word_idx(self, inc):
        self.word_idx = (self.word_idx + inc) % len(self.word_lst)

    def cycle_word_lst(self, clockwise:bool):
        if clockwise:
            self.update_word_idx(1)
        else:
            self.update_word_idx(-1)

    def update_word(self) -> str:
        self.word_lst = self.phoneme_interpreter.interpret(self.phonemes)
        if self.word_lst:
            word = self.word_lst[self.word_idx]
            if self.phonemes[0].capitalized:
                word = word.capitalize()
            return word
        return ""

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
        curr_phonemes = ''.join([phoneme.phoneme.name for phoneme in self.phonemes])
        curr_chars = ''.join(self.chars)
        curr_word = self.update_word()
        return curr_phonemes + curr_chars + "\n" + curr_word
    
    def complete(self) -> str:
        out = self.update_word()
        self.phonemes = []
        self.chars = []
        return out

    def is_chars_empty(self) -> bool:
        return not self.chars

    def is_phonemes_empty(self) -> bool:
        return not self.phonemes
    
    def is_word_lst_empty(self) -> bool:
        return not self.word_lst