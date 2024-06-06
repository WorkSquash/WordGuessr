import requests
import webbrowser
import os
from colored import colored, cprint
import re
import random

def get_local_version():
    # Read the local version number from the version.txt file
    if not os.path.isfile('version.txt'):
        return None
    with open('version.txt', 'r') as file:
        local_version = file.read().strip()
    return local_version

def get_remote_version():
    # Get the latest version number from the GitHub repository
    repo_url = 'https://raw.githubusercontent.com/your-username/your-repo/main/version.txt'
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        remote_version = response.text.strip()
        return remote_version
    except requests.exceptions.HTTPError as http_err:
        cprint(f"HTTP error occurred: {http_err}", fore_256="red")
    except requests.exceptions.ConnectionError:
        cprint("Error: Could not connect to the internet.", fore_256="red")
    except requests.exceptions.Timeout:
        cprint("Error: The request timed out.", fore_256="red")
    except requests.exceptions.RequestException as err:
        cprint(f"An error occurred: {err}", fore_256="red")
    return None

def check_version():
    local_version = get_local_version()
    if not local_version:
        cprint("Local version file not found.", fore_256="red")
        return
    remote_version = get_remote_version()
    if not remote_version:
        cprint("Could not retrieve remote version.", fore_256="red")
        return
    if local_version != remote_version:
        print(f"A new version is available: {remote_version}. You have version: {local_version}.")
        update = input("Do you want to update? (y/n): ").strip().lower()
        if update == 'y':
            repo_page_url = 'https://github.com/WorkSquash/WordGuessr'
            webbrowser.open(repo_page_url)
        else:
            print("You chose not to update.")
    else:
        print("You have the latest version.")

def load_categories(filename):
    # Load categories from a file
    with open(filename, 'r') as file:
        categories = [line.strip() for line in file]
    return categories

def sanitize_filename(filename):
    # Replace spaces and special characters with underscores
    # Split the filename by directory separators
    parts = filename.split('/')
    # Replace spaces and special characters with underscores for each part
    parts = [re.sub(r'[^\w]', '_', part).replace('__', '_') for part in parts]
    # Join the parts back together with directory separators
    sanitized_filename = '/'.join(parts)
    return sanitized_filename.lower()

def load_words(category):
    # Load words from a file corresponding to the category
    filename = f'wordLists/{category}.txt'
    filename = sanitize_filename(filename)
    if not os.path.isfile(filename):
        cprint(f"File {filename} does not exist.", fore_256="red")
        return []
    with open(filename, 'r') as file:
        words = [line.strip().upper() for line in file]
    return words

def read_readme(filename):
    # Read and print the contents of the readme file
    if not os.path.isfile(filename):
        cprint(f"File {filename} does not exist.", fore_256="red")
        return
    with open(filename, 'r') as file:
        readme_content = file.read()
    print(f'{readme_content}\n')

def choose_category(categories):
    # Let the player choose a category
    print("Choose a category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.capitalize()}")
    choice = int(input("Enter the number of your choice: "))
    return categories[choice - 1]

def choose_word(words):
    # Choose a random word from the list
    return random.choice(words)

def display_progress(word, guessed_letters):
    # Display the current progress of the word
    display_word = ' '.join([letter if letter in guessed_letters or not letter.isalpha() else '_' for letter in word])
    print(display_word)

def play_game():
    check_version()
    read_readme('readme.txt')
    
    categories = load_categories('categories.txt')
    
    category = choose_category(categories)
    words = load_words(category)
    
    if not words:
        cprint("No words available for this category.", fore_256="red")
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
        cprint(f'The word was {word}', fore_256="red")

if __name__ == "__main__":
    play_game()
