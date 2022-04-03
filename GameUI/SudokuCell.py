import tkinter as tk

# Individual cell of the grid
class SudokuCell(tk.Entry):
    def __init__(self, sudoku, row, column, expected_value, master=None, **kwargs):
        self.expected_value = expected_value
        self.sudoku = sudoku
        self.row = row
        self.column = column
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, justify='center', **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    # Make sure that what we are inputting is a digit. If its 0 clear the field
    # If the value is used up then display the text as red
    def check(self, *args):
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
        if self.get() != '':
            if self.get() in self.sudoku.used_values(self.row, self.column):
                self.configure(foreground='Red')
            else:
                self.configure(foreground='Black')
        self.sudoku.update_state(self.row, self.column, self.get())

    # We have to check if the user inputted a char as leading. Exmpl: If input was '2', and the user inputs '1' such
    # that the new input is '12'
    def leading_char_added(self, input_value):
        if input_value == '':
            return ''
        if len(input_value) < 2:
            return input_value
        if input_value[-1] == self.old_value:
            input_value = input_value[-2]
        return input_value

    # This allows buttons to input values into sudoku cells
    def input_value(self, new_value):
        self.old_value = new_value
        self.set(new_value)

    # Check if current input is equal to expected input
    def solved(self):
        return self.get() == self.expected_value