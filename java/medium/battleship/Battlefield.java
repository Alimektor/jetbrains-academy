package battleship;

import java.util.ArrayList;

public class Battlefield {
    private final int size = 10;
    private final Cell[][] battlefield;
    private final Cell[][] fog;
    private final String numberOfField;
    private final char[] lettersOfField;
    private int shipCellsCount;
    private ArrayList<Ship> ships;


    public Battlefield() {
        battlefield = new Cell[size][size];
        fog = new Cell[size][size];

        for (int row = 0; row < size; row++) {
            for (int column = 0; column < size; column++) {
                battlefield[row][column] = Cell.EMPTY;
                fog[row][column] = Cell.EMPTY;
            }
        }

        StringBuilder builder = new StringBuilder();
        for (int number = 1; number <= size; number++) {
            builder.append(number).append(" ");
        }
        numberOfField = builder.toString();

        lettersOfField = new char[size];
        for (int number = 0; number < size; number++) {
            lettersOfField[number] = ((char) (number + 65));
        }

        ships = new ArrayList<>();

        printBattlefield();
    }

    public void printBattlefield() {
        System.out.println(numberOfField);

        for (int row = 0; row < battlefield.length; row++) {
            System.out.print(lettersOfField[row] + " ");
            for (int column = 0; column < battlefield.length; column++) {
                Coordinate coordinate = new Coordinate(row, column);
                System.out.print(this.getBattlefieldCell(coordinate).getCell() + " ");
            }
            System.out.println();
        }
    }

    public void printFog() {
        System.out.println(numberOfField);

        for (int row = 0; row < fog.length; row++) {
            System.out.print(lettersOfField[row] + " ");
            for (int column = 0; column < fog.length; column++) {
                Coordinate coordinate = new Coordinate(row, column);
                System.out.print(this.getFogCell(coordinate).getCell() + " ");
            }
            System.out.println();
        }
    }

    public void trySetShip(String coordinates, int length, String name) throws BattlefieldException {
        String[] arr = coordinates.split(" ");
        Coordinate firstCoordinate = getCoordinate(arr[0]);
        Coordinate secondCoordinate = getCoordinate(arr[1]);
        Ship ship = new Ship(length);
        length--;

        if (secondCoordinate.checkPositionByX(firstCoordinate, length)) {

            for (int i = firstCoordinate.getX(); i <= secondCoordinate.getX(); i++) {
                Coordinate coordinate = new Coordinate(i, firstCoordinate.getY());
                if (!checkCell(coordinate))
                    throw new BattlefieldException("Error! You placed it too close to another one. Try again:");
            }

            for (int i = firstCoordinate.getX(); i <= secondCoordinate.getX(); i++) {
                Coordinate coordinate = new Coordinate(i, firstCoordinate.getY());
                setShipCell(coordinate, ship);
            }

        }
        else if (firstCoordinate.checkPositionByAbsX(secondCoordinate, length)) {

            for (int i = secondCoordinate.getX(); i <= firstCoordinate.getX(); i++) {
                Coordinate coordinate = new Coordinate(i, firstCoordinate.getY());
                if (!checkCell(coordinate))
                    throw new BattlefieldException("Error! You placed it too close to another one. Try again:");
            }

            for (int i = secondCoordinate.getX(); i <= firstCoordinate.getX(); i++) {
                Coordinate coordinate = new Coordinate(i, firstCoordinate.getY());
                setShipCell(coordinate, ship);
            }

        }
        else if (secondCoordinate.checkPositionByY(firstCoordinate, length)) {

            for (int i = firstCoordinate.getY(); i <= secondCoordinate.getY(); i++) {
                Coordinate coordinate = new Coordinate(firstCoordinate.getX(), i);
                if (!checkCell(coordinate))
                    throw new BattlefieldException("Error! You placed it too close to another one. Try again:");
            }

            for (int i = firstCoordinate.getY(); i <= secondCoordinate.getY(); i++) {
                Coordinate coordinate = new Coordinate(firstCoordinate.getX(), i);
                setShipCell(coordinate, ship);
            }

        }
        else if (firstCoordinate.checkPositionByAbsY(secondCoordinate, length)) {

            for (int i = secondCoordinate.getY(); i <= firstCoordinate.getY(); i++) {
                Coordinate coordinate = new Coordinate(firstCoordinate.getX(), i);
                if (!checkCell(coordinate))
                    throw new BattlefieldException("Error! You placed it too close to another one. Try again:");
            }

            for (int i = secondCoordinate.getY(); i <= firstCoordinate.getY(); i++) {
                Coordinate coordinate = new Coordinate(firstCoordinate.getX(), i);
                setShipCell(coordinate, ship);
            }
        }
        else if (firstCoordinate.isZeroLength(secondCoordinate)) {
            throw new BattlefieldException(String.format("Error! Wrong length of the %s! Try again:", name));
        }
        else {
            throw new BattlefieldException("Error! Wrong ship location! Try again:");
        }

        ships.add(ship);

        printBattlefield();
    }

