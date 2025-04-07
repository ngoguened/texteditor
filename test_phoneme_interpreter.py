from phoneme_interpreter_interface import PhonemeInterpreterInterface
from phonemes import PhonemeEnums

class TestPhonemeInterpreter(PhonemeInterpreterInterface):

    def interpret(self, phonemes):
        if len(phonemes) != 2:
            return []
        if phonemes[0].phoneme == PhonemeEnums.h and phonemes[1].phoneme == PhonemeEnums.aɪ:
            return ["hi", "high"]
        return []
