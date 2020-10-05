package tictactoe;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Arrays;


class TicTacToe {

    private char[][] matrix;

    public TicTacToe(String initial) {
        if (initial == null)
            initial = "_________";
        this.matrix = new char[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                matrix[i][j] = initial.charAt(i * 3 + j);
            }
        }
    }

    private boolean getWin(char symbol) {
        char[] checked = { symbol, symbol, symbol };
        ArrayList<Character> checkedList = new ArrayList<>();
        for (char ch : checked) {
            checkedList.add(ch);
        }
        ArrayList<Character> diagonal = new ArrayList<>();
        ArrayList<Character> horizontal;
        for (int i = 0; i < this.matrix.length; i++) {
            if (Arrays.equals(matrix[0], checked))
                return true;
            horizontal = new ArrayList<>();
            for (int j = 0; j < this.matrix[i].length; j++) {
                horizontal.add(this.matrix[j][i]);
                if (j + i == 2)
                    diagonal.add(matrix[i][j]);
            }
            if (horizontal.equals(checkedList))
                return true;
        }
        if (diagonal.equals(checkedList))
            return true;
        diagonal = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            diagonal.add(this.matrix[i][i]);
        }
        return diagonal.equals(checkedList);
    }

    private boolean getImpossible() {
        if (this.getWin('X') && this.getWin('O'))
            return true;
        int x = 0;
        int o = 0;
        for (int i = 0; i < this.matrix.length; i++) {
            for (int j = 0; j < this.matrix[i].length; j++) {
                if (matrix[i][j] == 'X') x++;
                if (matrix[i][j] == 'O') o++;
            }
        }
        return !((0 <= Math.abs(x - o)) && (Math.abs(x - o) <= 1));
    }

    private boolean getDraw() {
        for (int i = 0; i < this.matrix.length; i++) {
            for (int j = 0; j < this.matrix[i].length; j++) {
                if (matrix[i][j] == '_')
                    return false;
            }
        }
        return true;
    }

    private boolean check() {
        if (this.getImpossible()) {
            System.out.println("Impossible");
            return true;
        }
        else if (this.getWin('X')) {
            System.out.println("X wins");
            return true;
        }
        else if (this.getWin('O')) {
            System.out.println("O wins");
            return true;
        }
        else if (this.getDraw()) {
            System.out.println("Draw");
            return true;
        }
        else {
            return false;
        }
    }

    private boolean isOccupied(int x, int y) {
        return this.matrix[x][y] != '_';
    }

    public TicTacToe setCoordinates(char symbol) {
        while (true) {
            int x;
            int y;
            System.out.print("Enter the coordinates: ");
            Scanner scanner = new Scanner(System.in);
            try {
                y = scanner.nextInt();
                x = scanner.nextInt();
            }
            catch (Exception exc) {
                System.out.println("You should enter numbers!");
                continue;
            }
            if (1 <= x && x <= 3 && 1 <= y && y <= 3) {
                x = -x;
                --y;
            }
            else {
                System.out.println("Coordinates should be from 1 to 3!");
                continue;
            }
            if (x < 0) {
                x = x + 3;
            }
            if (y < 0) {
                y = y + 3;
            }
            if (this.isOccupied(x, y)) {
                System.out.println("This cell is occupied! Choose another one!");
                continue;
            }
            this.matrix[x][y] = symbol;
            return this;
        }
    }

    private boolean move(char symbol) {
        System.out.println(this);
        if (!this.check()) {
            this.setCoordinates(symbol);
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        StringBuilder result = new StringBuilder();
        result.append("---------\n");
        for (int i = 0; i < 3; i++) {
            result.append("|");
            for (int j = 0; j < 3; j++) {
                result.append(" ").append(matrix[i][j]);
            }
            result.append(" |\n");
        }
        result.append("---------\n");
        return result.toString();
    }

    public void main() {
        boolean haveWon = false;
        char[] symbols = { 'X', 'O' };
        while (!haveWon) {
            for (char symbol: symbols) {
                if (this.move(symbol)) {
                    haveWon = true;
                    break;
                }
            }
        }
    }
}

public class Main {
    public static void main(String[] args) {
        TicTacToe game = new TicTacToe(null);
        game.main();
    }
}