    public String hitAShip(String coordinate) throws BattlefieldException {
        Coordinate hit = getCoordinate(coordinate);
        trySetHit(hit);
        if (this.isHit(hit)) {
            for (Ship ship : ships) {
                if (ship.checkCoordinate(hit)) {
                    if (ship.isSank()) {
                        return "You sank a ship!";
                    }
                    return "You hit a ship!";
                }
            }
        }

        return "You missed!";
    }

    public boolean checkWin(Battlefield otherBattlefield) {
        return otherBattlefield.getShipCount() == 0;
    }

    private int getShipCount() {
        return shipCellsCount;
    }

    private void setShipCell(Coordinate coordinate, Ship ship) {
        ship.addCoordinate(coordinate);
        battlefield[coordinate.getX()][coordinate.getY()] = Cell.SHIP;
        shipCellsCount++;
    }

    private boolean checkCell(Coordinate coordinate) {
        int row1;
        int row2;
        int column1;
        int column2;

        switch (coordinate.getY()) {
            case 0:
                row1 = coordinate.getY();
                row2 = coordinate.getY() + 1;
                break;
            case 9:
                row1 = coordinate.getY() - 1;
                row2 = coordinate.getY();
                break;
            default:
                row1 = coordinate.getY() - 1;
                row2 = coordinate.getY() + 1;
        }

        switch (coordinate.getX()) {
            case 0:
                column1 = coordinate.getX();
                column2 = coordinate.getX() + 1;
                break;
            case 9:
                column1 = coordinate.getX() - 1;
                column2 = coordinate.getX();
                break;
            default:
                column1 = coordinate.getX() - 1;
                column2 = coordinate.getX() + 1;
        }


        for (int row = row1; row <= row2; row++) {
            for (int column = column1; column <= column2; column++) {
                Coordinate checking = new Coordinate(column, row);
                if (isShip(checking)) {
                    return false;
                }

            }
        }

        return true;
    }

    private boolean isShip(Coordinate coordinate) {
        return getBattlefieldCell(coordinate) == Cell.SHIP;
    }

    private boolean isHit(Coordinate coordinate) {
        return fog[coordinate.getX()][coordinate.getY()] == Cell.HIT;
    }

    private boolean isFree(Coordinate coordinate) {
        return battlefield[coordinate.getX()][coordinate.getY()] == Cell.EMPTY;
    }

    private void trySetHit(Coordinate coordinate) throws BattlefieldException {
        if (coordinate.getX() < 0 || coordinate.getY() < 0 || coordinate.getX() >= battlefield.length || coordinate.getY() >= battlefield.length) {
            throw new BattlefieldException("Error! You entered the wrong coordinates! Try again:");
        }

        if (this.isShip(coordinate)) {
            setHit(coordinate);
        }
        if (this.isFree(coordinate)) {
            setMissed(coordinate);
        }
    }

    private Cell getBattlefieldCell(Coordinate coordinate) {
        return battlefield[coordinate.getX()][coordinate.getY()];
    }

    private Cell getFogCell(Coordinate coordinate) {
        return fog[coordinate.getX()][coordinate.getY()];
    }

    private void setHit(Coordinate coordinate) {
        fog[coordinate.getX()][coordinate.getY()] = Cell.HIT;
        for (Ship ship : ships) {
            if (ship.checkCoordinate(coordinate))
                ship.hit();
        }
        battlefield[coordinate.getX()][coordinate.getY()] = Cell.HIT;
        shipCellsCount--;
    }

    private void setMissed(Coordinate coordinate) {
        fog[coordinate.getX()][coordinate.getY()] = Cell.MISSED;
        battlefield[coordinate.getX()][coordinate.getY()] = Cell.MISSED;
    }

    private Coordinate getCoordinate(String coordinate) {
        return new Coordinate(coordinate.toCharArray());
    }
}
