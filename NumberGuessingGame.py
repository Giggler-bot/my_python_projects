import random

guess_number = random.randint(1, 100)

guesses = 0

print("------Number Guessing Game------")

while True:
    guess = input("Guess a number between 1 and 100: ")

    if not guess.isdigit():
        guess = input("Please enter a number: ")
        continue

    guess = int(guess)
    guesses += 1

    if guess > guess_number:
        print("You guessed too high")
    elif guess < guess_number:
        print("You guessed too low")
    else:
        print("You guessed correctly")
        print("You guessed the number in " + str(guesses) + " guesses")
        break






