import tkinter as tk
import random
import numpy as np

from GameUI.SudokuCell import SudokuCell


# This class represents the game itself. It generates the UI and contains checks for valid inputs
class Sudoku:
    def __init__(self, sudoku_generator):
        self.sudoku_solution = None
        self.current_state = None
        self.input_fields = None
        self.sudoku_generator = sudoku_generator
        self.window = tk.Tk()
        self.window.maxsize(width=500, height=440)
        self.window.minsize(width=500, height=440)
        self.new_game()
        self.make_buttons()
        self.window.mainloop()

    # Grab another puzzle and make a grid for it
    def new_game(self):
        self.input_fields = []
        sudoku_array = self.sudoku_generator.get_sudoku()
        self.sudoku_solution = sudoku_array
        self.current_state = sudoku_array
        self.make_grid()

    # Creates the grid input fields
    def make_grid(self):
        for row in range(0, len(self.sudoku_solution[0])):
            x_axis = 0
            for column in range(0, len(self.sudoku_solution[row])):
                if random.randint(0, 9) > 6:
                    temp = SudokuCell(self, row, column, self.sudoku_solution[row][column], self.window)
                    self.input_fields.append(temp)
                    self.current_state[row][column] = ''
                else:
                    locked_field_value = tk.StringVar(self.window, value=str(self.sudoku_solution[row][column]))
                    temp = tk.Entry(readonlybackground='#ADD8E6', textvariable=locked_field_value, justify='center',
                                    state='readonly')
                temp.place(x=x_axis, y=row * 40, width=40, height=40)
                x_axis = x_axis + 40

    # Make UI buttons, for input, for new game, and for submitting results
    def make_buttons(self):
        reset_button = tk.Button(self.window, text="New Sudoku", command=self.new_game)
        submit_button = tk.Button(self.window, text="Submit", command=self.win_check)
        input_one = tk.Button(self.window, text="1", command=lambda: self.set_text("1", self.window.focus_get()))
        input_two = tk.Button(self.window, text="2", command=lambda: self.set_text("2", self.window.focus_get()))
        input_three = tk.Button(self.window, text="3", command=lambda: self.set_text("3", self.window.focus_get()))
        input_four = tk.Button(self.window, text="4", command=lambda: self.set_text("4", self.window.focus_get()))
        input_five = tk.Button(self.window, text="5", command=lambda: self.set_text("5", self.window.focus_get()))
        input_six = tk.Button(self.window, text="6", command=lambda: self.set_text("6", self.window.focus_get()))
        input_seven = tk.Button(self.window, text="7", command=lambda: self.set_text("7", self.window.focus_get()))
        input_eight = tk.Button(self.window, text="8", command=lambda: self.set_text("8", self.window.focus_get()))
        input_nine = tk.Button(self.window, text="9", command=lambda: self.set_text("9", self.window.focus_get()))
        input_clear = tk.Button(self.window, text="Clear", command=lambda: self.set_text("", self.window.focus_get()))
        reset_button.place(relx=0.5, rely=0.95, anchor='center')
        submit_button.place(relx=0.5, rely=0.87, anchor='center')
        input_one.place(relx=0.75, rely=0.25)
        input_two.place(relx=0.83, rely=0.25)
        input_three.place(relx=0.91, rely=0.25)
        input_four.place(relx=0.75, rely=0.15)
        input_five.place(relx=0.83, rely=0.15)
        input_six.place(relx=0.91, rely=0.15)
        input_seven.place(relx=0.75, rely=0.05)
        input_eight.place(relx=0.83, rely=0.05)
        input_nine.place(relx=0.91, rely=0.05)
        input_clear.place(relx=0.81, rely=0.35)

    # This applies button value to focused entry
    def set_text(self, text, cell):
        cell.input_value(text)
        return

    # Checks if cells are correctly filled. If any single one isn't, the game is not over yet.
    def win_check(self):
        for cell in self.input_fields:
            if not cell.solved():
                fail_button = tk.Button(self.window, text="The solution does not fit. Try again :)",
                                        command=lambda: fail_button.place_forget())
                fail_button.place(relx=0.5, rely=0.5, anchor='center')
                return False
        self.won_game_window()

    # Opens up a new window in which we can input name and surname of the player
    def won_game_window(self):
        self.save_game_window = tk.Toplevel(self.window)
        self.save_game_window.title("You Solved It!")
        self.save_game_window.geometry("200x120")
        name_var = tk.StringVar()
        surname_var = tk.StringVar()
        name_label = tk.Label(self.save_game_window, text='Name', font=('calibre', 10, 'bold'))
        name_entry = tk.Entry(self.save_game_window, textvariable=name_var, font=('calibre', 10, 'normal'))
        surname_label = tk.Label(self.save_game_window, text='Surname', font=('calibre', 10, 'bold'))
        surname_entry = tk.Entry(self.save_game_window, textvariable=surname_var, font=('calibre', 10, 'normal'))
        save_btn = tk.Button(self.save_game_window, text='Save Solution',
                             command=lambda: self.won_game(self.save_game_window, name_var, surname_var))
        name_label.pack()
        name_entry.pack()
        surname_label.pack()
        surname_entry.pack()
        save_btn.pack()

    # Save the game, close the window and start a new game
    def won_game(self, save_game_window, name, surname):
        self.save_game(name, surname)
        save_game_window.destroy()
        save_game_window.update()
        self.new_game()

    # Create a file with format name_surname.txt that contains the board state
    def save_game(self, name, surname):
        file_name = name.get() + '_' + surname.get() + '.txt'
        if file_name == '_.txt':
            file_name = 'solution.txt'
        f = open('./db/' + file_name, 'w')
        f.write(np.array2string(self.current_state))
        f.close()

    # We use this to figure out which sudoku square (matrix 3x3)  of the grid we are in
    @staticmethod
    def roundup_to_nearest_three(index):
        roundup_float = np.ceil((index + 1) / 3) * 3
        roundup_int = np.int(roundup_float)
        return roundup_int

    # We can't use the same value twice in a row column or sudoku square, so here we check for what has already
    # been used up
    def used_values(self, row, column):
        row_values = np.unique(self.current_state[row, :])
        col_values = np.unique(self.current_state[:, column])
        row_end_pos = self.roundup_to_nearest_three(row)
        col_end_pos = self.roundup_to_nearest_three(column)
        box_values = np.unique(self.current_state[row_end_pos - 3:row_end_pos, col_end_pos - 3:col_end_pos])
        all_values = np.concatenate((row_values, col_values, box_values), axis=None)
        used_values = np.unique(all_values)
        if used_values[0] == '':
            used_values = np.delete(used_values, 0)
        return used_values

    # We update the current state so we can validate inputs
    def update_state(self, row, column, new_value):
        self.current_state[row][column] = new_value
