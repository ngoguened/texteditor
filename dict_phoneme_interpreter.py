import pickle
from phonemes import PhonemeEnums, Phoneme
from phoneme_interpreter_interface import PhonemeInterpreterInterface

with open('saved_dictionary.pkl', 'rb') as f:
    word_dict = pickle.load(f)

class DictPhonemeInterpreter(PhonemeInterpreterInterface):
    def __init__(self):
        self.word_dict = word_dict
    
    def interpret(self, phonemes:list[Phoneme]):
        phoneme_enums:tuple[PhonemeEnums] = tuple([p.phoneme for p in phonemes])
        if phoneme_enums in self.word_dict:
            return self.word_dict[phoneme_enums]
        return []