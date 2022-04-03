""" Every sudoku generator needs to have this method"""
from abc import ABC, abstractmethod


class SudokuGenerator(ABC):
    @abstractmethod
    def get_sudoku(self):
        pass
