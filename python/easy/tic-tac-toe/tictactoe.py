class TicTacToe:
    def __init__(self, init_string="_________"):
        self.matrix = []
        i = 0
        while i < 9:
            row = []
            for symbol in init_string[i:i + 3]:
                row.append(symbol)
            self.matrix.append(row)
            i += 3

    def __str__(self):
        result = "---------\n"
        for row in self.matrix:
            result += "| "
            result += " ".join(row)
            result += " |\n"
        result += "---------"
        return result

    def __get_win(self, symbol="X"):
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

    def __get_impossible(self):
        if self.__get_win() and self.__get_win("O"): return True
        x = 0
        o = 0
        for row in self.matrix:
            x += row.count("X")
            o += row.count("O")
        return not (0 <= abs(x - o) <= 1)

    def __get_draw(self):
        for row in self.matrix:
            for column in row:
                if column == "_":
                    return False
        return True

    def __check(self):
        if self.__get_impossible():
            print("Impossible")
            return True
        elif self.__get_win("X"):
            print("X wins")
            return True
        elif self.__get_win("O"):
            print("O wins")
            return True
        elif self.__get_draw():
            print("Draw")
            return True
        else:
            return False

    def __is_occupied(self, x, y):
        return self.matrix[x][y] != "_"

    def __set_coordinates(self, symbol="X"):
        while True:
            try:
                y, x = input("Enter the coordinates: ").split()
            except:
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
            if self.__is_occupied(x, y):
                print("This cell is occupied! Choose another one!")
                continue
            self.matrix[x][y] = symbol
            return self

    def __move(self, symbol="X"):
        print(self)
        if not self.__check():
            self.__set_coordinates(symbol)
            return False
        return True

    def main(self):
        have_won = False
        while not have_won:
            for c in ("X", "O"):
                if self.__move(c):
                    have_won = True
                    break


if __name__ == '__main__':
    game = TicTacToe()
    game.main()
