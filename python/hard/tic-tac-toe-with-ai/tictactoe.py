import random
from enum import Enum


class MenuChoice(Enum):
    START = "start"
    EXIT = "exit"


class PlayerType(Enum):
    USER = "user"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Figure(Enum):
    X_SYMBOL = "X"
    O_SYMBOL = "O"
    EMPTY = " "


class Player:
    def __init__(self, name, symbol, board):
        self.figure = symbol
        self.board = board
        self.name = name

    def get_figure(self):
        return self.figure

    def move(self):
        pass


class User(Player):
    def move(self):
        while True:
            try:
                y, x = input("Enter the coordinates: ").split()
            except ValueError:
                print("You should enter numbers!")
                continue
            if x.isdigit() and y.isdigit():
                x = int(x)
                y = int(y)
            else:
                print("You should enter numbers!")
                continue
            if 1 <= x <= 3 and 1 <= y <= 3:
                x = -x
                y -= 1
            else:
                print("Coordinates should be from 1 to 3!")
                continue
            return x, y


class EasyComputer(Player):
    def move(self):
        return self._get_random_coordinates()

    def _get_random_coordinates(self):
        values = []
        for _ in range(2):
            values.append(random.randint(0, 2))
        return values


class MediumComputer(EasyComputer):
    def __init__(self, name, symbol, board):
        super().__init__(name, symbol, board)
        self.__win_move = None

    def move(self):
        if self.__can_win(self.get_figure()):
            return self.__win_move
        opponent_figure = Figure.O_SYMBOL
        if self.get_figure() == Figure.O_SYMBOL:
            opponent_figure = Figure.X_SYMBOL
        if self.__can_win(opponent_figure):
            return self.__win_move
        return self._get_random_coordinates()

    def __can_win(self, figure):
        figure = figure.value
        diagonal = []
        diagonal_coord = []
        for i, row in enumerate(self.board.matrix):
            horizontal = []
            horizontal_coord = []
            if row.count(figure) == 2 and row.count(Figure.EMPTY) == 1:
                self.__win_move = row.index(Figure.EMPTY)
                return True
            for j, cell in enumerate(row):
                horizontal.append(self.board.matrix[j][i])
                horizontal_coord.append((j, i))
                if j + i == 2:
                    diagonal.append(cell)
                    diagonal_coord.append((i, j))
            if horizontal.count(figure) == 2 and horizontal.count(Figure.EMPTY) == 1:
                ind = horizontal.index(Figure.EMPTY)
                self.__win_move = horizontal_coord[ind]
                return True
        if diagonal.count(figure) == 2 and diagonal.count(Figure.EMPTY) == 1:
            ind = diagonal.index(Figure.EMPTY)
            self.__win_move = diagonal_coord[ind]
            return True
        horizontal = []
        for i in range(3):
            horizontal.append(self.board.matrix[i][i])
        if horizontal.count(figure) == 2 and horizontal.count(Figure.EMPTY) == 1:
            self.__win_move = horizontal.index(Figure.EMPTY)
            return True
        return False


class HardComputer(MediumComputer):
    def move(self):
        board = self.board # copy
        scores_of_moves = []
        available_moves = self.board.free_moves()

        for cell in available_moves:
            scores_of_moves.append(self.__get_score(board, True, *cell))

        best_move_index = scores_of_moves.index(max(scores_of_moves))
        cell = available_moves[best_move_index]
        return cell

    def __get_score(self, board, is_player, *cell):
        if is_player:
            symbol = Figure.X_SYMBOL if self.get_figure() == Figure.X_SYMBOL else Figure.O_SYMBOL
        else:
            symbol = Figure.O_SYMBOL if self.get_figure() == Figure.X_SYMBOL else Figure.X_SYMBOL
        x, y = cell
        board.matrix[x][y] = symbol
        score = self.__minimax(board, is_player)
        board.matrix[x][y] = Figure.EMPTY
        return score

    def __minimax(self, board, is_player):
        check = board.check()
        if check == "Draw":
            return 0
        if  check == self.get_figure():
            return 10
        if check != self.get_figure():
            return -10

        available_moves = board.free_moves()
        scores_of_moves = []

        for cell in available_moves:
            if is_player:
                score = self.__get_score(board, False, *cell)
                if score == -10:
                    return score
            else:
                score = self.__get_score(board, True, *cell)
                if score == 10:
                    return score
            scores_of_moves.append(score)

        if is_player:
            return min(scores_of_moves)
        return max(scores_of_moves)


