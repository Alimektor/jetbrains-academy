#!/bin/python3
# -*- coding: utf-8 -*-
"""
:authors: Alimektor
:license: MIT
:copyright: (c) 2021 Alimektor
"""


class Bot:
    def greet(self, bot_name, birth_year):
        """Greetings from the bot

        :param bot_name: the bot name
        :type bot_name: str
        :param birth_year: the birth year of the bot_name
        :type birth_year: str
        """
        print('Hello! My name is ' + bot_name + '.')
        print('I was created in ' + birth_year + '.')

    def remind_name(self):
        """
        Remind the bot the name using input
        """
        print('Please, remind me your name.')
        name = input()
        print('What a great name you have, ' + name + '!')

    def guess_age(self):
        """
        The bots tried to guess the number using remainders of dividing the input by 3, 5, 7
        """
        print('Let me guess your age.')
        print('Enter remainders of dividing your age by 3, 5 and 7.')

        rem3 = int(input())
        rem5 = int(input())
        rem7 = int(input())
        age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

        print("Your age is " + str(age) +
              "; that's a good time to start programming!")

    def count(self):
        """
        The bot counts numbers
        """
        print('Now I will prove to you that I can count to any number you want.')

        num = int(input())
        curr = 0
        while curr <= num:
            print(f"{curr}!")
            curr = curr + 1

    def test(self):
        """
        Test the infinite loop
        """
        print("Let's test your programming knowledge.")
        print("Why do we use methods?")
        choice = 0
        while choice != 2:
            print("1. To repeat a statement multiple times.")
            print("2. To decompose a program into several small subroutines.")
            print("3. To determine the execution time of a program.")
            print("4. To interrupt the execution of a program.")
            choice = int(input())
            if choice != 2:
                print("Please, try again.")
        print('Completed, have a nice day!')

    def end(self):
        """
        Last sentence of the program
        """
        print('Congratulations, have a nice day!')


def main():
    """
    Main function for entry point
    """
    bot = Bot()
    bot.greet('Aid', '2020')
    bot.remind_name()
    bot.guess_age()
    bot.count()
    bot.test()
    bot.end()


if __name__ == '__main__':
    main()
