""" Controller for the game"""
import numpy as np
import random


class SudokuGameLogic:
    def __init__(self, sudoku_generator, sudoku_board=None):
        """ Make the controller. You need a sudoku generator and a UI controller"""
        self.sudoku_ui = None
        self.sudoku_solution = None
        self.current_state = None
        self.sudoku_generator = sudoku_generator
        self.sudoku_board = sudoku_board

    def new_game(self):
        """Generate a new puzzle and then create ui for it"""
        sudoku_arr = self.new_puzzle()
        self.sudoku_board.new_game_ui(sudoku_arr)

    def new_puzzle(self):
        """Puzzle Generators either return a solved puzzle or a partial puzzle.
        If we are given a partial puzzle we will need to hide some parts of it
        to make sudoku playable"""
        self.sudoku_solution = self.sudoku_generator.get_sudoku()
        self.current_state = self.sudoku_solution.copy()
        if self.is_solved():
            self.randomly_generate_puzzle_from_solved_sudoku()
        else:
            self.solve_puzzle()
            temp = self.sudoku_solution.copy()
            self.sudoku_solution = self.current_state.copy()
            self.current_state = temp.copy()
        return self.current_state

    def is_solved(self):
        """Check if the current_solution is valid"""
        return self.solution_valid(self.current_state)

    def won_game(self, name, surname):
        """If the game is won save and start a new sudoku puzzle"""
        self.save_game(name, surname)
        self.new_game()

    def save_game(self, name, surname):
        """Save the game as name_surname.txt"""
        file_name = name + '_' + surname + '.txt'
        if file_name == '_.txt':
            file_name = 'solution.txt'
        f = open('./db/' + file_name, 'w')
        f.write(np.array2string(self.current_state))
        f.close()

    def update_state(self, row, column, new_value):
        """Changing the current state"""
        self.current_state[row][column] = new_value

    @staticmethod
    def solution_valid(sudoku_solution):
        """Check if rows, columns or sudoku squares have a missing spot or more than 9 values"""
        for row in range(0, 9):
            row_values = np.unique(sudoku_solution[row, :])
            if len(row_values) != 9 or "" in row_values:
                return False
        for column in range(0, 9):
            col_values = np.unique(sudoku_solution[:, column])
            if len(col_values) != 9 or "" in col_values:
                return False
        for row_end in range(3,9,3):
            for column_end in range(3,9,3):
                box_values = np.unique(sudoku_solution[row_end - 3:row_end, column_end - 3:column_end])
                if len(box_values) != 9 or "" in box_values:
                    return False
        return True

    def randomly_generate_puzzle_from_solved_sudoku(self):
        """Turn a solved sudoku into a puzzle"""
        for row in range(0, 9):
            for column in range(0, 9):
                if random.randint(0, 9) > 6:
                    self.current_state[row][column] = ''

    def used_values(self, row, column):
        """Here we check for already used values,
        in a row, in a column and sudoku square"""
        row_values = np.unique(self.current_state[row, :])
        col_values = np.unique(self.current_state[:, column])
        row_end_pos = self.roundup_to_nearest_three(row)
        col_end_pos = self.roundup_to_nearest_three(column)
        box_values = np.unique(self.current_state[row_end_pos - 3:row_end_pos,
                               col_end_pos - 3:col_end_pos])
        all_values = np.concatenate((row_values, col_values, box_values), axis=None)
        used_values = np.unique(all_values)
        if used_values[0] == '':
            used_values = np.delete(used_values, 0)
        return used_values

    def solve_puzzle(self):
        """ Backtracking recursive solution"""
        found_empty_row_and_column = self.find_empty()
        if not found_empty_row_and_column:
            return True
        else:
            row, col = found_empty_row_and_column
        for input in range(1, 10):
            if str(input) not in self.used_values(row, col):
                self.current_state[row][col] = str(input)
                if self.solve_puzzle():
                    return True
                self.current_state[row][col] = ''
        return False

    def find_empty(self):
        """Find an empty spot in sudoku square"""
        for row in range(0, 9):
            for column in range(0, 9):
                if self.current_state[row][column] == '':
                    return row, column  # row, col
        return None

    @staticmethod
    def roundup_to_nearest_three(index):
        """We are rounding up to three so that we can find the square
        to which this coordinate belongs"""
        roundup_float = np.ceil((index + 1) / 3) * 3
        roundup_int = np.int(roundup_float)
        return roundup_int
