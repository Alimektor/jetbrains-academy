package tictactoe;

import java.util.Scanner;

public class Main {
    public static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        while (true) {
            try {
                String[] commands = getCommands();
                MenuChoice command = MenuChoice.setChoice(commands[0]);
                if (command == MenuChoice.EXIT)
                    break;
                if (commands.length != 3)
                    throw new IllegalArgumentException("Bad parameters");
                Board board = new Board();
                Player first = getPlayer(commands[1], Figure.X_SYMBOL, board);
                Player second = getPlayer(commands[2], Figure.O_SYMBOL, board);
                if (command == MenuChoice.START)
                    start(first, second, board);
            } catch (IllegalArgumentException exception) {
                System.out.println(exception.getMessage());
            }
        }
    }

    private static String[] getCommands() {
        String input = scanner.nextLine();
        return input.split(" ");
    }

    private static Player getPlayer(String type, Figure figure, Board board) {
        switch (type) {
            case "user":
                return new User(figure, board);
            case "easy":
                return new EasyPlayer(figure, board);
            case "medium":
                return new MediumPlayer(figure, board);
            case "hard":
                return new HardPlayer(figure, board);
        }
        throw new IllegalArgumentException("Not a player type!");
    }

    private static void start(Player first, Player second, Board board) {
        System.out.println(board);
        while (board.canPlay()) {
            try {
                System.out.println(first.getMessage());
                first.move();
                System.out.println(board);
                if (!board.canPlay())
                    break;
                System.out.println(second.getMessage());
                second.move();
                System.out.println(board);
            } catch (IllegalArgumentException exception) {
                System.out.println(exception.getMessage());
            }
        }
        System.out.println(checkWithMessage(board.check()));
    }

    private static String checkWithMessage(State state) {
        switch (state) {
            case Immpossible:
                return "Impossible";
            case xWins:
                return "X wins";
            case oWins:
                return "O wins";
            case Draw:
                return "Draw";
            case NotFinished:
                return "Game not finished";
        }
        throw new IllegalArgumentException("State is not valid");
    }
}
