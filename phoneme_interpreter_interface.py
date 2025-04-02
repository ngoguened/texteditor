'''
PhonemeInterpreterInterface is an interface where given a sequence of phonemes entered by the user,
implementations suggest a list of possible words that those phonemes could represent.
The order is potentially meaningful.
'''
from phonemes import Phoneme

class PhonemeInterpreterInterface:
    def interpret(self, phonemes:list[Phoneme]) -> list[str]:
        return None
