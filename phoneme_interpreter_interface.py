'''
PhonemeInterpreter is essentially a wrapper for the model I choose to use 
and methods to add context (the rest of the document, as a string. This will 
only be used when the input is very long), prompt (the string describing the 
task to the LLM), and input (the list of editable words)
'''
class PhonemeInterpreterInterface:
    def __init__(self, llm:str=None, context:str=None):
        self.llm = llm # The llm api provider takes the model name as input.
        self.context = context

    def interpret(self, input:str) -> str:
        return None

    def set_context(self, text:str):
        pass

    def add_context(self, text:str):
        pass