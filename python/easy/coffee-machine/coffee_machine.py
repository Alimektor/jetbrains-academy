import enum


class CoffeeChoice(enum.Enum):
    ESPRESSO = 1
    LATTE = 2
    CAPPUCCINO = 3


class Coffee:
    def __init__(self, money=0, water=0, milk=0, beans=0, cups=1):
        self.money = money
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cups = cups

    def __sub__(self, other):
        money = self.money + other.money
        water = self.water - other.water
        milk = self.milk - other.milk
        beans = self.beans - other.beans
        cups = self.cups - other.cups
        return Coffee(money, water, milk, beans, cups)


class CoffeeMaker:
    def __init__(self):
        self.milk = 540
        self.water = 400
        self.beans = 120

        self.info = Coffee(550, 400, 540, 120, 9)
        self.espresso = Coffee(money=4, water=250, beans=16)
        self.latte = Coffee(money=7, water=350, milk=75, beans=20)
        self.cappuccino = Coffee(money=6, water=200, milk=100, beans=12)

    def __make(self):
        milk_for_coffee = self.milk // self.milk
        water_for_coffee = self.water // self.water
        beans_for_coffee = self.beans // self.coffee_beans
        return min(milk_for_coffee, water_for_coffee, beans_for_coffee)

    def remaining(self):
        print("The coffee machine has:")
        print(f"{self.info.water} of water")
        print(f"{self.info.milk} of milk")
        print(f"{self.info.beans} of coffee beans")
        print(f"{self.info.cups} of disposable cups")
        print(f"${self.info.money} of money" if self.info.money > 0 else f"{self.info.money} of money")
        print()

    def menu(self):
        while True:
            choice = input("Write action (buy, fill, take, remaining, exit)")
            print()
            if choice == "exit":
                break
            if choice == "buy":
                self.buy()
            if choice == "fill":
                self.fill()
            if choice == "take":
                self.take()
            if choice == "remaining":
                self.remaining()

    def had_enough(self, coffee):
        if self.info.milk < coffee.milk:
            return "Sorry, not enough milk!"
        if self.info.water < coffee.water:
            return "Sorry, not enough water!"
        if self.info.beans < coffee.beans:
            return "Sorry, not enough coffee beans!"
        if self.info.cups < coffee.cups:
            return "Sorry, not enough disposable cups!"
        self.info -= coffee
        return "I have enough resources, making you a coffee!"


    def buy(self):
        coffee_choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
        if coffee_choice == "back":
            return
        coffee_choice = CoffeeChoice(int(coffee_choice))
        if coffee_choice == CoffeeChoice.ESPRESSO:
            coffee = self.espresso
        if coffee_choice == CoffeeChoice.LATTE:
            coffee = self.latte
        if coffee_choice == CoffeeChoice.CAPPUCCINO:
            coffee = self.cappuccino
        print(self.had_enough(coffee))


    def fill(self):
        self.info.water +=  int(input("Write how many ml of water do you want to add:"))
        self.info.milk +=   int(input("Write how many ml of milk do you want to add:"))
        self.info.beans +=  int(input("Write how many grams of coffee beans do you want to add:"))
        self.info.cups +=   int(input("Write how many disposable cups of coffee do you want to add:"))

    def take(self):
        print(f"I gave you {self.info.money}")
        self.info.money = 0


if __name__ == '__main__':
    coffee_maker = CoffeeMaker()
    coffee_maker.menu()
