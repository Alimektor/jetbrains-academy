package cinema;

import java.util.Scanner;

public class Cinema {
    static int rowNumber;
    static int columnNumber;
    static int frontPrice = 10;
    static int backPrice = 8;
    static int price = frontPrice;
    static char[][] seats;
    static int menuOption = -1;
    static int totalTickets = 0;
    static int purchasedTickets = 0;
    static int currentIncome;
    static int totalIncome;
    static int frontRow;


    private static void showMenu() {
        Scanner scanner = new Scanner(System.in);
        System.out.println();
        System.out.println("1. Show the seats");
        System.out.println("2. Buy a ticket");
        System.out.println("3. Statistics");
        System.out.println("0. Exit");
        menuOption = scanner.nextInt();
    }

    private static void statistics() {
        System.out.println("Number of purchased tickets: " + getPurchasedTickets());
        System.out.println("Percentage: " + String.format("%.2f", getPercentage()) + "%");
        System.out.println("Current income: $" + getCurrentIncome());
        System.out.println("Total income: $" + getTotalIncome());
    }

    private static int getTotalTickets() {
        return totalTickets;
    }

    private static int getPurchasedTickets() {
        return purchasedTickets;
    }

    private static boolean isBusy(char seat)
    {
        return seat == 'B';
    }

    private static double getPercentage() {
        int tickets = getPurchasedTickets();
        if (tickets == 0)
            return 0;
        return (double) tickets / getTotalTickets() * 100;
    }

    private static int getCurrentIncome() {
        return currentIncome;
    }

    private static int getTotalIncome() {
        return totalIncome;
    }

    private static void menu() {
        switch (menuOption)
        {
            case 1:
                printSeats();
                break;
            case 2:
                setSeatBusy();
                break;
            case 3:
                statistics();
                break;
        }
    }

    private static void createSeats() {
        seats = new char[rowNumber][columnNumber];
        for (int row = 0; row < rowNumber; row++) {
            for (int column = 0; column < columnNumber; column++) {
                seats[row][column] = 'S';
            }
        }
        totalTickets = rowNumber * columnNumber;
        if (totalTickets > 60) {
            frontRow = ((int) Math.floor(rowNumber / 2.0));
        } else {
            frontRow = rowNumber;
        }
        totalIncome = (columnNumber * frontRow) * frontPrice + (columnNumber * (rowNumber - frontRow)) * backPrice;
    }

    private static void printSeats() {
        System.out.println();
        System.out.println("Cinema:");
        System.out.print("  ");
        for (int column = 0; column < columnNumber; column++) {
            System.out.print((column + 1) + " ");
        }
        System.out.println();
        for (int row = 0; row < rowNumber; row++) {
            System.out.print((row + 1) + " ");
            for (int column = 0; column < columnNumber; column++) {
                System.out.print(seats[row][column] + " ");
            }
            System.out.println();
        }
        System.out.println();
    }

    private static void setSeats() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter the number of rows:");
        rowNumber = scanner.nextInt();
        System.out.println("Enter the number of seats in each row:");
        columnNumber = scanner.nextInt();
        createSeats();
    }

    private static void printTicketPrice() {
        System.out.println("Ticket price: $" + price);
    }

    private static void setBusy(int row, int column) {
        seats[row - 1][column - 1] = 'B';
    }

    private static char getSeat(int row, int column) {
        return seats[row - 1][column - 1];
    }

    private static void setSeatBusy() {
        Scanner scanner = new Scanner(System.in);
        int row;
        int column;
        while (true) {
            System.out.println("Enter a row number:");
            row = scanner.nextInt();
            System.out.println("Enter a seat number in that row:");
            column = scanner.nextInt();
            if (row > rowNumber || column > columnNumber) {
                System.out.println("Wrong input!");
                continue;
            }
            break;
        }

        if (isBusy(getSeat(row, column))) {
            System.out.println("That ticket has already been purchased!");
            setSeatBusy();
            return;
        }

        if (row <= frontRow)
            price = frontPrice;
        else
            price = backPrice;
        setBusy(row, column);
        printTicketPrice();
        purchasedTickets++;
        currentIncome += price;
    }

    public static void main(String[] args) {
        setSeats();
        while (menuOption != 0)
        {
            showMenu();
            menu();
        }
    }
}