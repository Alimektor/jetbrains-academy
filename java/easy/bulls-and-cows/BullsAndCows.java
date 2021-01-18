package bullscows;

import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class Main {
    private static int size;
    private static String secretCode;
    private static final int maxCodeLength = 36;
    private static final int minCodeLength = 1;
    private static int possibilities;
    private static char lastElement;

    public static void main(String[] args) {
        try {
            if (!createSecretCode())
                return;
            System.out.println("Okay, let's start a game!");
            String digits;
            int turn = 1;
            do {
                System.out.println("Turn " + turn);
                digits = getDigits();
                System.out.println("Grade: " + getGrade(digits) + ". The secret code is " + getSecretCode());
                turn++;
            } while (!getWin(digits));
            System.out.println("Congratulations! You guessed the secret code.");
        } catch (Exception e) {
            System.out.println("Error: something bad occurred.");
        }
    }

    private static boolean getWin(String guess) {
        return getBulls(guess) == size;
    }

    private static char getRandom(char[] array) {
        int rnd = new Random().nextInt(array.length);
        return array[rnd];
    }

    private static String getStringRepresentation(ArrayList<Character> list) {
        StringBuilder builder = new StringBuilder(list.size());
        for(Character ch: list)
        {
            builder.append(ch);
        }
        return builder.toString();
    }

    private static boolean createSecretCode() {
        boolean error = setSize();
        if (error)
            return false;

        error = setPossibilities();
        if (error)
            return false;

        char[] elements = "0123456789abcdefghijklmnopqrstuvwxyz".substring(0, possibilities).toCharArray();
        lastElement = elements[elements.length - 1];
        ArrayList<Character> list = new ArrayList<>();

        for (int i = 0; i < size; i++) {
            char randomElement;
            do {
                randomElement = getRandom(elements);
            } while (list.contains(randomElement));
            list.add(randomElement);
        }

        secretCode = getStringRepresentation(list);
        getPrepared();
        return true;
    }

    private static boolean setPossibilities() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Input the number of possible symbols in the code:");
        possibilities = scanner.nextInt();
        if (possibilities < size || possibilities > maxCodeLength) {
            System.out.println("Error: possibilities is less than the code length or more than max symbols.");
            return true;
        }
        return false;
    }

    private static boolean setSize() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Input the length of the secret code:");
        int number = scanner.nextInt();

        if ((number > maxCodeLength) || (number < minCodeLength)) {
            System.out.println("Error: can't generate a secret number with this length because there aren't enough unique sequences.");
            return true;
        }
        size = number;
        return false;
    }

    private static void getPrepared() {
        System.out.println("The secret is prepared: " + "*".repeat(Math.max(0, size)) + " (0-9, a-" + lastElement + ").");
    }

    private static String getSecretCode() {
        return secretCode;
    }

    private static boolean containsDigit(String code, char digit) {
        return code.indexOf(digit) != -1;
    }

    private static int getCows(String guess) {
        int cows = 0;

        for (int i = 0; i < guess.length(); i++) {
            if (containsDigit(secretCode, guess.charAt(i))) {
                cows++;
            }
        }

        return cows - getBulls(guess);
    }

    private static int getBulls(String guess) {
        int bulls = 0;

        for (int i = 0; i < guess.length(); i++) {
            if (guess.charAt(i) == secretCode.charAt(i)) {
                bulls++;
            }
        }

        return bulls;
    }

    private static String getGrade(String guess) {
        StringBuilder grade = new StringBuilder();
        int bulls = getBulls(guess);
        int cows = getCows(guess);
        if (cows == 0 && bulls == 0)
            return "None";
        if (bulls > 0)
            grade.append(bulls).append(" bull(s)");
        if (bulls > 0 && cows > 0)
            grade.append(" and ");
        if (cows > 0)
            grade.append(cows).append(" cows(s)");

        return grade.toString();
    }

    private static String getDigits() {
        Scanner scanner = new Scanner(System.in);
        return scanner.nextLine();
    }
}
