import tkinter as tk
from tkinter import messagebox
import random

WORDS = [
    "APPLE", "BANANA", "CAMERA", "DOLPHIN", "ELEPHANT",
    "FLOWER", "GALAXY", "HORIZON", "ISLAND", "JUNGLE",
    "KITTEN", "LADDER", "MIRROR", "NOTEBOOK", "OCEAN",
    "PYTHON", "QUARTZ", "RAINBOW", "SUNFLOWER", "TORNADO",
    "UNICORN", "VOLCANO", "WATERFALL", "XYLOPHONE", "ZEPPELIN",
    "ANCHOR", "BALLOON", "CACTUS", "DRAGON", "ENGINE",
    "FOSSIL", "GUITAR", "HAMMER", "ICEBERG", "JAGUAR",
    "KOALA", "LANTERN", "MAGNET", "NEBULA", "OXYGEN",
    "PUZZLE", "ROCKET", "SATELLITE", "TREASURE", "UMBRELLA",
    "VORTEX", "WHISTLE", "YACHT", "ZIPPER", "CRYSTAL"
]


class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman - Main Menu")
        self.root.geometry("800x800")

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True)

        self.title_underscore_frame = tk.Frame(self.frame)
        self.title_underscore_frame.pack(pady=(30, 200))

        title_text = "HANGMAN"
        for idx, char in enumerate(title_text):
            tk.Label(self.title_underscore_frame, text=char, font=(
                "Arial", 24, "bold"), width=2).grid(row=0, column=idx, padx=2)
            tk.Label(self.title_underscore_frame, text="_", font=(
                "Arial", 20), width=2).grid(row=1, column=idx, padx=2)

        self.start_game_button = tk.Button(self.frame, text="Start Game", font=(
            "Arial", 16), width=30, height=3, command=self.start_game)
        self.start_game_button.pack(pady=10)
        HoverableButton(self.start_game_button)

        self.custom_mode_button = tk.Button(self.frame, text="Custom Mode", font=(
            "Arial", 16), width=30, height=3, command=self.custom_mode)
        self.custom_mode_button.pack(pady=10)
        HoverableButton(self.custom_mode_button)

        self.quit_button = tk.Button(self.frame, text="Quit Game", font=(
            "Arial", 16), width=30, height=3, command=root.quit)
        self.quit_button.pack(pady=5)
        HoverableButton(self.quit_button)

    def start_game(self, custom_word=None):
        self.root.geometry("1500x700")
        self.frame.destroy()
        HangmanGame(self.root, custom_word)

    def custom_mode(self):
        self.frame.destroy()
        self.CustomWordBuilder(self.root)

    class CustomWordBuilder:
        def __init__(self, root):
            self.root = root
            self.root.geometry("1500x700")
            self.word = ""

            self.frame = tk.Frame(root)
            self.frame.pack(expand=True, fill="both")

            title = tk.Label(self.frame, text="Enter a Word",
                             font=("Arial", 24, "bold"))
            title.pack(pady=30)

            self.word_display = tk.StringVar()
            self.word_display.set(" _ " * 10)
            self.display_label = tk.Label(
                self.frame, textvariable=self.word_display, font=("Arial", 20))
            self.display_label.pack(pady=20)

            self.backspace_frame = tk.Frame(self.frame)
            self.backspace_frame.pack(pady=(0, 10), fill="x")

            self.backspace_btn = tk.Button(
                self.backspace_frame,
                text="Backspace",
                font=("Arial", 14, "bold"),
                width=12,
                height=2,
                command=self.backspace
            )
            self.backspace_btn.pack(anchor="e", padx=40)
            HoverableButton(self.backspace_btn)

            self.keyboard_frame = tk.Frame(self.frame)
            self.keyboard_frame.pack(pady=20)
            self.create_keyboard()

            self.start_game_btn = tk.Button(
                self.frame,
                text="Start Game",
                font=("Arial", 14, "bold"),
                width=30,
                height=3,
                command=self.start_game,
                state="disabled"
            )
            self.start_game_btn.pack(pady=30)
            HoverableButton(self.start_game_btn)

        def create_keyboard(self):
            keys = [
                "QWERTYUIOP",
                "ASDFGHJKL",
                "ZXCVBNM"
            ]

            for row_keys in keys:
                row = tk.Frame(self.keyboard_frame)
                row.pack(pady=5)
                for letter in row_keys:
                    btn = tk.Button(
                        row, text=letter,
                        font=("Arial", 14, "bold"),
                        width=9, height=3,
                        command=lambda l=letter: self.add_letter(l)
                    )
                    btn.pack(side="left", padx=4)
                    HoverableButton(btn)

        def add_letter(self, letter):
            if len(self.word) < 10:
                self.word += letter
                self.update_display()

        def backspace(self):
            self.word = self.word[:-1]
            self.update_display()

        def update_display(self):
            if self.word:
                self.word_display.set(
                    " ".join(self.word + "_" * (10 - len(self.word))))
                self.start_game_btn.config(state="normal")
            else:
                self.word_display.set("_ " * 10)
                self.start_game_btn.config(state="disabled")

        def start_game(self):
            self.frame.destroy()
            HangmanGame(self.root, self.word.upper())


