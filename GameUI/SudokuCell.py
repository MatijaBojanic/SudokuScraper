import tkinter as tk
# We have a sudoku container
# We have sudokuCells
# an invalid input would be checked on sudoku cell level
# to get it we need to track current sudoku status
# Row - column must be 1 to 9 and each square should have it. To check this we have to keep track of current inputs


class SudokuCell(tk.Entry):
    def __init__(self, sudoku, row, column, expected_number, master=None, **kwargs):
        self.sudoku = sudoku
        self.row = row
        self.column = column
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)

        self.expected_value = expected_number
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set
        # self.sudoku.check_unique(self.row, self.column)

    # Check if the value is correctly inputted (Deal with leading input)
    # Check if the input is valid. If the input is 0 or '' remove the current input
    def check(self, *args):
        #leading char check
        input_value = self.get().strip()
        input_value = self.leading_char_added(input_value)
        #check for digit input
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
        #check if the inputed digit is valid or make the field red
        if self.get() != '':
            if self.get() in self.sudoku.used_values(self.row, self.column):
                self.configure(foreground='Red')
            else:
                self.configure(foreground='Black')




    #   Check if the added char was added as the leading char
    #   Lets say the old input was '2', and we add a '3' such that the new input becomes '32'
    def leading_char_added(self, input_value):
        if input_value == '':
            return ''
        if len(input_value) < 2:
            return input_value
        if input_value[-1] == self.old_value:
            input_value = input_value[-2]
        return input_value

    def input_value(self,new_value):
        self.old_value = new_value
        self.set(new_value)

    def solved(self):
        return self.get().strip() == str(self.expected_value)