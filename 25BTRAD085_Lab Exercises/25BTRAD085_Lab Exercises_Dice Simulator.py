import random

while True:
    print("\n----- DICE SIMULATOR -----")

    input("Press Enter to roll the dice...")

    number = random.randint(1, 6)

    print("You rolled:", number)

    choice = input("Roll again? (yes/no): ")

    if choice.lower() != "yes":
        print("Thank you for playing!")
        break