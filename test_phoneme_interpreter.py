from phoneme_interpreter_interface import PhonemeInterpreterInterface

class TestPhonemeInterpreter(PhonemeInterpreterInterface):

    def interpret(self, phonemes):
        return ["fee", "fie", "foe", "fum"] if phonemes else []
