from tkinter import Tk, Label, Button, Entry, messagebox, LabelFrame, Canvas, PhotoImage
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

        # Create and layout widgets for word length selection
        self.create_word_length_widgets()
        self.layout_word_length_widgets()

    def create_word_length_widgets(self):
        # Create labels and buttons for word length selection
        self.title_label = Label(self.window, text="Wordle Game")
        self.length_label = Label(self.window, text="Select word length:")
        self.length_4_button = Button(self.window, text="4", command=lambda: self.select_length(4))
        self.length_5_button = Button(self.window, text="5", command=lambda: self.select_length(5))
        self.length_6_button = Button(self.window, text="6", command=lambda: self.select_length(6))
        self.guessing_canvas = Canvas(self.window, width=650, height=300)
        
    def layout_word_length_widgets(self):
        # Layout labels and buttons for word length selection
        self.title_label.pack()
        self.length_label.pack()
        self.length_4_button.pack(side="left")
        self.length_5_button.pack(side="left")
        self.length_6_button.pack(side="left")
        self.guessing_canvas.pack()
        
        # Load and display the image on the guessing canvas
        self.img = PhotoImage(file="4 5 or 6 .png")
        self.guessing_canvas.create_image(0.00000001,0.00000001, anchor="nw", image=self.img)

    def create_guessing_widgets(self):
        # Create labels, buttons, and entry field for guessing
        self.clear_board()  # Clear the previous board if any
        self.letters_frame = self.create_letters_frame()
        self.guess_label = Label(self.window, text="Enter your guess:")
        self.guess_entry = Entry(self.window)
        self.submit_button = Button(self.window, text="Submit", command=self.submit_guess)
        self.new_game_button = Button(self.window, text="New Game", command=self.new_game)
        self.exit_button = Button(self.window, text="Exit", command=self.window.destroy)  # Close all screens
        self.guesses_label = Label(self.window, text="Guesses:")
        self.guessing_canvas = Canvas(self.window, width=200, height=100)

    def layout_guessing_widgets(self):
        # Layout labels, buttons, and entry field for guessing
        self.letters_frame.pack(side="top")
        self.guess_label.pack()
        self.guess_entry.pack()
        self.submit_button.pack(side="left")
        self.new_game_button.pack(side="left")
        self.exit_button.pack(side="left")
        self.guesses_label.pack()
     

    def clear_board(self):
        # Clear the previous board if any
        if hasattr(self, "letters_frame"):
            self.letters_frame.pack_forget()
        if hasattr(self, "guess_label"):
            self.guess_label.pack_forget()
        if hasattr(self, "guess_entry"):
            self.guess_entry.pack_forget()
        if hasattr(self, "submit_button"):
            self.submit_button.pack_forget()
        if hasattr(self, "new_game_button"):
            self.new_game_button.pack_forget()
        if hasattr(self, "exit_button"):
            self.exit_button.pack_forget()
        if hasattr(self, "guesses_label"):
            self.guesses_label.pack_forget()

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

    def select_length(self, length):
        self.word_length = length
        self.create_guessing_widgets()  # Create the guessing widgets
        self.layout_guessing_widgets()  # Layout the guessing widgets
        self.new_game()

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

        self.guess_entry.delete(0, "end")  # Clear the guess entry field

    def new_game(self):
        if self.word_length == 0:
            return

        # Clear the letter highlights before starting a new game
        self.clear_letter_highlights()

        self.word = self.load_word()
        self.guesses = []
        self.remaining_guesses = 6
        self.update_guesses_label()
        self.highlight_letters("")

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
            button.config(highlightbackground="SystemButtonFace")

    def highlight_letters(self, guess):
        self.clear_letter_highlights()
        for i, letter in enumerate(guess):
            button_found = False
            if letter == self.word[i]:
                for button in self.letters_frame.winfo_children():
                    button_letter = button['text']
                    if letter == button_letter:
                        button.config(highlightbackground="green")
                        button_found = True
                        break
            elif letter in self.word:
                for button in self.letters_frame.winfo_children():
                    button_letter = button['text']
                    if letter == button_letter:
                        button.config(highlightbackground="yellow")
                        button_found = True
                        break
            if not button_found:
                for button in self.letters_frame.winfo_children():
                    button_letter = button['text']
                    if letter == button_letter:
                        button.config(highlightbackground="red")
                        break

    def guess_letter(self, letter):
        current_text = self.guess_entry.get()
        self.guess_entry.delete(0, "end")
        self.guess_entry.insert("end", current_text + letter)

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    window = Tk()
    game = WordleGame(window)
    game.start()

