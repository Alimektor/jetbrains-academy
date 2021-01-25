package tictactoe;

public class Coordinate {
    private final int x;
    private final int y;

    Coordinate(int x, int y) {

        if (x > 3 || x < 1 || y > 3 || y < 1)
            throw new IllegalArgumentException("Coordinates should be from 1 to 3!");
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    @Override
    public String toString() {
        return "(row: " + x + ", column: " + y + ")";
    }
}
