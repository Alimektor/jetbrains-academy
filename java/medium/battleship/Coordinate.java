package battleship;

public class Coordinate {
    private final int x;
    private final int y;

    Coordinate(char[] arr) {
        x = arr[0] - 65;
        y = (arr.length > 2) ? 10 - 1: arr[1] - 49;
    }

    Coordinate(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public boolean checkPositionByX(Coordinate other, int length) {
        return this.checkLengthByX(other, length) && this.onLineY(other);
    }

    public boolean checkPositionByY(Coordinate other, int length) {
        return this.checkLengthByY(other, length) && this.onLineX(other);
    }

    public boolean checkPositionByAbsX(Coordinate other, int length) {
        return this.checkLengthByAbsX(other, length) && this.onLineY(other);
    }

    public boolean checkPositionByAbsY(Coordinate other, int length) {
        return this.checkLengthByAbsY(other, length) && this.onLineX(other);
    }

    public boolean isZeroLength(Coordinate other) {
        return this.onLineY(other) || this.onLineX(other);
    }

    public boolean compare(Coordinate other) {
        if (this.getX() != other.getX())
            return false;
        if (this.getY() != other.getY())
            return false;
        return true;
    }

    private boolean onLineY(Coordinate other) {
        return this.getY() == other.getY();
    }

    private boolean onLineX(Coordinate other) {
        return this.getX() == other.getX();
    }

    private boolean checkLengthByAbsX(Coordinate other, int length) {
        return Math.abs(this.getX() - other.getX()) == length;
    }

    private boolean checkLengthByAbsY(Coordinate other, int length) {
        return Math.abs(this.getY() - other.getY()) == length;
    }

    private boolean checkLengthByX(Coordinate other, int length) {
        return this.getX() - other.getX() == length;
    }

    private boolean checkLengthByY(Coordinate other, int length) {
        return this.getY() - other.getY() == length;
    }

}
