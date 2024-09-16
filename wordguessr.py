import json
import os
import random
import re
import unicodedata
from colored import cprint
import configparser  # Import configparser to read ini files

# Global variables for translations
TRANSLATIONS = {}
LANGUAGE_FILE = 'language.ini'
LANGUAGE_DIR = 'languages/'

def load_translation(language_code):
    """Load the translation file for the given language code."""
    global TRANSLATIONS
    translation_file = os.path.join(LANGUAGE_DIR, f'{language_code}.json')
    
    if not os.path.isfile(translation_file):
        cprint(get_translation("translation_file_not_found", translation_file), 'red')
        return

    with open(translation_file, 'r', encoding='utf-8') as file:
        TRANSLATIONS = json.load(file)

def get_translation(key, *args):
    """Get the translation for a given key and format it with arguments."""
    translation = TRANSLATIONS.get(key, key)  # Fallback to key if not found
    if args:
        translation = translation.format(*args)
    return translation

def read_language_ini():
    """Read the language.ini file to determine the default language."""
    config = configparser.ConfigParser()
    if not os.path.isfile(LANGUAGE_FILE):
        cprint(get_translation("language_ini_not_found"), 'yellow')
        with open(LANGUAGE_FILE, 'w', encoding='utf-8') as file:
            file.write('[Settings]\nlanguage=en\n')
        return 'en'

    config.read(LANGUAGE_FILE)
    
    if 'Settings' in config:
        return config['Settings'].get('language', 'en')

    return 'en'

def load_categories(filename):
    """Load categories from a file."""
    filename = sanitize_filename(filename)
    if not os.path.isfile(filename):
        cprint(get_translation("categories_file_not_found", filename), 'red')
        return []
    
    with open(filename, 'r', encoding='utf-8') as file:
        categories = [line.strip() for line in file]

    return categories

def sanitize_filename(filename):
    normalized_filename = unicodedata.normalize('NFKD', filename)
    sanitized_filename = re.sub(r'[^\w/.]+', '_', normalized_filename)
    return sanitized_filename.lower()

def load_words(category):
    """Load words from a file corresponding to the category."""
    filename = f'wordLists/{category}.txt'
    filename = sanitize_filename(filename)
    if not os.path.isfile(filename):
        cprint(get_translation("words_file_not_found", filename), 'red')
        return []

    with open(filename, 'r', encoding='utf-8') as file:
        words = [line.strip().upper() for line in file]

    return words

def choose_category(categories):
    """Let the player choose a category."""
    print(get_translation("choose_category"))
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.capitalize()}")

    while True:
        try:
            choice = int(input(get_translation("category_choice_prompt")).strip())
            if 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                # Check if words are available in the chosen category
                if load_words(selected_category):
                    return selected_category
                else:
                    cprint(get_translation("no_words_available"), 'red')
            else:
                cprint(get_translation("invalid_choice"), 'red')
        except ValueError:
            cprint(get_translation("invalid_input"), 'red')

def choose_word(words):
    """Choose a random word from the list."""
    return random.choice(words)

def display_progress(word, guessed_letters):
    """Display the current progress of the word."""
    display_word = ' '.join([letter if letter in guessed_letters or not letter.isalpha() else '_' for letter in word])
    print(display_word)

def play_game():
    """Play the WordGuessR game."""
    language_code = read_language_ini()
    load_translation(language_code)
    
    categories = load_categories('categories.txt')
    
    if not categories:
        cprint(get_translation("no_categories_available"), 'red')
        return
    
    while True:
        category = choose_category(categories)
        words = load_words(category)
        
        if not words:
            cprint(get_translation("no_words_available_for_category"), 'red')
            continue
        
        word = choose_word(words)
        word_length = len(word)
        
        # Adjust the number of tries based on the length of the word
        tries = max(8, 15 - word_length)
        
        guessed = False
        guessed_letters = []
        
        cprint(get_translation("welcome_message"), 'blue')
        # Change this line to include the tries left translation
        cprint(get_translation("tries_left", tries), fore_rgb=[252, 144, 3])
        display_progress(word, guessed_letters)
        print("\n")
        
        while not guessed and tries > 0:
            guess = input(get_translation("guess_prompt")).upper()
            
            if len(guess) == 1 and guess.isalnum():
                if guess in guessed_letters:
                    cprint(get_translation("already_guessed", guess), 'yellow')
                elif guess not in word:
                    cprint(get_translation("not_in_word", guess), 'red')
                    tries -= 1
                    guessed_letters.append(guess)
                else:
                    cprint(get_translation("good_guess", guess), 'green')
                    guessed_letters.append(guess)
                    if all(letter in guessed_letters or not letter.isalpha() for letter in word):
                        guessed = True
            elif len(guess) == len(word):
                if guess == word:
                    guessed = True
                else:
                    cprint(get_translation("not_the_word", guess), 'red')
                    tries -= 1
            else:
                cprint(get_translation("invalid_guess"), 'red')
            
            if not guessed:
                # Change this line as well
                cprint(get_translation("tries_left", tries), fore_rgb=[138, 138, 138])
                display_progress(word, guessed_letters)
                print("\n")
            
            if tries < 10 and len(guess) == len(word) and guess != word:
                cprint(get_translation("guess_whole_word_warning"), 'red')
        
        if guessed:
            cprint(get_translation("congratulations", word), 'green')
        else:
            cprint(get_translation('out_of_tries', word), 'red')
        
        play_again = input(get_translation("play_again")).strip().lower()
        if play_again == 'y':
            if input(get_translation("choose_new_category")).strip().lower() == 'y':
                continue
            else:
                break
        else:
            cprint(get_translation("thanks_for_playing"), 'yellow')
            break

if __name__ == "__main__":
    play_game()