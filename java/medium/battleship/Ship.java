package battleship;

public class Ship {
    Coordinate[] coordinates;
    private int size;
    private int current;

    Ship(int size) {
        this.size = size;
        this.current = 0;
        coordinates = new Coordinate[size];
    }

    public void addCoordinate(Coordinate coordinate) {
        coordinates[current] = coordinate;
        current++;
    }

    public boolean checkCoordinate(Coordinate coordinate) {
        for (Coordinate cell : coordinates) {
            if (cell.compare(coordinate))
                return true;
        }
        return false;
    }

    public boolean isSank() {
        return size == 0;
    }

    public void hit() {
        size--;
    }
}
