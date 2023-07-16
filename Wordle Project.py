from tkinter import Tk, Label, Button, Entry, messagebox, LabelFrame
import string
import random

class WordleGame:
    def __init__(self, window):
        self.window = window
        self.window.title("Wordle Game")
        self.word_length = 0
        self.word = ""
        self.guesses = []
        self.remaining_guesses = 6

        # Create and layout widgets
        self.create_widgets()

    def create_widgets(self):
        # Create labels, buttons, and entry field
        self.title_label = Label(self.window, text="Wordle Game")
        self.length_label = Label(self.window, text="Select word length:")
        self.length_4_button = Button(self.window, text="4", command=lambda: self.select_length(4))
        self.length_5_button = Button(self.window, text="5", command=lambda: self.select_length(5))
        self.length_6_button = Button(self.window, text="6", command=lambda: self.select_length(6))
        self.submit_button = Button(self.window, text="Submit", command=self.submit_guess)
        self.new_game_button = Button(self.window, text="New Game", command=self.new_game)
        self.exit_button = Button(self.window, text="Exit", command=self.window.quit)
        self.letters_frame = self.create_letters_frame()
        self.guess_label = Label(self.window, text="Enter your guess:")
        self.guess_entry = Entry(self.window)
        self.guesses_label = Label(self.window, text="Guesses:")

    def layout_widgets(self):
        # Layout labels, buttons, and entry field
        self.title_label.pack()
        self.length_label.pack()
        self.length_4_button.pack(side="left")
        self.length_5_button.pack(side="left")
        self.length_6_button.pack(side="left")
        self.submit_button.pack(side="left")
        self.new_game_button.pack(side="left")
        self.exit_button.pack(side="left")
        self.letters_frame.pack()
        self.guess_label.pack()
        self.guess_entry.pack()
        self.guesses_label.pack()

    def create_letters_frame(self):
        # Create frame to hold letter buttons
        frame = LabelFrame(self.window, text="Letters")

        # Create letter buttons
        row = 0
        col = 0
        for letter in string.ascii_uppercase:
            button = Button(frame, text=letter, command=lambda l=letter: self.guess_letter(l))
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col == 7:
                col = 0
                row += 1

        return frame

    def layout_widgets(self):
        # Layout labels, buttons, and entry field
        self.title_label.pack()
        self.length_label.pack()
        self.length_4_button.pack(side="left")
        self.length_5_button.pack(side="left")
        self.length_6_button.pack(side="left")
        self.submit_button.pack(side="left")
        self.new_game_button.pack(side="left")
        self.exit_button.pack(side="left")
        self.letters_frame.pack()

    def select_length(self, length):
        self.word_length = length
        self.new_game()
        self.layout_widgets()

    def submit_guess(self):
        guess = self.guess_entry.get().upper()

        # Validate input
        if not guess.isalpha() or len(guess) != self.word_length:
            messagebox.showwarning("Invalid Guess", f"Please enter a {self.word_length}-letter word.")
            return

        # Check if the guess matches the word
        if guess == self.word:
            messagebox.showinfo("Congratulations", "You guessed the word correctly!")
            self.new_game()
        else:
            self.guesses.append(guess)
            self.remaining_guesses -= 1
            if self.remaining_guesses == 0:
                messagebox.showinfo("Game Over", f"Out of guesses! The word was: {self.word}")
                self.new_game()
            else:
                self.update_guesses_label()
                self.highlight_letters(guess)

        self.guess_entry.delete(0, "end")

    def new_game(self):
        if self.word_length == 0:
            return

        self.word = self.load_word()
        self.guesses = []
        self.remaining_guesses = 6
        self.update_guesses_label()
        self.clear_letter_highlights()

    def load_word(self):
        filename = f"random_{self.word_length}word.txt"
        with open(filename, "r") as file:
            words = file.read().splitlines()
        return random.choice(words).upper()

    def update_guesses_label(self):
        guesses_text = "\n".join(self.guesses)
        self.guesses_label.config(text=f"Guesses:\n{guesses_text}")

    def clear_letter_highlights(self):
        for button in self.letters_frame.winfo_children():
            button.config(bg="SystemButtonFace")

    def highlight_letters(self, guess):
        self.clear_letter_highlights()
        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                button = self.letters_frame.winfo_children()[ord(letter) - ord("A")]
                button.config(bg="green")
            elif letter in self.word:
                button = self.letters_frame.winfo_children()[ord(letter) - ord("A")]
                button.config(bg="yellow")

    def guess_letter(self, letter):
        current_text = self.guess_entry.get()
        self.guess_entry.delete(0, "end")
        self.guess_entry.insert("end", current_text + letter)

    def start(self):
        self.layout_widgets()
        self.guess_entry = Entry(self.window)
        self.guess_entry.pack()
        self.guesses_label = Label(self.window, text="Guesses:")
        self.guesses_label.pack()
        self.window.mainloop()

window = Tk()
game = WordleGame(window)
game.start()






