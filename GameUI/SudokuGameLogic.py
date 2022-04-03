import tkinter as tk
import numpy as np
import random

class SudokuGameLogic:
    def __init__(self, sudoku_generator, sudoku_board=None):
        self.sudoku_ui = None
        self.sudoku_solution = None
        self.current_state = None
        self.sudoku_generator = sudoku_generator
        self.sudoku_board = sudoku_board

    def new_game(self):
        if self.sudoku_board == None:
            return
        sudoku_arr = self.new_puzzle()
        self.sudoku_board.new_game_ui(sudoku_arr)

    def new_puzzle(self):
        self.sudoku_solution = self.sudoku_generator.get_sudoku()
        self.current_state = self.sudoku_solution
        self.randomly_generate_puzzle_from_solved_sudoku()
        return self.current_state

    # save current game and start a new one
    def won_game(self, name, surname):
        self.save_game(name, surname)
        self.new_game()

    def save_game(self, name, surname):
        file_name = name + '_' + surname + '.txt'
        if file_name == '_.txt':
            file_name = 'solution.txt'
        f = open('./db/' + file_name, 'w')
        f.write(np.array2string(self.current_state))
        f.close()

    @staticmethod
    def roundup_to_nearest_three(index):
        roundup_float = np.ceil((index + 1) / 3) * 3
        roundup_int = np.int(roundup_float)
        return roundup_int

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

    def update_state(self, row, column, new_value):
        self.current_state[row][column] = new_value

    def randomly_generate_puzzle_from_solved_sudoku(self):
        for row in range(0, 9):
            for column in range(0, 9):
                if random.randint(0, 9) > 6:
                    self.current_state[row][column] = ''

    def solve_puzzle(self):
        pass

    def win_check(self):
        #return np.array_equal(self.sudoku_solution, self.current_state)
        return True # Temp Testing save
