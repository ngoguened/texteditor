from phoneme_interpreter_interface import PhonemeInterpreterInterface
from phonemeKeyboard.phonemes import PhonemeEnums, Phoneme

class DictPhonemeInterpreter(PhonemeInterpreterInterface):
    def __init__(self, word_dict):
        self.word_dict = word_dict
    
    def interpret(self, phonemes:list[Phoneme]):
        phoneme_enums:tuple[PhonemeEnums] = tuple([p.phoneme for p in phonemes])
        if phoneme_enums in self.word_dict:
            return self.word_dict[phoneme_enums]
        return []