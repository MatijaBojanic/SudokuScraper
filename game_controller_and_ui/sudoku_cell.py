""" Sudoku board is made out of multiple cells"""
import tkinter as tk


class SudokuCell(tk.Entry):
    """ Individual cell of the grid"""

    def __init__(self, sudoku, row, column, original_value, master=None, **kwargs):
        self.lock = False
        self.sudoku = sudoku
        self.row = row
        self.column = column
        self.original_value = original_value
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, justify='center', **kwargs)
        self.old_value = ''
        self.var.trace('w', self.check)
        self.get, self.set = self.var.get, self.var.set

    def check(self, *args):
        """ Make sure that what we are inputting is a digit. If its 0 clear the field
                 If the value is used up then display the text as red """
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
            if self.get() in self.sudoku.sudoku_game_logic.used_values(self.row, self.column) and not self.lock:
                self.configure(foreground='Red')
            else:
                self.configure(foreground='Black')
        self.sudoku.sudoku_game_logic.update_state(self.row, self.column, self.get())

    def update_original_value(self, new_value, *args):
        """Update the value that is displayed in the sudoku cell
        and style it properly, either as a locked or allowed input field"""
        if new_value == '':
            self.config(bg='#d3d3d3')
            self.original_value = new_value
            self.set(new_value)
            self.config(state='normal')
            self.lock = False
        else:
            self.lock = True
            self.config(state='readonly')
            self.configure(foreground='Black')
            self.config(readonlybackground='#ADD8E6')
            self.original_value = new_value
            self.set(new_value)

    def input_value(self, new_value):
        """This allows buttons to input values into sudoku cells"""
        if not self.lock:
            self.old_value = new_value
            self.set(new_value)

    def leading_char_added(self, input_value):
        """We have to check if the user inputted a char as leading.
        Ex: If input was '2', and the user inputs '1' such
        that the new input is '12'"""
        if input_value == '':
            return ''
        if len(input_value) < 2:
            return input_value
        if input_value[-1] == self.old_value:
            input_value = input_value[-2]
        return input_value
