package tictactoe;

public enum Figure {
    EMPTY(' '),
    X_SYMBOL('X'),
    O_SYMBOL('O');

    private final char figure;

    Figure(char figure) {
        this.figure = figure;
    }

    static Figure setFigure(char symbol) {
        for (Figure figure : Figure.values()) {
            if (symbol == figure.getSymbol())
                return figure;
        }
        return EMPTY;
    }

    char getSymbol() {
        return this.figure;
    }
}
