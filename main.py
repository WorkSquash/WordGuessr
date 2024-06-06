import random
import os
from colored import colored, cprint


def load_categories(filename):
    """Load categories from a file."""
    with open(filename, 'r') as file:
        categories = [line.strip() for line in file]
    return categories

def load_words(category):
    """Load words from a file corresponding to the category."""
    filename = f'wordLists/{category}.txt'
    filename = filename.replace(' ', '_')
    filename = filename.lower()
    if not os.path.isfile(filename):
        cprint(f"File {filename} does not exist.", fore_256= "red")
        return []
    with open(filename, 'r') as file:
        words = [line.strip().upper() for line in file]
    return words

def read_readme(filename):
    """Read and print the contents of the readme file."""
    if not os.path.isfile(filename):
        cprint(f"File {filename} does not exist.", fore_256= "red")
        return
    with open(filename, 'r') as file:
        readme_content = file.read()
    print(f'{readme_content}\n')

def choose_category(categories):
    """Let the player choose a category."""
    print("Choose a category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.capitalize()}")
    choice = int(input("Enter the number of your choice: "))
    return categories[choice - 1]

def choose_word(words):
    """Choose a random word from the list."""
    return random.choice(words)

def display_progress(word, guessed_letters):
    """Display the current progress of the word."""
    display_word = ' '.join([letter if letter in guessed_letters or not letter.isalpha() else '_' for letter in word])
    print(display_word)

def play_game():
    read_readme('readme.txt')
    
    categories = load_categories('categories.txt')
    
    category = choose_category(categories)
    words = load_words(category)
    
    if not words:
        cprint("No words available for this category.", fore_256= "red")
        return
    
    word = choose_word(words)
    
    guessed = False
    guessed_letters = []
    tries = 10
    
    print("Let's play Hangman!")
    print(f"You have {tries} tries left.")
    display_progress(word, guessed_letters)
    print("\n")
    
    while not guessed and tries > 0:
        guess = input("Please guess a letter, number, or word: ").upper()
        if len(guess) == 1 and (guess.isalnum() or guess.isspace()):
            if guess in guessed_letters:
                print("You already guessed the character", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                if all(letter in guessed_letters or not letter.isalpha() for letter in word):
                    guessed = True
        elif len(guess) == len(word):
            if guess != word:
                print(guess, "is not the word.")
                tries -= 1
            else:
                guessed = True
        else:
            print("Not a valid guess.")
        
        if not guessed:
            print(f"You have {tries} tries left.")
            display_progress(word, guessed_letters)
            print("\n")
    
    if guessed:
        cprint("Congratulations, you guessed the word! You win!", fore_256="green")
    else:
        print('Sorry you ran out of tries.')
        cprint(f'The word was {word}', fore_256= "red")

if __name__ == "__main__":
    play_game()
