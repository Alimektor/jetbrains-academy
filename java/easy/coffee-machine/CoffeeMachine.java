package machine;
import java.util.Scanner;

class Coffee {
    public int money;
    public int water;
    public int milk;
    public int beans;
    public int cups;

    public Coffee(int money, int water, int milk, int beans, int cups) {
        this.money = money;
        this.water = water;
        this.milk = milk;
        this.beans = beans;
        this.cups = cups;
    }

    public Coffee subtract(Coffee other) {
        int money = this.money + other.money;
        int water = this.water - other.water;
        int milk = this.milk - other.milk;
        int beans = this.beans - other.beans;
        int cups = this.cups - other.cups;
        return new Coffee(money, water, milk, beans, cups);
    }
}

public class CoffeeMachine {
    private Coffee info;
    private final Scanner scanner;
    public int water;
    public int milk;
    public int beans;

    public CoffeeMachine() {
        this.info = new Coffee(550, 400, 540, 120, 9);
        this.water = 400;
        this.milk = 540;
        this.beans = 120;
        this.scanner = new Scanner(System.in);
    }

    private void remaining() {
        System.out.print("The coffee machine has:\n");
        System.out.printf("%d of water\n", this.info.water);
        System.out.printf("%d of milk\n", this.info.milk);
        System.out.printf("%d of coffee beans\n", this.info.beans);
        System.out.printf("%d of disposable cups\n", this.info.cups);
        System.out.printf("$%d of money\n", this.info.money);
    }

    private void menu() {
        while (true) {
            System.out.println("Write action (buy, fill, take, remaining, exit):");
            String choice = scanner.nextLine();
            System.out.println();
            if (choice.equals("buy"))
                this.buy();
            if (choice.equals("fill"))
                this.fill();
            if (choice.equals("take"))
                this.take();
            if (choice.equals("remaining"))
                this.remaining();
            if (choice.equals("exit"))
                break;
        }
    }

    private void take() {
        System.out.printf("I gave you $%d\n", this.info.money);
        this.info.money = 0;
    }

    private void fill() {
        System.out.println("Write how many ml of water do you want to add:");
        this.info.water += this.scanner.nextInt();
        System.out.println("Write how many ml of milk do you want to add:");
        this.info.milk += this.scanner.nextInt();
        System.out.println("Write how many grams of coffee beans do you want to add:");
        this.info.beans += this.scanner.nextInt();
        System.out.println("Write how many disposable cups of coffee do you want to add:");
        this.info.cups += this.scanner.nextInt();
    }

    private void buy() {
        System.out.println("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:");
        String coffeeChoice = this.scanner.nextLine();
        Coffee coffee = new Coffee(0, 0, 0, 0, 0);
        if (coffeeChoice.equals("back")) return;
        if (coffeeChoice.equals("1")) coffee = new Coffee(4, 250, 0, 16, 1);
        if (coffeeChoice.equals("2")) coffee = new Coffee(7, 350, 75, 20, 1);
        if (coffeeChoice.equals("3")) coffee = new Coffee(6, 200, 100, 12, 1);
        System.out.println(this.hadEnough(coffee));
    }

    private String hadEnough(Coffee coffee) {
        if (this.info.milk < coffee.milk)
            return "Sorry, not enough milk!";
        if (this.info.water < coffee.water)
            return "Sorry, not enough water!";
        if (this.info.beans < coffee.beans)
            return "Sorry, not enough coffee beans!";
        if (this.info.cups < coffee.cups)
            return "Sorry, not enough disposable cups!";
        this.info = this.info.subtract(coffee);
        return "I have enough resources, making you a coffee!";
    }

    public static void main(String[] args) {
        CoffeeMachine machine = new CoffeeMachine();
        machine.menu();
    }
}
