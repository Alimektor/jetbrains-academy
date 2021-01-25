package tictactoe;

import java.util.ArrayList;

public class Board {
    private final Figure[][] matrix;
    private final int boardLength = 3;

    public Board(String init) {
        matrix = new Figure[boardLength][boardLength];
        this.createBoard(init);
    }

    public Board() {
        matrix = new Figure[boardLength][boardLength];
        this.createBoard();
    }

    public Board(Board board) {
        this(board.getInitString());
    }

    public String getInitString() {
        StringBuilder stringBuilder = new StringBuilder();
        for (int row = 1; row <= this.getLength(); row++) {
            for (int column = 1; column <= this.getLength(); column++) {
                stringBuilder.append(this.getFigure(row, column).getSymbol());
            }
        }
        return stringBuilder.toString();
    }

    public void setCell(Coordinate coordinate, Figure value) {
        this.matrix[coordinate.getX() - 1][coordinate.getY() - 1] = value;
    }

    public void setFigure(Coordinate coordinate, Figure figure) {
        if (this.isOccupied(coordinate))
            throw new IllegalArgumentException("This cell is occupied! Choose another one!");
        this.setCell(coordinate, figure);
    }


    public Figure getFigure(Coordinate coordinate) {
        return this.matrix[coordinate.getX() - 1][coordinate.getY() - 1];
    }

    public Figure getFigure(int x, int y) {
        return this.matrix[x - 1][y - 1];
    }

    private void createBoard() {
        for (int row = 1; row <= this.getLength(); row++) {
            for (int column = 1; column <= this.getLength(); column++) {
                this.setCell(new Coordinate(row, column), Figure.EMPTY);
            }
        }
    }

    private void createBoard(String init) {
        int current = 0;
        for (int row = 1; row <= this.getLength(); row++) {
            for (int column = 1; column <= this.getLength(); column++) {
                Figure figure = Figure.setFigure(init.charAt(current));
                this.setCell(new Coordinate(row, column), figure);
                current++;
            }
        }
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder("---------\n");

        for (Figure[] figures : this.matrix) {
            result.append("|");
            for (int j = 0; j < this.getLength(); j++) {
                result.append(" ").append(figures[j].getSymbol());
            }
            result.append(" |\n");
        }

        result.append("---------");

        return result.toString();
    }

    public Figure getWhoseMove() {
        if (this.getFigureNumbers(Figure.X_SYMBOL) > this.getFigureNumbers(Figure.O_SYMBOL))
            return Figure.O_SYMBOL;
        return Figure.X_SYMBOL;
    }

    public State check() {
        if (this.getImpossible()) {
            return State.Immpossible;
        }
        if (this.getWin(Figure.X_SYMBOL)) {
            return State.xWins;
        }
        if (this.getWin(Figure.O_SYMBOL)) {
            return State.oWins;
        }
        if (this.getDraw()) {
            return State.Draw;
        }
        return State.NotFinished;
    }

    public int getLength() {
        return this.matrix.length;
    }

    private int getFigureNumbers(Figure figure) {
        int count = 0;
        for (int row = 1; row <= this.getLength(); row++) {
            for (int column = 1; column <= this.getLength(); column++) {
                if (this.getFigure(row, column) == figure)
                    count++;
            }
        }
        return count;
    }

    private boolean isOccupied(Coordinate coordinate) {
        return this.getFigure(coordinate) != Figure.EMPTY;
    }

    private boolean getDraw() {
        for (int row = 1; row <= this.getLength(); row++) {
            for (int column = 1; column <= this.getLength(); column++) {
                if (this.getFigure(row, column) == Figure.EMPTY)
                    return false;
            }
        }
        return true;
    }

    private boolean getWin(Figure figure) {
        for (int row = 1; row <= this.getLength(); row++) {
            if (this.getCountOnRow(figure, row) == this.getLength())
                return true;
        }

        for (int column = 1; column <= this.getLength(); column++) {
            if (this.getCountOnColumn(figure, column) == this.getLength())
                    return true;
        }

        if (this.getCountOnMainDiagonal(figure) == this.getLength())
            return true;

        return this.getCountOnSideDiagonal(figure) == this.getLength();
    }

    private boolean getImpossible() {
        if (this.getWin(Figure.X_SYMBOL) && this.getWin(Figure.O_SYMBOL)) {
            return true;
        }

        int xCount = 0;
        int oCount = 0;

        xCount += this.getFigureNumbers(Figure.X_SYMBOL);
        oCount += this.getFigureNumbers(Figure.O_SYMBOL);
        int difference = Math.abs(xCount - oCount);
        return !((0 <= difference) && (difference <= 1));
    }

    public boolean canPlay() {
        if (this.getImpossible()) {
            return false;
        }
        if (this.getWin(Figure.X_SYMBOL)) {
            return false;
        }
        if (this.getWin(Figure.O_SYMBOL)) {
            return false;
        }
        if (this.getDraw()) {
            return false;
        }
        return true;
    }

    public Coordinate getEmptyOnlyRow(int row) {
        for (int column = 1; column <= this.getLength(); column++) {
            if (this.getFigure(row, column) == Figure.EMPTY) {
                return new Coordinate(row, column);
            }
        }
        throw new IllegalArgumentException("No empty cell on columns!");
    }

    public Coordinate getEmptyOnlyColumn(int column) {
        for (int row = 1; row <= this.getLength(); row++) {
            if (this.getFigure(row, column) == Figure.EMPTY) {
                return new Coordinate(row, column);
            }
        }
        throw new IllegalArgumentException("No empty cell on rows!");
    }

    public Coordinate getEmptyOnlyMainDiagonal() {
        for (int main = 1; main <= this.getLength(); main++) {
            if (this.getFigure(main, main) == Figure.EMPTY) {
                return new Coordinate(main, main);
            }
        }
        throw new IllegalArgumentException("No empty cell on main diagonal!");
    }

    public Coordinate getEmptyOnlySideDiagonal() {
        for (int side = 1; side <= this.getLength(); side++) {
            if (this.getFigure(side, this.getLength() + 1 - side) == Figure.EMPTY) {
                return new Coordinate(side, this.getLength() + 1 - side);
            }
        }
        throw new IllegalArgumentException("No empty cell on side diagonal!");
    }

    public int getCountOnRow(Figure figure, int row) {
        int count = 0;
        for (int column = 1; column <= this.getLength(); column++) {
            if (this.getFigure(row, column) == figure)
                count++;
        }
        return count;
    }

    public int getCountOnColumn(Figure figure, int column) {
        int count = 0;
        for (int row = 1; row <= this.getLength(); row++) {
            if (this.getFigure(row, column) == figure)
                count++;
        }
        return count;
    }

    public int getCountOnMainDiagonal(Figure figure) {
        int count = 0;
        for (int main = 1; main <= this.getLength(); main++) {
            if (this.getFigure(main, main) == figure)
                count++;
        }
        return count;
    }

    public int getCountOnSideDiagonal(Figure figure) {
        int count = 0;
        for (int side = this.getLength(); side >= 1; side--) {
            if (this.getFigure(side, this.getLength() + 1 - side) == figure) {
                count++;
            }
        }
        return count;
    }

    public Coordinate[] freeMoves() {
        ArrayList<Coordinate> moves = new ArrayList<>();
        for (int row = 1; row <= this.getLength(); row++) {
            for (int column = 1; column <= this.getLength(); column++) {
                if (this.getFigure(row, column) == Figure.EMPTY)
                    moves.add(new Coordinate(row, column));
            }
        }
        return moves.toArray(new Coordinate[0]);
    }
}
