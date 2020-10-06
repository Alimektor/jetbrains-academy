import random


class RockPaperScissors:
    def __init__(self):
        self.__rules = {
            "rock": ["fire", "scissors", "snake", "human", "tree", "wolf", "sponge"],
            "fire": ["scissors", "snake", "human", "tree", "wolf", "sponge", "paper"],
            "scissors": ["snake", "human", "tree", "wolf", "sponge", "paper", "air"],
            "snake": ["human", "tree", "wolf", "sponge", "paper", "air", "water"],
            "human": ["tree", "wolf", "sponge", "paper", "air", "water", "dragon"],
            "tree": ["wolf", "sponge", "paper", "air", "water", "dragon", "devil"],
            "wolf": ["sponge", "paper", "air", "water", "dragon", "devil", "lightning"],
            "sponge": ["paper", "air", "water", "dragon", "devil", "lightning", "gun"],
            "paper": ["air", "water", "dragon", "devil", "lightning", "gun", "rock"],
            "air": ["water", "dragon", "devil", "lightning", "gun", "rock", "fire"],
            "water": ["dragon", "devil", "lightning", "gun", "rock", "fire", "scissors"],
            "dragon": ["devil", "lightning", "gun", "rock", "fire", "scissors", "snake"],
            "devil": ["lightning", "gun", "rock", "fire", "scissors", "snake", "human"],
            "lightning": ["gun", "rock", "fire", "scissors", "snake", "human", "tree"],
            "gun": ["rock", "fire", "scissors", "snake", "human", "tree", "wolf"]
        }
        self.__default_options = {
            "rock": ["scissors"],
            "scissors": ["paper"],
            "paper": ["rock"]
        }
        self.__options = {}
        self.__list_options = list(self.__default_options)
        self.__player_turn = None
        self.__computer_turn = None
        self.__name = "Tim"
        self.__file_name = "rating.txt"
        # with open(self.__file_name, "r+") as text_file:
        #     print("Tim 350", file=text_file)
        #     print("Jane 200", file=text_file)
        #     print("Alex 400", file=text_file)

    def __lose(self):
        return self.__player_turn in self.__options[self.__computer_turn]

    def __draw(self):
        return not self.__lose() and not self.__win()

    def __win(self):
        return self.__computer_turn in self.__options[self.__player_turn]

    def __is_exit(self):
        return self.__player_turn == "!exit"

    def __check_invalid(self):
        return self.__player_turn not in self.__list_options

    def __is_rating(self):
        return self.__player_turn == "!rating"

    def __set_temp_name(self):
        self.__name = input("Enter your name: ")
        with open(self.__file_name, "r") as text_file:
            lines = text_file.readlines()
        lines = [line.split() for line in lines]
        table_score = {}
        for name, score in lines:
            table_score[name] = score
        if self.__name in table_score.keys():
            self.__temp_score = int(table_score[self.__name])
        else:
            self.__temp_score = 0
        print(f"Hello, {self.__name}")

    def __set_name(self):
        self.__name = input("Enter your name: ")
        with open(self.__file_name, "r") as text_file:
            lines = text_file.readlines()
        lines = [line.split() for line in lines]
        table_score = {}
        for name, score in lines:
            table_score[name] = score
        if self.__name not in table_score.keys():
            table_score[self.__name] = 0
        with open(self.__file_name, "w+") as text_file:
            for name in table_score:
                print(f"{name} {table_score[name]}", file=text_file)
        print(f"Hello, {self.__name}")

    def __rating(self):
        with open(self.__file_name, "r+") as text_file:
            lines = text_file.readlines()
        lines = [line.split() for line in lines]
        table_score = {}
        for name, score in lines:
            table_score[name] = score
        with open(self.__file_name, "r+") as text_file:
            for name in table_score:
                print(f"{name} {table_score[name]}", file=text_file)
        return table_score[self.__name]

    def __rating_temp(self):
        return self.__temp_score

    def __add_temp_score(self, adding):
        self.__temp_score += int(adding)

    def __add_score(self, adding):
        with open(self.__file_name, "r+") as text_file:
            lines = text_file.readlines()
        lines = [line.split() for line in lines]
        table_score = {}
        for name, score in lines:
            table_score[name] = int(score)
        table_score[self.__name] += int(adding)
        with open(self.__file_name, "r+") as text_file:
            for name in table_score:
                print(f"{name} {table_score[name]}", file=text_file)

    def __set_options(self):
        options = input().split(",")
        if len(options) >= 3:
            for option in options:
                self.__options[option] = self.__rules[option]
        else:
            self.__options = self.__default_options
        self.__list_options = list(self.__options)

    def main(self):
        self.__set_temp_name()
        self.__set_options()
        print("Okay, let's start")
        while True:
            self.__player_turn = input()
            self.__computer_turn = random.choice(self.__list_options)
            if self.__is_exit():
                print("Bye!")
                break
            if self.__is_rating():
                print(f"Your rating: {self.__temp_score}")
                continue
            if self.__check_invalid():
                print("Invalid input")
                continue
            if self.__lose():
                print(f"Sorry, but the computer chose {self.__computer_turn}")
            if self.__draw():
                print(f"There is a draw ({self.__computer_turn})")
                self.__add_temp_score(50)
            if self.__win():
                print(f"Well done. The computer chose {self.__computer_turn} and failed")
                self.__add_temp_score(100)


if __name__ == '__main__':
    rps = RockPaperScissors()
    rps.main()
