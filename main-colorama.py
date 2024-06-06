import requests
import webbrowser
import os
import random
import re
import unicodedata
from colorama import init, Fore
init()

def get_local_version():
    # Read the local version number from the version.txt file
    if not os.path.isfile('version.txt'):
        return None
    with open('version.txt', 'r', encoding='utf-8') as file:
        local_version = file.read().strip()
    return local_version

def get_remote_version():
    # Get the latest version number from the GitHub repository
    repo_url = 'https://raw.githubusercontent.com/WorkSquash/WordGuessr/master/version.txt'
    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        remote_version = response.text.strip()
        return remote_version
    except requests.exceptions.HTTPError as http_err:
        print(Fore.RED + f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "Error: Could not connect to the internet.")
    except requests.exceptions.Timeout:
        print(Fore.RED + "Error: The request timed out.")
    except requests.exceptions.RequestException as err:
        print(Fore.RED + f"An error occurred: {err}")
    return None

def check_version():
    local_version = get_local_version()
    if not local_version:
        print(Fore.RED + "Local version file not found.")
        return
    remote_version = get_remote_version()
    if not remote_version:
        print(Fore.RED + "Could not retrieve remote version.")
        return
    if local_version != remote_version:
        print(f"A new version is available: {remote_version}. You have version: {local_version}.")
        update = input("Do you want to update? (y/n): ").strip().lower()
        if update == 'y':
            repo_page_url = 'https://github.com/WorkSqush/WordGuessr'
            webbrowser.open(repo_page_url)
        else:
            print("You chose not to update.")
    else:
        print("You have the latest version.")

def load_categories(filename):
    # Load categories from a file
    with open(filename, 'r', encoding='utf-8') as file:
        categories = [line.strip() for line in file]
    return categories

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    normalized_filename = unicodedata.normalize('NFKD', filename)
    sanitized_filename = re.sub(r'[^\w/.]+', '_', normalized_filename)
    return sanitized_filename.lower()

def load_words(category):
    # Load words from a file corresponding to the category
    filename = f'wordLists/{category}.txt'
    filename = sanitize_filename(filename)
    if not os.path.isfile(filename):
        print(Fore.RED + f"File {filename} does not exist.")
        return []
    with open(filename, 'r', encoding='utf-8') as file:
        words = [line.strip().upper() for line in file]
    return words

def read_readme(filename):
    # Read and print the contents of the readme file
    if not os.path.isfile(filename):
        print(Fore.RED + f"File {filename} does not exist.")
        return
    with open(filename, 'r', encoding='utf-8') as file:
        readme_content = file.read()
    print(readme_content + "\n")

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
        print(Fore.RED + "No words available for this category.")
        return
    
    word = choose_word(words)
    
    guessed = False
    guessed_letters = []
    tries = 10
    
    print("Let's play WordGuessr!")
    print(f"You have {tries} tries left.")
    display_progress(word, guessed_letters)
    print("\n")
    
    while not guessed and tries > 0:
        guess = input("Please guess a letter, number, or word: ").upper()
        try:
            guess = guess.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            print(Fore.RED + "Invalid input. Please enter a valid UTF-8 encoded character.")
            continue
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
        print(Fore.GREEN + f"Congratulations, you guessed the word '{word}'!")
    else:
        print('Sorry you ran out of tries.')
        print(Fore.RED + f'The word was {word}')
    
    input(Fore.RESET + "Press any key to close the game...")

if __name__ == "__main__":
    play_game()
