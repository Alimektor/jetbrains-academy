package tictactoe;

import java.util.Scanner;

public class User extends Player {
    private final Scanner scanner = new Scanner(System.in);

    User(Figure symbol, Board board) {
        super("", symbol, board);
    }

    private int getInteger() throws IllegalArgumentException {
        if (!scanner.hasNextInt()) {
            scanner.next();
            throw new IllegalArgumentException("You should enter numbers!");
        }
        return scanner.nextInt();
    }

    @Override
    protected String getMessage() {
        return "";
    }

    @Override
    void move() {
        while (true) {
            try {
                System.out.println("Enter the coordinates: ");

                int x = getInteger();
                int y = getInteger();

                Coordinate coordinate = new Coordinate(x, y);
                board.setFigure(coordinate, this.getFigure());
                return;
            } catch (IllegalArgumentException exception) {
                System.out.println(exception.getMessage());
            }
        }
    }
}