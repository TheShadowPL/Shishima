import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.messagebox import askyesno

from game_engine.engine import GameEngine
from ui.gui import GameUI


def main():
    question = askyesno("Shisima", "Do you want to load previous game?")
    root = tk.Tk()
    root.withdraw()


    if question:
        load_game_path = filedialog.askopenfilename(title="Select saved game", filetypes=[("JSON files", "*.json")])
    else:
        load_game_path = None

    game_engine = GameEngine()
    if load_game_path:
        try:
            game_engine.load_game(load_game_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {e}")
            return

    game_ui = GameUI(game_engine)
    game_ui.eval('tk::PlaceWindow . center')
    game_ui.mainloop()


if __name__ == "__main__":
    main()
