from game_controller_and_ui.sudoku_board import SudokuBoard
from game_controller_and_ui.sudoku_game_logic import SudokuGameLogic
from sudoku_generators.sudoku_scrapper_sudokuweb import SudokuScrapperSudokuweb

game_logic = SudokuGameLogic(SudokuScrapperSudokuweb())
board = SudokuBoard(game_logic)
game_logic.sudoku_board = board

game_logic.new_game()
game_logic.sudoku_board.run()
