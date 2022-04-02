import tkinter as tk
from Generator.SudokuScrapperSudokuweb import SudokuScrapperSudokuweb


# This is a good idea but needs more polish. We need to make it
# a) Track its expected value
# b) Be able to lock it
class DigitInput(tk.Entry):
    def __init__(self, expected_number, master=None, **kwargs):
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.expected_value = expected_number
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def solved(self):
        if int(self.get().strip()) == self.expected_value:
            return True
        return False

    #   Check if the input is valid. If the input is 0 or '' remove the current input
    def check(self, *args):  #
        # if the added thing was a leading number
        input_value = self.get().strip()
        input_value = self.leading_char_added(input_value)
        if input_value.isdigit():
            if input_value[-1] != '0':
                self.old_value = input_value[-1]
                self.set(input_value[-1])
            else:
                self.old_value = ''
                self.set('')
        elif input_value == '':
            self.old_value = ''
            self.set('')
        else:
            self.set(self.old_value)

    #   Check if the added char was added as the leading char
    def leading_char_added(self, input_value):
        if input_value == '':
            return ''
        if input_value[-1] == self.old_value:
            input_value = input_value[-2]
        return input_value


class Sudoku:
    def __init__(self, sudoku_generator):
        sudoku_array = sudoku_generator.get_sudoku()
        window = tk.Tk()
        window.maxsize(width=360, height=420)
        window.minsize(width=360, height=420)

        for row in range(0, len(sudoku_array[0])):
            x_cord = 0
            for element in sudoku_array[row]:
                temp = DigitInput(element, window)
                temp.place(x=x_cord, y=row*40, width=40, height=40)
                x_cord = x_cord + 40

        window.mainloop()
        # i will just be lazy and make a submit solution button that will send a win/try again

Sudoku(SudokuScrapperSudokuweb())
