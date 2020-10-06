from enum import Enum
import random
import math
import sqlite3


class BankDataBase:
    def __init__(self, db_name):
        self.__connection = sqlite3.connect(db_name)
        self.create()

    def create(self):
        dropping = """
        DROP TABLE IF EXISTS card;
        """
        creating = """
        CREATE TABLE IF NOT EXISTS card(
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
        );
        """
        self.query(dropping)
        self.query(creating)

    def query(self, query):
        self.__get_cursor().execute(query)
        self.commit()

    def __get_cursor(self):
        return self.__connection.cursor()

    def commit(self):
        self.__connection.commit()

    def get_card_by_number(self, number):
        cursor = self.__get_cursor()
        cursor.execute(f"SELECT * FROM card WHERE number = '{number}';")
        return CreditCard.get_from_tuple(cursor.fetchone())

    def add_card(self, card):
        id = int(card.get_number())
        number = card.get_number()
        pin = card.get_pin()
        balance = card.get_balance()
        cursor = self.__get_cursor()
        query = f"INSERT INTO card VALUES({id}, '{number}', '{pin}', {balance});"
        cursor.execute(query)
        self.commit()

    def add_to_balance(self, income, card):
        balance = card.get_balance() + int(income)
        number = card.get_number()
        self.query(f"UPDATE card SET balance = {balance} WHERE number = '{number}';")

    def remove_from_balance(self, money, card):
        balance = card.get_balance() - int(money)
        number = card.get_number()
        self.query(f"UPDATE card SET balance = {balance} WHERE number = '{number}';")

    def delete(self, card):
        number = card.get_number()
        self.query(f"DELETE FROM card WHERE number = '{number}';")


class CreditCard:
    def __init__(self, number=None, pin=None, balance=0):
        self.__number = number
        self.__pin = pin
        self.__balance = balance
        self.__choice = None
        if self.__number is None:
            iin = "400000"
            can = ""
            for i in range(9):
                can += str(self.__get_random_digit())
            check_digit = self.__get_checksum(iin + can)
            self.__number = f"{iin}{can}{check_digit}"
        if self.__pin is None:
            self.__pin = ""
            for i in range(4):
                self.__pin += str(self.__get_random_digit())

    @staticmethod
    def __get_checksum(check):
        check = [int(i) for i in list(check)]
        for i in range(len(check)):
            if i % 2 == 0:
                check[i] *= 2
            if check[i] > 9:
                check[i] -= 9
        summation = sum(check)
        return math.ceil(summation / 10) * 10 - summation

    def __get_random_digit(self):
        return random.randint(1, 9)

    @staticmethod
    def check_card_number(card_number):
        try:
            iin = card_number[:6]
            can = card_number[6:-1]
            check_digit = CreditCard.__get_checksum(iin + can)
            right_number = f"{iin}{can}{check_digit}"
            return right_number == card_number
        except:
            return False

    def get_number(self):
        return self.__number

    def get_pin(self):
        return self.__pin

    def get_balance(self):
        return self.__balance

    def add_balance(self, money):
        self.__balance += int(money)

    def substract_balance(self, money):
        self.__balance -= int(money)

    @classmethod
    def get_from_tuple(cls, param):
        if param:
            return CreditCard(param[1], param[2], param[3])
        return False


class MenuChoice(Enum):
    EXIT = 0
    CREATE = 1
    LOGIN = 2


class AccountChoice(Enum):
    EXIT = 0
    BALANCE = 1
    ADDING = 2
    TRANSFER = 3
    CLOSING = 4
    LOGOUT = 5


class BankSystem:
    def __init__(self, database_name):
        self.__db = BankDataBase(database_name)
        self.__menu_choice = None
        self.__account_choice = None

    def __menu(self):
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        self.__menu_choice = MenuChoice(int(input()))

    def __create_account(self):
        print("Your card has been created")
        verified = False
        new_card = CreditCard()
        while True:
            if self.__db.get_card_by_number(new_card.get_number()):
                break
            new_card = CreditCard()
            self.__db.add_card(new_card)
        print(f"Your card number:\n{new_card.get_number()}")
        print(f"Your card PIN:\n{new_card.get_pin()}")

    def __menu_account(self):
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        self.__account_choice = AccountChoice(int(input()))

    def __main_account(self):
        print("You have successfully logged in!")
        while True:
            if self.__account_choice == AccountChoice.BALANCE:
                self.__get_balance()
            if self.__account_choice == AccountChoice.LOGOUT:
                print("\nYou have successfully logged out!")
                self.__account_choice = None
                self.__current_card = None
                return
            if self.__account_choice == AccountChoice.EXIT:
                self.__menu_choice = MenuChoice.EXIT
                self.__account_choice = None
                self.__current_card = None
                return
            if self.__account_choice == AccountChoice.ADDING:
                self.__add()
            if self.__account_choice == AccountChoice.CLOSING:
                self.__close_the_account()
            if self.__account_choice == AccountChoice.TRANSFER:
                self.__transfer_menu()
            self.__menu_account()

    def __get_balance(self):
        self.__current_card = self.__db.get_card_by_number(self.__current_card.get_number())
        print(f"\nBalance: {self.__current_card.get_balance()}\n")

    def __add(self):
        print("Enter income:")
        income = int(input())
        self.__db.add_to_balance(income, self.__current_card)
        self.__current_card.add_balance(self.__current_card.get_balance() + income)
        print("Income was added!")

    def __close_the_account(self):
        self.__db.delete(self.__current_card)
        print("The account has been closed!")

    def __transfer_menu(self):
        print("Enter card number:")
        card_number = input()
        if not CreditCard.check_card_number(card_number):
            print("Probably you made mistake in the card number.")
            print("Please try again!")
            return
        card = self.__db.get_card_by_number(card_number)
        if not card:
            print("Such a card does not exist.")
            return
        print("Enter how much money you want to transfer:")
        money = int(input())
        if self.__current_card.get_balance() < money:
            print("Not enough money!")
            return
        self.__db.add_to_balance(money, card)
        self.__db.remove_from_balance(money, self.__current_card)
        self.__current_card.substract_balance(money)
        print("Success!")

    def __login(self):
        print("Enter your card number:")
        number = input()
        print("Enter your PIN")
        pin = input()
        card = self.__db.get_card_by_number(number)
        if card and card.get_pin() == pin:
            self.__current_card = card
            self.__main_account()
            return True
        print("Wrong card number or PIN!")
        return False

    def main(self):
        while True:
            if self.__menu_choice == MenuChoice.EXIT:
                print("\nBye!")
                return
            if self.__menu_choice == MenuChoice.CREATE:
                self.__create_account()
            if self.__menu_choice == MenuChoice.LOGIN:
                self.__login()
                if self.__menu_choice == MenuChoice.EXIT:
                    continue
            self.__menu()


if __name__ == '__main__':
    bank = BankSystem("card.s3db")
    bank.main()
