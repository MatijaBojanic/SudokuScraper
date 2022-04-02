import tkinter as tk
import random

from GameUI.SudokuCell import SudokuCell


class Sudoku:
    def __init__(self, sudoku_generator):
        self.input_fields = None
        self.sudoku_generator = sudoku_generator
        self.window = tk.Tk()
        self.window.maxsize(width=360, height=440)
        self.window.minsize(width=360, height=440)
        self.make_grid()
        self.window.mainloop()

    def make_grid(self):
        self.input_fields = []
        sudoku_array = self.sudoku_generator.get_sudoku()
        for row in range(0, len(sudoku_array[0])):
            x_cord = 0
            for element in sudoku_array[row]:
                if random.randint(0, 9) > 6:
                    temp = SudokuCell(element, self.window, justify='center')
                    self.input_fields.append(temp)
                else:
                    v = tk.StringVar(self.window, value=str(element))
                    temp = tk.Entry(readonlybackground='#ADD8E6', textvariable=v, justify='center', state='readonly')
                temp.place(x=x_cord, y=row * 40, width=40, height=40)
                x_cord = x_cord + 40
        submit_button = tk.Button(self.window, text="Submit", command=self.all_answers)
        reset_button = tk.Button(self.window, text="New Sudoku", command=self.make_grid)
        reset_button.place(relx=0.5, rely=0.95, anchor='center')
        submit_button.place(relx=0.5, rely=0.87, anchor='center')

    def all_answers(self):
        for cell in self.input_fields:
            if not cell.solved():
                fail_button = tk.Button(self.window, text="The solution does not fit. Try again :)",
                                        command=lambda: fail_button.place_forget())
                fail_button.place(relx=0.5, rely=0.5, anchor='center')
                return False
        win_button = tk.Button(self.window, text="You Won!  Press here for a new puzzle!", command=self.make_grid)
        win_button.place(relx=0.5, rely=0.5, anchor='center')