class HangmanGame:
    def __init__(self, root, custom_word=None):
        self.is_custom = custom_word is not None
        self.root = root
        self.root.title("Hangman Game")

        self.word = custom_word if custom_word else random.choice(
            WORDS).upper()
        self.guessed_letters = set()
        self.mistakes = 0
        self.max_mistakes = 7
        self.wins = 0
        self.losses = 0

        self.create_menu(self.is_custom)
        self.second_row_indent = 0.5
        self.third_row_indent = 2
        self.create_ui()

        for letter, btn in self.letter_buttons.items():
            HoverableButton(btn)

        self.end_message_text = None
        self.end_message_color = None

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=2,
                         padx=10, pady=10, sticky="nsew")
        self.canvas.bind("<Configure>", lambda e: self.redraw_canvas())
        self.draw_gallows()

        if not self.is_custom:
            self.score_label = tk.Label(
                root, text=f"Wins: {self.wins} | Losses: {self.losses}", font=("Arial", 14))
            self.score_label.grid(row=2, column=0, sticky="w", padx=20)

        self.root.bind("<KeyPress>", self.handle_keypress)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=3)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=2)

        self.update_word_display()

    def create_menu(self, is_custom):
        menu_bar = tk.Menu(self.root)

        main_menu = tk.Menu(menu_bar, tearoff=0)

        main_menu.add_command(
            label="Main Menu", command=self.back_to_main_menu)
        main_menu.add_separator()
        if not is_custom:
            main_menu.add_command(label="Restart", command=self.restart_game)
            main_menu.add_separator()
        main_menu.add_command(label="Quit Game", command=self.root.quit)

        menu_bar.add_cascade(label="Menu", menu=main_menu)

        self.root.config(menu=menu_bar)

    def back_to_main_menu(self):
        self.root.config(menu=None)
        for widget in self.root.winfo_children():
            widget.destroy()
        MainMenu(self.root)

    def create_ui(self):
        self.word_display = tk.StringVar()
        tk.Label(self.root, textvariable=self.word_display, font=("Arial", 20)).grid(
            row=1, column=0, columnspan=2, sticky="nsew")

        if not self.is_custom:
            self.next_button = tk.Button(
                self.root,
                text="Next Word",
                font=("Arial", 14, "bold"),
                width=20,
                height=2,
                state="disabled",
                command=self.next_round
            )
            self.next_button.grid(
                row=2, column=1, sticky="e", padx=20, pady=(10, 0))
            HoverableButton(self.next_button)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(
            row=3, column=0, columnspan=2, pady=10, sticky="nsew")

        self.letter_buttons = {}

        keyboard_rows = [
            ("QWERTYUIOP", 0),
            ("ASDFGHJKL", 20),
            ("ZXCVBNM", 0),
        ]

        for row_letters, indent in keyboard_rows:
            row_frame = tk.Frame(self.buttons_frame)
            row_frame.pack(pady=5)

            tk.Label(row_frame, width=indent // 10).pack(side="left")

            for letter in row_letters:
                btn = tk.Button(
                    row_frame, text=letter, font=("Arial", 14, "bold"),
                    width=9, height=3,
                    command=lambda l=letter: self.guess_letter(l)
                )
                btn.pack(side="left", padx=6, pady=4)
                self.letter_buttons[letter] = btn

                HoverableButton(btn)

    def update_word_display(self):
        self.word_display.set(
            " ".join([l if l in self.guessed_letters else "_" for l in self.word]))

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        self.guessed_letters.add(letter)

        if letter in self.word:
            self.letter_buttons[letter].config(
                state="disabled", bg="#008000", disabledforeground="#FFFFFF")
        else:
            self.letter_buttons[letter].config(
                state="disabled", bg="#A9A9A9", disabledforeground="#DDDDDD")
            self.mistakes += 1
            self.draw_hangman()

        self.update_word_display()
        self.check_game_status()

    def draw_gallows(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width() or 300
        height = self.canvas.winfo_height() or 300
        base_x1, base_x2 = width * 0.3, width * 0.7
        pole_x, top_x2 = (base_x1 + base_x2) / 2, base_x2
        top_y = height * 0.2

        self.canvas.create_line(base_x1, height * 0.9,
                                base_x2, height * 0.9, width=5)
        self.canvas.create_line(pole_x, top_y, pole_x, height * 0.9, width=5)
        self.canvas.create_line(pole_x, top_y, top_x2, top_y, width=5)

    def draw_hangman(self):
        self.canvas.delete("hangman")
        width = self.canvas.winfo_width() or 300
        height = self.canvas.winfo_height() or 300
        head_x, head_y = width * 0.7, height * 0.3
        top_y = height * 0.2

        parts = [
            lambda: self.canvas.create_line(
                head_x, top_y-2, head_x, head_y, width=5, tags="hangman"),
            lambda: self.canvas.create_oval(
                head_x-20, head_y, head_x+20, head_y+40, width=5, tags="hangman"),
            lambda: self.canvas.create_line(
                head_x, head_y+40, head_x, head_y+100, width=5, tags="hangman"),
            lambda: self.canvas.create_line(
                head_x, head_y+50, head_x-30, head_y+80, width=5, tags="hangman"),
            lambda: self.canvas.create_line(
                head_x, head_y+50, head_x+30, head_y+80, width=5, tags="hangman"),
            lambda: self.canvas.create_line(
                head_x, head_y+98, head_x-30, head_y+150, width=5, tags="hangman"),
            lambda: self.canvas.create_line(
                head_x, head_y+98, head_x+30, head_y+150, width=5, tags="hangman")
        ]

        for i in range(min(self.mistakes, len(parts))):
            parts[i]()

    def redraw_canvas(self):
        self.draw_gallows()
        self.draw_hangman()

        if self.end_message_text:
            self.draw_end_message(self.end_message_text,
                                  self.end_message_color)

    def draw_end_message(self, message, color):
        self.end_message_text = message
        self.end_message_color = color

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.create_text(
            20, 20,
            anchor="nw",
            text=message,
            fill=color,
            font=("Arial", 20, "bold"),
            tags="end_message",
            justify="left"
        )

    def check_game_status(self):
        if set(self.word) <= self.guessed_letters:
            self.draw_end_message("You Win!", "green")
            self.wins += 1
            self.disable_buttons()
        elif self.mistakes >= self.max_mistakes:
            self.draw_end_message(
                f"You Lose!\nThe word was: {self.word}", "red")
            self.losses += 1
            self.disable_buttons()

        self.update_score()
        self.next_button.config(state="normal")

    def disable_buttons(self):
        for btn in self.letter_buttons.values():
            btn.config(state="disabled", bg="#A9A9A9",
                       disabledforeground="#DDDDDD")

    def next_round(self):
        self.word = random.choice(WORDS).upper()
        self.guessed_letters.clear()
        self.mistakes = 0
        self.end_message_text = None
        self.end_message_color = None

        self.canvas.delete("hangman", "end_message")
        self.draw_gallows()
        self.update_word_display()

        for btn in self.letter_buttons.values():
            btn.config(state="normal", bg="SystemButtonFace", fg="black")

        if not self.is_custom:
            self.next_button.config(state="disabled")

    def update_score(self):
        if not self.is_custom:
            self.score_label.config(
                text=f"Wins: {self.wins} | Losses: {self.losses}")

    def restart_game(self):
        self.word = random.choice(WORDS).upper()
        self.guessed_letters.clear()
        self.mistakes = 0
        self.end_message_text = None
        self.end_message_color = None

        self.canvas.delete("hangman", "end_message")
        self.draw_gallows()
        self.update_word_display()

        for btn in self.letter_buttons.values():
            btn.config(state="normal", bg="SystemButtonFace", fg="black")

        self.update_score()

    def handle_keypress(self, event):
        letter = event.char.upper()
        if letter in self.letter_buttons and self.letter_buttons[letter]['state'] == 'normal':
            self.guess_letter(letter)

    def show_about(self):
        messagebox.showinfo(
            "About", "Hangman Game\nDeveloped using Tkinter in Python.")


class HoverableButton:
    def __init__(self, button):
        self.button = button
        self.add_hover_effect()

    def add_hover_effect(self):
        self.button.bind("<Enter>", self.on_hover)
        self.button.bind("<Leave>", self.on_hover_leave)

    def on_hover(self, event):
        if self.button['state'] != 'disabled':
            self.button.config(bg="#E0E0E0")

    def on_hover_leave(self, event):
        if self.button['state'] != 'disabled':
            self.button.config(bg="SystemButtonFace")


if __name__ == "__main__":
    root = tk.Tk()
    MainMenu(root)
    root.mainloop()
