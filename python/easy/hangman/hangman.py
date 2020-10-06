import random
from string import ascii_lowercase

words = ["python", "java", "kotlin", "javascript"]

print("\nH A N G M A N\n")

random.shuffle(words)
riddle = list(words[0])
tries = 8
hidden = len(riddle) * ["-"]
typed = []

choice = None
while True:
    try:
        print('Type "play" to play the game, "exit" to quit: \n', end="")
        choice = input()
        if choice not in ["play", "exit"]:
            raise ValueError()
        if choice == "exit":
            break
    except ValueError:
        continue

    won = False
    while tries > 0 and not won:
        try:
            print()
            print("".join(hidden))
            print("Input a letter: ", end="")
            guess = input()

            if len(guess) != 1:
                raise ValueError("You should input a single letter")

            if guess not in ascii_lowercase:
                raise ValueError("It is not an ASCII lowercase letter")

            if guess in typed:
                raise ValueError("You already typed this letter")
            else:
                typed.append(guess)

            if guess in riddle:
                for i in range(len(riddle)):
                    if guess == riddle[i]:
                        hidden[i] = guess
                if hidden == riddle:
                    won = True
            else:
                print("No such letter in the word")
                tries -= 1
        except ValueError as e:
            print(e)

    if won:
        print(f"You guessed the word {''.join(riddle)}")
        print("You survived!")
    else:
        print("You are hanged!")
