package battleship;

import java.util.Scanner;

public class Player {
    private final String name;
    private Battlefield board;
    private static Scanner scanner;

    Player(String name) {
        this.name = name;
        scanner = new Scanner(System.in);
    }

    public Battlefield getBoard() {
        return board;
    }

    public void setBoard() {
        board = new Battlefield();
        System.out.println(this.getName() + ", place your ships on the game field");
        input("Aircraft Carrier", 5);
        input("Battleship", 4);
        input("Submarine", 3);
        input("Cruiser", 3);
        input("Destroyer", 2);
    }

    public boolean isWin(Player other) {
        return board.checkWin(other.getBoard());
    }

    public void takeAShot(Player other) {
            try {
                other.getBoard().printFog();
                System.out.println("---------------------");
                board.printBattlefield();
                System.out.println("Take a shot!");
                String coordinate = scanner.nextLine().trim();
                String message = other.getBoard().hitAShip(coordinate);
                System.out.println(message);
            } catch (Exception exception) {
                System.out.println(exception.getMessage());
            }
    }

    private void input(String name, int size) {
        System.out.printf("Enter the coordinates of the %s (%d cells):%n", name, size);
        while (true) {
            String coordinates = scanner.nextLine().trim();
            try {
                board.trySetShip(coordinates, size, name);
                break;
            } catch (BattlefieldException exception) {
                System.out.println(exception.getMessage());
            }
        }
    }

    public String getName() {
        return name;
    }
}
