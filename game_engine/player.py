# player.py
class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def place_piece(self, board):
        while True:
            row = int(input('Wpisz numer wiersza (0-2), gdzie chcesz postawić pionek: '))
            col = int(input('Wpisz numer kolumny (0-2), gdzie chcesz postawić pionek: '))
            if board[row][col] == ' ':
                return row, col
            else:
                print('To pole jest już zajęte, spróbuj ponownie.')

    def move_piece(self, board, player_pieces):
        while True:
            print('Wybierz pionek do przesunięcia:')
            for idx, (row, col) in enumerate(player_pieces):
                print(f'{idx}: Pionek na pozycji ({row}, {col})')
            piece_idx = int(input('Wpisz numer pionka, który chcesz przesunąć: '))
            if piece_idx < 0 or piece_idx >= len(player_pieces):
                print('Nieprawidłowy numer pionka, spróbuj ponownie.')
                continue
            row, col = player_pieces[piece_idx]
            new_row = int(input('Wpisz numer nowego wiersza (0-2): '))
            new_col = int(input('Wpisz numer nowej kolumny (0-2): '))
            if (new_row, new_col) not in player_pieces and board[new_row][new_col] == ' ':
                player_pieces[piece_idx] = (new_row, new_col)
                board[row][col] = ' '
                return new_row, new_col
            else:
                print(
                    'Nie możesz przesunąć pionka na zajęte pole lub na pole z pionkiem przeciwnika, spróbuj ponownie.')

class HumanPlayer(Player):
    def make_move(self, board):
        while True:
            try:
                row = int(input('Wpisz numer wiersza (0-2): '))
                col = int(input('Wpisz numer kolumny (0-2): '))
                if board[row][col] == ' ':
                    return row, col
                else:
                    print('To pole jest już zajęte, spróbuj ponownie.')
            except (ValueError, IndexError):
                print('Nieprawidłowe wartości, wpisz numer wiersza i kolumny jako liczby całkowite od 0 do 2.')


class ComputerPlayer(Player):
    def make_move(self, board):