class TicTacToe:
    def __init__(self, init_string=""):
        self.matrix = []
        if not init_string:
            self.create_board(init_string)
        else:
            self.create_board(Figure.EMPTY.value * 9)

    def __str__(self):
        result = "---------\n"
        for row in self.matrix:
            result += "| "
            result += " ".join(figure.value for figure in row)
            result += " |\n"
        result += "---------"
        return result

    def __get_impossible(self):
        if self.get_win() and self.get_win(Figure.O_SYMBOL):
            return True
        x = 0
        o = 0
        for row in self.matrix:
            x += row.count(Figure.X_SYMBOL)
            o += row.count(Figure.O_SYMBOL)
        return not (0 <= abs(x - o) <= 1)

    def __get_draw(self):
        for row in self.matrix:
            for column in row:
                if column == Figure.EMPTY:
                    return False
        return True

    def check(self):
        if self.__get_impossible():
            return "Impossible"
        elif self.get_win(Figure.X_SYMBOL):
            return Figure.X_SYMBOL
        elif self.get_win(Figure.O_SYMBOL):
            return Figure.O_SYMBOL
        elif self.__get_draw():
            return "Draw"
        else:
            return False

    def __check_with_message(self):
        if self.__get_impossible():
            print("Impossible")
            return "Impossible"
        elif self.get_win(Figure.X_SYMBOL):
            print("X wins")
            return True
        elif self.get_win(Figure.O_SYMBOL):
            print("O wins")
            return True
        elif self.__get_draw():
            print("Draw")
            return True
        else:
            return False

    def __is_occupied(self, x, y):
        return self.matrix[x][y] != Figure.EMPTY

    def get_win(self, symbol=Figure.X_SYMBOL):
        checked = [symbol] * 3
        diagonal = []
        for i, row in enumerate(self.matrix):
            if row == checked:
                return True
            horizontal = []
            for j, column in enumerate(row):
                horizontal.append(self.matrix[j][i])
                if j + i == 2:
                    diagonal.append(column)
            if horizontal == checked:
                return True
        if diagonal == checked:
            return True
        diagonal = []
        for i in range(3):
            diagonal.append(self.matrix[i][i])
        if diagonal == checked:
            return True

    def free_moves(self):
        return [[i, k] for i in range(3) for k in range(3) if self.matrix[i][k] == Figure.EMPTY]

    def get_player(self, player_type, figure):
        players_type = (
            PlayerType.USER,
            PlayerType.EASY,
            PlayerType.MEDIUM,
            PlayerType.HARD
        )
        players = (
            User,
            EasyComputer,
            MediumComputer,
            HardComputer
        )
        names = (
            "user",
            "easy",
            "medium",
            "hard"
        )
        for _type, player, name in zip(players_type, players, names):
            if _type == player_type:
                return player(name, figure, self)

    def turn(self, player):
        print(self)
        if not self.__check_with_message():
            self.set_figure(player)
            return False
        return True

    def start(self, first_figure: PlayerType, second_figure: PlayerType):
        first_player = self.get_player(first_figure, Figure.X_SYMBOL)
        second_player = self.get_player(second_figure, Figure.O_SYMBOL)
        have_won = False
        moves = (first_player, second_player)
        while not have_won:
            for player in moves:
                if self.turn(player):
                    have_won = True
                    break
        self.clear_board()

    def set_figure(self, player):
        x, y = player.move()
        while True:
            if self.__is_occupied(x, y):
                if isinstance(player, User):
                    print("This cell is occupied! Choose another one!")
                x, y = player.move()
            else:
                break
        self.matrix[x][y] = player.get_figure()
        if isinstance(player, EasyComputer):
            print(f'Making move level "{player.name}"')

    def clear_board(self):
        for i, row in enumerate(self.matrix):
            for j, column in enumerate(self.matrix[i]):
                self.matrix[i][j] = Figure.EMPTY

    def create_board(self, init_string):
        i = 0
        while i < 9:
            row = []
            for symbol in init_string[i:i + 3]:
                row.append(Figure(symbol))
            self.matrix.append(row)
            i += 3

    def main(self):
        while True:
            try:
                commands = input("Input command: ").split()
                command = MenuChoice(commands[0])
                if command == MenuChoice.EXIT:
                    break
                first = PlayerType(commands[1])
                second = PlayerType(commands[2])
                if command == MenuChoice.START:
                    self.start(first, second)
            except (ValueError, IndexError):
                print("Bad parameters")


if __name__ == '__main__':
    game = TicTacToe("_" * 9)
    game.main()
