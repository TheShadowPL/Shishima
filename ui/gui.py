import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import askyesno


class GameUI(tk.Tk):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.title('Game Interface')
        self.canvas = tk.Canvas(self, width=300, height=300)
        self.canvas.pack()
        self.status_label = tk.Label(self, text="Player 1", font=("Helvetica", 16))
        self.status_label.pack()
        self.selected_piece = None
        self.draw_board()
        self.update_pieces()
        self.canvas.bind("<Button-1>", self.on_click)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        answer = askyesno("Game", "Do you want to save your game?")
        if answer:
            file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                     filetypes=[("JSON files", "*.json")],
                                                     title="Save Game As")
            if file_path:
                self.engine.save_game(file_path)

        self.destroy()
        self.quit()
    def check_end(self):
        if self.engine.check_winner():
            winner = self.engine.current_player
            message = f"Player {winner} won!" if winner != "Draw" else "Draw!"
            self.end_game(message)
        else:
            self.engine.switch_player()
            self.update_status_label()

    def draw_board(self):
        self.canvas.create_rectangle(50, 50, 250, 250, outline='black')
        self.outer_positions = [(50, 50), (150, 50), (250, 50), (250, 150), (250, 250), (150, 250), (50, 250), (50, 150)]
        for pos in self.outer_positions:
            x, y = pos
            self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, outline='black')
        self.center_position = (150, 150)
        self.canvas.create_rectangle(130, 130, 170, 170, fill='blue', outline='black')

    def update_pieces(self):
        game_state = self.engine.get_game_state()
        positions = game_state['positions']
        current_player = game_state['current_player']
        game_over = game_state['game_over']

        self.canvas.delete('piece')
        for i, pos in enumerate(self.outer_positions + [self.center_position]):
            x, y = pos
            piece = positions[i]
            if piece:
                color = 'purple' if piece == 'Gracz 1' else 'orange'
                self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill=color, outline='black', tags='piece')

        if game_over:
            winner_message = f"Player {current_player} won!" if game_state['winner'] else "Draw!"
            self.status_label.config(text=winner_message)
        else:
            self.status_label.config(text=f"Player {current_player} turn")

    def on_click(self, event):
        if self.engine.game_over:
            return
        clicked_index = self.get_clicked_index(event.x, event.y)
        if clicked_index is not None:
            if self.selected_piece is None:
                if self.engine.positions[clicked_index] == self.engine.current_player:
                    self.selected_piece = clicked_index
                    self.highlight_piece(clicked_index)
            else:
                if clicked_index == self.selected_piece:
                    self.canvas.delete('highlight')
                    self.selected_piece = None
                else:
                    if self.engine.make_move(self.selected_piece, clicked_index):
                        self.canvas.delete('highlight')
                        if self.engine.check_winner():
                            self.end_game(f"Player {self.engine.current_player} won!")
                        self.update_pieces()
                    else:
                        self.canvas.delete('highlight')
                        self.selected_piece = None
                        if self.engine.positions[clicked_index] == self.engine.current_player:
                            self.selected_piece = clicked_index
                            self.highlight_piece(clicked_index)

    def get_clicked_index(self, x, y):
        for i, pos in enumerate(self.outer_positions + [self.center_position]):
            px, py = pos
            if (px - 20 < x < px + 20) and (py - 20 < y < py + 20):
                return i
        return None

    def highlight_piece(self, index):
        x, y = self.outer_positions[index] if index < 8 else self.center_position
        self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill='grey', outline='red', tags='highlight')

    def end_game(self, message):
        self.engine.game_over = True
        self.update_status_label(message)

    def update_status_label(self, message=None):
        if message:
            self.status_label.config(text=message)
        else:
            text = "Player X's turn" if self.engine.current_player == 'X' else "Player O's turn"
            if self.engine.game_over:
                text = "Player X won!" if self.engine.current_player == 'X' else "Player O won!"
            self.status_label.config(text=text)
