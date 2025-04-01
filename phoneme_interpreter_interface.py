'''
PhonemeInterpreterInterface is an interface for implementations that replace the stream of phonemes
entered by the user with a list of possible words that the stream of phonemes could represent.
The order is potentially meaningful.
'''
from phonemes import Phoneme

class PhonemeInterpreterInterface:
    def interpret(self, phonemes:list[Phoneme]) -> list[str]:
        return None
