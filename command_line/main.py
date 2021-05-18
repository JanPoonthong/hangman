import os.path
import sys

# Import gui/main.py
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import gui.main

hangman_status = gui.main.hangman_status
hangman_status = 6


def display_hangman(status):
    stages = [  # final state: head, torso, both arms, and both legs
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     / \\
           -
        """,
        # head, torso, both arms, and one leg
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |     /
           -
        """,
        # head, torso, and both arms
        """
           --------
           |      |
           |      O
           |     \\|/
           |      |
           |
           -
        """,
        # head, torso, and one arm
        """
           --------
           |      |
           |      O
           |     \\|
           |      |
           |
           -
        """,
        # head and torso
        """
           --------
           |      |
           |      O
           |      |
           |      |
           |
           -
        """,
        # head
        """
           --------
           |      |
           |      O
           |
           |
           |
           -
        """,
        # initial empty state
        """
           --------
           |      |
           |
           |
           |
           |
           -
        """,
    ]
    return stages[status]


if __name__ == "__main__":
    while True:
        gui.main.display_word = ""

        for letter in gui.main.WORD:
            if letter in gui.main.GUESSED:
                gui.main.display_word += letter + " "
            else:
                gui.main.display_word += "_ "
        print(gui.main.display_word)

        guess = input("Guess a letter: ").upper()
        gui.main.GUESSED.append(guess)

        if guess not in gui.main.WORD:
            hangman_status -= 1
            print(display_hangman(hangman_status))

        gui.main.won = True
        for letter in gui.main.WORD:
            if letter not in gui.main.GUESSED:
                gui.main.won = False
                break

        if gui.main.won:
            print("You Won")
            break

        if hangman_status == 0:
            print("You lose")
            break

        print(f"All guesses: {gui.main.GUESSED}")
    print(f"The word was: {gui.main.WORD}")
