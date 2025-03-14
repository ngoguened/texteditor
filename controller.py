import curses
from text_editor import WindowedLines
from view import View

class Controller:
    """The connection between the model and the view"""
    def __init__(self, model:WindowedLines, view:View, window:curses.window):
        self.model = model
        self.view = view
        self.window = window

    def run(self):
        "the loop connecting the model to user input, displayed using a curses view."
        curses.noecho()
        curses.cbreak()
        curses.raw()

        while self.model.is_running():
            self.model.putch(self.window.getch())
            self.view.update(model=self.model)

        curses.nocbreak()
        curses.echo()
        curses.endwin()
