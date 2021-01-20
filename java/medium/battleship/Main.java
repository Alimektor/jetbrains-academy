package battleship;

import java.io.IOException;
import java.util.Scanner;

public class Main {
    private static Scanner scanner;
    private static Battlefield battlefield;
    private static String winner;

    public static void main(String[] args) {
        Player player1 = new Player("Player 1");
        Player player2 = new Player("Player 2");

        player1.setBoard();
        promptEnter();
        player2.setBoard();
        promptEnter();
        System.out.println("The game starts!");

        while (true) {
            player1.takeAShot(player2);
            if (player1.isWin(player2)) {
                setWinner(player1);
                break;
            }
            promptEnter();
            player2.takeAShot(player1);
            if (player2.isWin(player1)) {
                setWinner(player2);
                break;
            }
            promptEnter();
        }

        announceWinner();
    }

    private static void setWinner(Player player) {
        winner = player.getName();
    }

    private static void announceWinner() {
        System.out.println("You sank the last ship. You won. Congratulations!");
    }

    private static void promptEnter() {
        System.out.println("Press Enter and pass the move to another player");
        try {
            System.in.read();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
