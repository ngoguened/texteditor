import curses
from model import WindowedLines

class View:
    def __init__(self, window:curses.window):
        self.window = window
        self.phoneme_panel:curses.window = None

    def toggle_panel(self, model:WindowedLines) -> curses.window:
        if model.get_phoneme_mode():
            self.phoneme_panel = self.window.subwin(self.window.getmaxyx()[0]-5, 0)
            self.phoneme_panel.refresh()
        else:
            self.phoneme_panel = None
        return self.phoneme_panel

    def add_str_to_window(self, text:str):
        self.window.addstr(text)
        self.window.refresh()

    def update_panel(self, text:str):
        if self.phoneme_panel:
            self.phoneme_panel.addstr(text)
            self.phoneme_panel.refresh()

    def update(self, model:WindowedLines):
        self.window.erase()
        self.window.addstr(model.print_window())
        self.window.move(len(model.prev_lines)-model.top_window_row,min(model.cursor_position, model.window_size[1]))
        self.window.refresh()
        self.update_panel(text=model.get_panel_text())
        self.toggle_panel(model=model)
