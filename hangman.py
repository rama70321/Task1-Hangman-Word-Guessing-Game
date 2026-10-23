
import random
from pathlib import Path

# Maximum number of incorrect attempts
MAX_ATTEMPTS = 6

# Fallback words used when words.txt is not available
DEFAULT_WORDS = [
    "python", "computer", "programming", "hangman",
    "science", "keyboard", "internet", "student",
    "developer", "machine", "learning", "security"
]

# ASCII gallows stages: one stage for each number of mistakes
HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
"""
]


def load_words():
    """Load words from words.txt or use default words."""
    file_path = Path(__file__).with_name("words.txt")

    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                words = [
                    line.strip().lower()
                    for line in file
                    if line.strip().isalpha()
                ]

            if words:
                return words
        except OSError:
            pass

    return DEFAULT_WORDS


def display_game(secret_word, guessed_letters, wrong_guesses):
    """Display the gallows, masked word, and guessed letters."""
    print(HANGMAN_STAGES[wrong_guesses])

    masked_word = " ".join(
        letter if letter in guessed_letters else "_"
        for letter in secret_word
    )

    print("Word:             ", masked_word)
    print("Wrong guesses:    ", wrong_guesses, "/", MAX_ATTEMPTS)

    if guessed_letters:
        print("Guessed letters:  ",
              " ".join(sorted(guessed_letters)))
    else:
        print("Guessed letters:   None")

    print("-" * 40)


def play_hangman():
    """Run one complete Hangman game."""
    words = load_words()
    secret_word = random.choice(words)

    # Sets automatically prevent duplicate letters
    guessed_letters = set()
    wrong_letters = set()
    wrong_guesses = 0

    print("=" * 40)
    print("       WELCOME TO HANGMAN!")
    print("=" * 40)
    print("Guess the secret word one letter at a time.")
    print(f"You have {MAX_ATTEMPTS} incorrect attempts.")
    print("Type 'quit' to exit the game.\n")

    while wrong_guesses < MAX_ATTEMPTS:
        display_game(secret_word, guessed_letters, wrong_guesses)

        # Check whether all letters have been guessed
        if all(letter in guessed_letters for letter in secret_word):
            print("CONGRATULATIONS! YOU WIN!")
            print("You guessed the word:", secret_word)
            return

        guess = input("Enter a letter: ").strip().lower()

        # Allow the player to quit
        if guess == "quit":
            print("\nGame ended. The word was:", secret_word)
            return

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input! Enter one letter at a time.\n")
            continue

        # Do not penalize repeated guesses
        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try another letter.\n")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"Correct! '{guess}' is in the word.\n")
        else:
            wrong_letters.add(guess)
            wrong_guesses += 1
            print(f"Wrong! '{guess}' is not in the word.\n")

    # Show the final stage and defeat message
    display_game(secret_word, guessed_letters, wrong_guesses)
    print("GAME OVER! YOU LOST.")
    print("The secret word was:", secret_word)


if __name__ == "__main__":
    play_hangman()
