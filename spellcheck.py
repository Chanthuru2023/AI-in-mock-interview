import tkinter as tk
from tkinter import simpledialog, messagebox
from spellchecker import SpellChecker
from textblob import TextBlob

# Initialize the spell checker
spell = SpellChecker()

def check_spelling_and_grammar(text):
    # Spell check
    misspelled_words = spell.unknown(text.split())

    # Grammar check using TextBlob
    blob = TextBlob(text)
    corrected_text = str(blob.correct())

    # Prepare results
    result = f"Misspelled words: {', '.join(misspelled_words)}\n"
    result += f"Corrected text: {corrected_text}"

    return result

# Create a simple GUI dialog box
def show_dialog():
    ROOT = tk.Tk()
    ROOT.withdraw()  # Hide the main window

    # Show an input dialog
    user_input = simpledialog.askstring("Input", "Enter text for spelling and grammar check:")

    if user_input:
        result = check_spelling_and_grammar(user_input)
        messagebox.showinfo("Result", result)

if __name__ == "__main__":
    show_dialog()
