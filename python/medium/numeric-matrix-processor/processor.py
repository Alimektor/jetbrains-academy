import enum
import math

def get_number(number):
    try:
        number = float(number)
    except:
        raise ValueError("Input should be a number.")
    if number == int(number):
        number = int(number)
    return number


def get_truncated_number(number, after):
    number = math.trunc(get_number(number) * 10 ** after)
    return number / 10 ** after


class Choices(enum.Enum):
    EXIT = 0
    ADDING = 1
    MULTIPLY_BY_CONSTANT = 2
    MULTIPLY_MATRICES = 3
    TRANSPOSED = 4
    DETERMINANT = 5
    INVERSE = 6


class TransposedChoices(enum.Enum):
    MAIN = 1
    SIDE = 2
    VERTICAL = 3
    HORIZONTAL = 4


class Matrix:
    def __init__(self, n, m):
        self.__matrix = []
        for row in range(n):
            self.__matrix.append([])
            for cell in range(m):
                self.__matrix[row].append(0)

    def __len__(self):
        return len(self.__matrix)

    def __getitem__(self, row):
        return self.__matrix[row]

    def __setitem__(self, row, value):
        self.__matrix[row] = value

    def __delitem__(self, key):
        del self.__matrix[key]

    def __iter__(self):
        return iter(self.__matrix)

    def __reversed__(self):
        return reversed(self.__matrix)

    def __str__(self):
        result = ""

        for row in self:
            for cell in row:
                result += f"{cell} "
            result += "\n"

        return result

    def get_rows(self):
        return len(self)

    def get_columns(self):
        return len(self[0])

    def __add_matrix(self, other):
        try:
            result = Matrix(len(self), len(self[0]))
            if (len(self) != len(other)) or (len(self[0]) != len(other[0])):
                raise ValueError("The matrices must be equal.")
            for irow, row in enumerate(self):
                for icell, cell in enumerate(self[irow]):
                    result[irow][icell] = self[irow][icell] + other[irow][icell]
            return result
        except:
            return "ERROR"

    def __mul_number(self, other):
        result = Matrix(len(self), len(self[0]))
        for irow, row in enumerate(self):
            for icell, cell in enumerate(self[irow]):
                result[irow][icell] = self[irow][icell] * other
        return result

    def __mul_matrices(self, other):
        if self.get_columns() != other.get_rows():
            return "The operation cannot be performed."
        result = Matrix(self.get_rows(), other.get_columns())
        for i_first_row in range(self.get_rows()):
            for i_second_column in range(other.get_columns()):
                dot = 0
                for i_cell in range(self.get_columns()):
                    dot += self[i_first_row][i_cell] * other[i_cell][i_second_column]
                result[i_first_row][i_second_column] = dot
        return result

    def __add__(self, other):
        if isinstance(other, Matrix):
            return self.__add_matrix(other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul_number(other)
        if isinstance(other, Matrix):
            return self.__mul_matrices(other)

    def get_numbers(self, number=2):
        self.buffer = input().split()
        if len(self.buffer) != number:
            raise ValueError(f"The number must be {number}.")
        try:
            self.buffer = list(map(get_number, self.buffer))
        except:
            print("Something wrong with numbers.")
        return self.buffer

    def set_values(self):
        for i_row, row in enumerate(self):
            cells = self.get_numbers(len(self[i_row]))
            for i_cell, cell in enumerate(self[i_row]):
                self[i_row][i_cell] = cells[i_cell]

    def get_main_transposed(self):
        result = Matrix(self.get_columns(), self.get_rows())
        for i_row in range(self.get_rows()):
            for i_column in range(self.get_columns()):
                result[i_column][i_row] = self[i_row][i_column]
        return result

    def get_side_transposed(self):
        result = self.get_main_transposed().get_horizontal_transposed().get_vertical_transposed()
        return result

    def get_vertical_transposed(self):
        result = Matrix(self.get_rows(), self.get_columns())
        for i_row in range(self.get_rows()):
            result[i_row] = reversed(self[i_row])
        return result

    def get_horizontal_transposed(self):
        result = Matrix(self.get_rows(), self.get_columns())
        for i_row in range(self.get_rows()):
            result[result.get_rows() - i_row - 1] = self[i_row]
        return result

    def copy_matrix(self):
        copied = Matrix(self.get_rows(), self.get_columns())
        for i_row in range(copied.get_rows()):
            for i_cell in range(copied.get_columns()):
                copied[i_row][i_cell] = self[i_row][i_cell]
        return copied

    def get_determinant(self):
        copied_matrix = self.copy_matrix()
        temp = []
        for i in range(len(copied_matrix)):
            temp.append(0)
        total = 1
        det = 1
        n = copied_matrix.get_rows()
        for i in range(0, len(copied_matrix)):
            index = i
            while copied_matrix[index][i] == 0 and index < len(copied_matrix):
                index += 1
            if index == len(copied_matrix):
                continue
            if index != i:
                for j in range(0, n):
                    copied_matrix[index][j], copied_matrix[i][j] = copied_matrix[i][j], copied_matrix[index][j]
                det = det * int(pow(-1, index - i))
            for j in range(0, n):
                temp[j] = copied_matrix[i][j]
            for j in range(i + 1, n):
                num1 = temp[i]
                num2 = copied_matrix[j][i]
                for k in range(0, n):
                    copied_matrix[j][k] = (num1 * copied_matrix[j][k]) - (num2 * temp[k])
                total = total * num1

        for i in range(0, n):
            det = det * copied_matrix[i][i]
        return get_number(det / total)

    def get_inversed(self):
        if not self.check_squareness() or not self.check_non_singular():
            print("This matrix doesn't have an inverse.\n")
            return None
        li = self.getMatrixInverse(self.copy_matrix())
        result = Matrix(self.get_rows(), self.get_columns())
        for i in range(len(li)):
            for j in range(len(li[0])):
                result[i][j] = get_truncated_number(li[i][j], 2)
        return result

    def transposeMatrix(self, m):
        return list(map(list, zip(*m)))

    def getMatrixMinor(self, m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    def getMatrixDeternminant(self, m):
        # base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1) ** c) * m[0][c] * self.getMatrixDeternminant(self.getMatrixMinor(m, 0, c))
        return determinant

    def getMatrixInverse(self, m):
        determinant = self.getMatrixDeternminant(m)
        # special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                    [-1 * m[1][0] / determinant, m[0][0] / determinant]]

        # find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m, r, c)
                cofactorRow.append(((-1) ** (r + c)) * self.getMatrixDeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = (cofactors[r][c] / determinant)
        return cofactors

    def check_squareness(self):
        return self.get_rows() == self.get_columns()

    def check_non_singular(self):
        try:
            return self.get_determinant() != 0
        except:
            return False

    def get_identity_matrix(self, length):
        result = Matrix(length, length)
        for i in range(length):
            for j in range(length):
                if i == j:
                    result[i][j] = 1
        return result


class App:
    def __init__(self):
        self.result = []
        self.choice = None
        self.tranposed_choice = None

    def show_menu(self):
        print("1. Add matrices")
        print("2. Multiply matrix by constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        print("0. Exit")
        print("Your choice: ", end="")
        choice = int(input())
        self.choice = Choices(choice)

    def get_choice(self):
        return self.choice

    def get_size_of_matrices(self, what=""):
        print(f"Enter size of {what}matrix: ", end="")
        row, column = input().split()
        return int(row), int(column)

    def get_matrix(self, row, column, what=""):
        matrix = Matrix(row, column)
        print(f"Enter {what}matrix:")
        matrix.set_values()
        return matrix

    def get_constant(self):
        print("Enter constant: ", end="")
        result = input()
        return get_number(result)

    def get_result(self, result):
        if result is not None:
            print("The result is:")
            print(result)

    def show_transposed_menu(self):
        print()
        print("1. Main diagonal")
        print("2. Side diagonal")
        print("3. Vertical line")
        print("4. Horizontal line")
        print("Your choice: ", end="")
        choice = int(input())
        self.tranposed_choice = TransposedChoices(choice)

    def get_transposed_choice(self):
        return self.tranposed_choice


if __name__ == '__main__':
    app = App()
    while app.get_choice() != Choices.EXIT:
        app.show_menu()
        if app.get_choice() == Choices.ADDING:
            n1, m1 = app.get_size_of_matrices("number ")
            first = app.get_matrix(n1, m1, "number ")
            n2, m2 = app.get_size_of_matrices("base ")
            second = app.get_matrix(n1, m1, "base ")
            app.get_result(first + second)
        if app.get_choice() == Choices.MULTIPLY_BY_CONSTANT:
            n, m = app.get_size_of_matrices()
            matrix = app.get_matrix(n, m)
            c = app.get_constant()
            app.get_result(matrix * c)
        if app.get_choice() == Choices.MULTIPLY_MATRICES:
            n1, m1 = app.get_size_of_matrices("number ")
            first = app.get_matrix(n1, m1, "number ")
            n2, m2 = app.get_size_of_matrices("base ")
            second = app.get_matrix(n2, m2, "base ")
            app.get_result(first * second)
        if app.get_choice() == Choices.TRANSPOSED:
            app.show_transposed_menu()
            n, m = app.get_size_of_matrices()
            matrix = app.get_matrix(n, m)
            if app.get_transposed_choice() == TransposedChoices.MAIN:
                print(matrix.get_main_transposed())
            if app.get_transposed_choice() == TransposedChoices.SIDE:
                print(matrix.get_side_transposed())
            if app.get_transposed_choice() == TransposedChoices.VERTICAL:
                print(matrix.get_vertical_transposed())
            if app.get_transposed_choice() == TransposedChoices.HORIZONTAL:
                print(matrix.get_horizontal_transposed())
        if app.get_choice() == Choices.DETERMINANT:
            n, m = app.get_size_of_matrices()
            matrix = app.get_matrix(n, m)
            app.get_result(matrix.get_determinant())
        if app.get_choice() == Choices.INVERSE:
            n, m = app.get_size_of_matrices()
            matrix = app.get_matrix(n, m)
            app.get_result(matrix.get_inversed())
