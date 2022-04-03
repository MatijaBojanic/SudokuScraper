import tkinter as tk
import numpy as np
from GameUI.SudokuCell import SudokuCell


class SudokuBoard:
    def __init__(self, sudoku_game_logic):
        self.sudoku_game_logic = sudoku_game_logic
        self.input_fields = []
        self.sudoku_board_state = None
        self.window = tk.Tk()
        self.window.maxsize(width=500, height=440)
        self.window.minsize(width=500, height=440)
        # self.make_input_fields()
        self.make_buttons()
        # self.window.mainloop()

    def run(self):
        self.window.mainloop()

    # Grab another puzzle and make a grid for it
    def new_game_ui(self, sudoku_puzzle):
        self.sudoku_board_state = sudoku_puzzle
        self.make_grid()

    def make_grid(self):
        for row in range(0, len(self.sudoku_board_state[0])):
            x_axis = 0
            for column in range(0, len(self.sudoku_board_state[row])):
                if self.sudoku_board_state[row][column] == '':
                    temp = SudokuCell(self, row, column, self.sudoku_board_state[row][column], self.window)
                    self.input_fields.append(temp)
                else:
                    locked_field_value = tk.StringVar(self.window, value=str(self.sudoku_board_state[row][column]))
                    temp = tk.Entry(readonlybackground='#ADD8E6', textvariable=locked_field_value, state='readonly')
                temp.place(x=x_axis, y=row * 40, width=40, height=40)
                x_axis = x_axis + 40



    # def make_input_fields(self):
    #     for row in range(0, 9):
    #         x_axis = 0
    #         for column in range(0, 9):
    #             sudoku_cell = SudokuCell(self, self.sudoku_game_logic, row, column,'', self.window)
    #             self.input_fields.append(sudoku_cell)
    #             sudoku_cell.place(x=x_axis, y=row * 40, width=40, height=40)
    #             x_axis = x_axis + 40


    # def update_grid(self):
    #     self.input_fields[0].update_original_value('2')
        # input_fields_counter = 0
        # for row in range(0, 9):
        #     for column in range(0, 9):
        #         self.input_fields[input_fields_counter].update_original_value(self.sudoku_board_state[row][column])



    def make_buttons(self):
        reset_button = tk.Button(self.window, text="New Sudoku", command=lambda:self.sudoku_game_logic.new_game())
        submit_button = tk.Button(self.window, text="Submit", command=self.win_check)  # TODO
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

    def set_text(self, text, cell):
        cell.input_value(text)
        return

    def win_check(self):
        if self.sudoku_game_logic.win_check():
            fail_button = tk.Button(self.window, text="The solution does not fit. Try again :)",
                                        command=lambda: fail_button.place_forget())
            fail_button.place(relx=0.5, rely=0.5, anchor='center')
            return False
        self.won_game_window()

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
                             command=lambda: self.won_game(self.save_game_window, name_var.get(), surname_var.get()))
        name_label.pack()
        name_entry.pack()
        surname_label.pack()
        surname_entry.pack()
        save_btn.pack()

    def won_game(self, save_game_window, name, surname):
        self.sudoku_game_logic.save_game(name, surname)
        save_game_window.destroy()
        save_game_window.update()
        self.sudoku_game_logic.new_game() #TODO WHAT HERE

