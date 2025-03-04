import random
import time
import json
import os
import tkinter as tk
from tkinter import messagebox

# List of words and their hints categorized
categories = {
    "programming_languages": [
        ("python", "A popular programming language"),
        ("java", "A programming language used for building Android apps"),
        ("swift", "A programming language used for iOS development")
    ],
    "games": [
        ("hangman", "The name of the game you're playing"),
        ("chess", "A strategy board game"),
        ("monopoly", "A board game about real estate")
    ]
}

def get_random_word_and_hint(category):
    return random.choice(categories[category])

def display_word(word, guessed_letters):
    displayed_word = ""
    for letter in word:
        if letter in guessed_letters:
            displayed_word += letter + " "
        else:
            displayed_word += "_ "
    return displayed_word.strip()

def calculate_score(word, guessed_letters, max_incorrect_guesses, incorrect_guesses, full_word_guessed):
    correct_guesses = 0
    for letter in word:
        if letter in guessed_letters:
            correct_guesses += 1

    score = (correct_guesses * 10) - (incorrect_guesses * 5)
    
    if full_word_guessed:
        score += 50  # Adding bonus points for guessing the full word

    return max(score, 0)

def check_all_letters_guessed(word, guessed_letters):
    for letter in word:
        if letter not in guessed_letters:
            return False
    return True

# GUI setup
def setup_gui():
    def start_game():
        global word, hint, guessed_letters, incorrect_guesses, hint_used, full_word_guessed, start_time, max_incorrect_guesses, time_limit
        guessed_letters = set()
        incorrect_guesses = 0
        hint_used = False
        full_word_guessed = False
        start_time = time.time()

        difficulty = difficulty_var.get().lower()
        if difficulty == "easy":
            max_incorrect_guesses = 8
            time_limit = 120  # 2 minutes
        elif difficulty == "medium":
            max_incorrect_guesses = 6
            time_limit = 90  # 1.5 minutes
        elif difficulty == "hard":
            max_incorrect_guesses = 4
            time_limit = 60  # 1 minute
        else:
            max_incorrect_guesses = 6
            time_limit = 90  # default to medium
            messagebox.showinfo("Info", "Invalid difficulty level. Setting to Medium by default.")

        category = category_var.get()
        if category.lower() in categories:
            word, hint = get_random_word_and_hint(category.lower())
        else:
            word, hint = get_random_word_and_hint("games")
            messagebox.showinfo("Info", "Invalid category. Choosing a random word from the available categories.")

        hint_button.config(state="normal")
        guess_button.config(state="normal")
        guess_entry.config(state="normal")
        update_display()

    def update_display():
        displayed_word = display_word(word, guessed_letters)
        word_label.config(text=displayed_word)
        remaining_guesses_label.config(text=f"Guesses left: {max_incorrect_guesses - incorrect_guesses}")
        elapsed_time = time.time() - start_time
        time_left_label.config(text=f"Time left: {int(time_limit - elapsed_time)} seconds")

    def check_guess(guess=None):
        global incorrect_guesses, full_word_guessed,hint_used
        if not guess:
            guess = guess_entry.get().lower()
            guess_entry.delete(0, tk.END)

        if time.time() - start_time > time_limit:
            end_game(False, "Time's up! You didn't guess the word in time.")
            return

        if guess == 'hint':
            if not hint_used:
                messagebox.showinfo("Hint", f"Hint: {hint}")
                hint_used = True
            else:
                messagebox.showinfo("Hint", "You've already used your hint!")
            return

        if guess in guessed_letters:
            messagebox.showinfo("Info", "You've already guessed that letter!")
        elif guess == word:
            full_word_guessed = True
            end_game(True, f"Congratulations! You guessed the word '{word}'!")
        elif guess in word:
            guessed_letters.add(guess)
            if check_all_letters_guessed(word, guessed_letters):
                full_word_guessed = True
                end_game(True, f"Congratulations! You guessed the word '{word}'!")
            else:
                update_display()
        else:
            incorrect_guesses += 1
            if incorrect_guesses >= max_incorrect_guesses:
                end_game(False, f"Game over! The word was '{word}'.")
            else:
                messagebox.showinfo("Info", f"Incorrect guess! You have {max_incorrect_guesses - incorrect_guesses} guesses left.")
                update_display()
    def end_game(won, message):
        global guessed_letters, incorrect_guesses, full_word_guessed, start_time
        if won:
            elapsed_time = time.time() - start_time
            score = calculate_score(word, guessed_letters, max_incorrect_guesses, incorrect_guesses, full_word_guessed)
            messagebox.showinfo("Game Over", f"{message}\nYou scored {score} points in {int(elapsed_time)} seconds.")
        else:
            messagebox.showinfo("Game Over", message)
        
        guessed_letters = set()
        incorrect_guesses = 0
        full_word_guessed = False
        word_label.config(text="")
        remaining_guesses_label.config(text="")
        time_left_label.config(text="")
        hint_button.config(state="disabled")
        guess_button.config(state="disabled")
        guess_entry.config(state="disabled")

    # Main program execution
    root = tk.Tk()
    root.title("Hangman Game")

    # GUI Elements
    difficulty_var = tk.StringVar(value="Medium")
    category_var = tk.StringVar(value="Games")

    tk.Label(root, text="Difficulty:").pack()
    tk.OptionMenu(root, difficulty_var, "Easy", "Medium", "Hard").pack()

    tk.Label(root, text="Category:").pack()
    tk.OptionMenu(root, category_var, *categories.keys()).pack()

    start_button = tk.Button(root, text="Start Game", command=start_game)
    start_button.pack()

    hint_button = tk.Button(root, text="Hint", state="disabled", command=lambda: check_guess('hint'))
    hint_button.pack()

    word_label = tk.Label(root, text="")
    word_label.pack()

    remaining_guesses_label = tk.Label(root, text="")
    remaining_guesses_label.pack()

    time_left_label = tk.Label(root, text="")
    time_left_label.pack()

    guess_entry = tk.Entry(root, state="disabled")
    guess_entry.pack()

    guess_button = tk.Button(root, text="Guess", state="disabled", command=check_guess)
    guess_button.pack()

    root.mainloop()

setup_gui()
