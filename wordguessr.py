import requests
import webbrowser
import os
import random
import re
import unicodedata
from colored import *

def get_local_version():
    if not os.path.isfile('version.txt'):
        return None
    with open('version.txt', 'r', encoding='utf-8') as file:
        local_version = file.read().strip()
    return local_version

def get_remote_version():
    repo_url = 'https://raw.githubusercontent.com/WorkSquash/WordGuessr/master/version.txt'
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        remote_version = response.text.strip()
        return remote_version
    except requests.exceptions.HTTPError as http_err:
        cprint(f"HTTP error occurred: {http_err}", 'red')
    except requests.exceptions.ConnectionError:
        cprint("Error: Could not connect to the internet.", 'red')
    except requests.exceptions.Timeout:
        cprint("Error: The request timed out.", 'red')
    except requests.exceptions.RequestException as err:
        cprint(f"An error occurred: {err}", 'red')
    return None

def check_version():
    local_version = get_local_version()
    if not local_version:
        cprint("Local version file not found.", 'red')
        return
    remote_version = get_remote_version()
    if not remote_version:
        cprint("Could not retrieve remote version.", 'red')
        return
    if local_version != remote_version:
        cprint(f"A new version is available: {remote_version}. You have version: {local_version}.", 'yellow')
        update = input("Do you want to update? (y/n): ").strip().lower()
        if update == 'y':
            repo_page_url = 'https://github.com/WorkSquash/WordGuessr/releases'
            webbrowser.open(repo_page_url)
        else:
            cprint("You chose not to update.", 'yellow')
    else:
        cprint("You have the latest version.", 'green')

def readme(filename):
    if not os.path.isfile(filename):
        cprint(f"File {filename} does not exist.", 'red')
        return
    with open(filename, 'r', encoding='utf-8') as file:
        readme_content = file.read()
    print(f'{readme_content}\n')

def load_categories(filename):
    filename = sanitize_filename(filename)
    if not os.path.isfile(filename):
        cprint(f"File {filename} does not exist.", 'red')
        return []
    with open(filename, 'r', encoding='utf-8') as file:
        categories = [line.strip() for line in file]
    return categories

def sanitize_filename(filename):
    normalized_filename = unicodedata.normalize('NFKD', filename)
    sanitized_filename = re.sub(r'[^\w/.]+', '_', normalized_filename)
    return sanitized_filename.lower()

def load_words(category):
    filename = f'wordLists/{category}.txt'
    filename = sanitize_filename(filename)
    if not os.path.isfile(filename):
        cprint(f"File {filename} does not exist.", 'red')
        return []
    with open(filename, 'r', encoding='utf-8') as file:
        words = [line.strip().upper() for line in file]
    return words

def choose_category(categories):
    print("Choose a category:")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.capitalize()}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                if load_words(selected_category):
                    return selected_category
                else:
                    cprint("No words available for this category. Please choose another one.", 'red')
            else:
                cprint("Invalid choice. Please enter a valid number.", 'red')
        except ValueError:
            cprint("Invalid input. Please enter a number.", 'red')

def choose_word(words):
    return random.choice(words)

def display_progress(word, guessed_letters):
    display_word = ' '.join([letter if letter in guessed_letters or not letter.isalpha() else '_' for letter in word])
    print(display_word)

def play_game():
    check_version()
    readme('readme.txt')
    
    categories = load_categories('categories.txt')
    
    if not categories:
        cprint("No categories available.", 'red')
        return
    
    category = choose_category(categories)
    words = load_words(category)
    
    if not words:
        cprint("No words available for this category.", 'red')
        return
    
    word = choose_word(words)
    word_length = len(word)
    
    # Adjust the number of tries based on the length of the word
    tries = max(8, 15 - word_length)
    
    guessed = False
    guessed_letters = []
    
    cprint("Let's play WordGuessR!\n", 'blue')
    cprint(f"You have {tries} tries", fore_rgb=[252, 144, 3])
    display_progress(word, guessed_letters)
    print("\n")
    
    while not guessed and tries > 0:
        guess = input("Please guess a letter or the word: ").upper()
        
        if len(guess) == 1 and guess.isalnum():
            if guess in guessed_letters:
                cprint(f"You already guessed the character {guess}", 'yellow')
            elif guess not in word:
                cprint(f"{guess} is not in the word.", 'red')
                tries -= 1
                guessed_letters.append(guess)
            else:
                cprint(f"Good job, {guess} is in the word!", 'green')
                guessed_letters.append(guess)
                if all(letter in guessed_letters or not letter.isalpha() for letter in word):
                    guessed = True
        elif len(guess) == len(word):
            if guess != word:
                cprint(f"{guess} is not the word.", 'red')
                tries -= 1
            else:
                guessed = True
        else:
            cprint("Not a valid guess.", 'red')
        
        if not guessed:
            cprint(f"You have {tries} tries left", fore_rgb=[138, 138, 138])
            display_progress(word, guessed_letters)
            print("\n")
        
        # Allow the player to guess the whole word only after a certain number of unsuccessful attempts
        if tries < 10 and len(guess) == len(word) and guess != word:
            cprint("You can only guess the whole word after a few unsuccessful attempts.", 'red')
    
    if guessed:
        cprint(f"Congratulations, you guessed the word '{word}'!", 'green')
    else:
        cprint('Sorry you ran out of tries.', 'red')
        cprint(f'The word was {word}', 'red')
    
    input("Press any key to close the game...")

if __name__ == "__main__":
    play_game()