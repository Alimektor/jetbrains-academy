package battleship;

public enum Cell {
    EMPTY('~'),
    HIT('x'),
    SHIP('o'),
    MISSED('M');

    private final char cell;

    Cell(char cell) {
        this.cell = cell;
    }

    public char getCell() {
        return this.cell;
    }
}
