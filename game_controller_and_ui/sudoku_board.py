"""UI for sudoku"""
import tkinter as tk
from game_controller_and_ui.sudoku_cell import SudokuCell


class SudokuBoard:
    """Sudoku board container ui"""
    def __init__(self, sudoku_game_logic):
        self.save_game_window = None
        self.sudoku_game_logic = sudoku_game_logic
        self.input_fields = []
        self.sudoku_board_state = None
        self.window = tk.Tk()
        self.window.maxsize(width=500, height=440)
        self.window.minsize(width=500, height=440)
        self.make_input_fields()
        self.make_buttons()

    def run(self):
        """You need to run after creating every ui
        element otherwise tk fails"""
        self.window.mainloop()

    def new_game_ui(self, sudoku_puzzle):
        """Get puzzle and fill input fields"""
        self.sudoku_board_state = sudoku_puzzle
        self.fill_grid()

    def fill_grid(self):
        """Go through each input field and give it new value"""
        input_fields_counter = 0
        for row in range(0, 9):
            for column in range(0, 9):
                self.input_fields[input_fields_counter].update_original_value(self.sudoku_board_state[row][column])
                input_fields_counter = input_fields_counter + 1

    def make_input_fields(self):
        """Create input fields"""
        for row in range(0, 9):
            x_axis = 0
            for column in range(0, 9):
                sudoku_cell = SudokuCell(self, row, column, '', self.window)
                self.input_fields.append(sudoku_cell)
                sudoku_cell.place(x=x_axis, y=row * 40, width=40, height=40)
                x_axis = x_axis + 40

    def make_buttons(self):
        """ Make new_game, submit, show_solution buttons
        as well as a numpad with clear button"""
        new_puzzle_button = tk.Button(self.window, text="New Sudoku", command=lambda:self.sudoku_game_logic.new_game())
        submit_button = tk.Button(self.window, text="Submit", command=self.win_check)
        show_solution_button = tk.Button(self.window, text="Show Solution", command=self.show_solution)
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
        new_puzzle_button.place(relx=0.5, rely=0.95, anchor='center')
        submit_button.place(relx=0.5, rely=0.87, anchor='center')
        show_solution_button.place(relx=0.77, rely=0.92)

    def show_solution(self):
        """Show solution given puzzle"""
        self.sudoku_board_state = self.sudoku_game_logic.sudoku_solution
        self.fill_grid()

    def win_check(self):
        """Check if the game is won in the controller
        If won ask for name+surname to save the result
        Otherwise popup fail msg"""
        if self.sudoku_game_logic.is_solved():
            self.won_game_window()
        else:
            fail_button = tk.Button(self.window, text="The solution does not fit. Try again :)",
                                    command=lambda: fail_button.place_forget())
            fail_button.place(relx=0.5, rely=0.5, anchor='center')

    def won_game_window(self):
        """Open new window form that asks for name and surname inputs"""
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
        """Submit name and surname results to the controller,
        close the form window and start a new game"""
        self.sudoku_game_logic.save_game(name, surname)
        save_game_window.destroy()
        save_game_window.update()
        self.sudoku_game_logic.new_game()

    @staticmethod
    def set_text(text, cell):
        """Put text into input_field. Used by numpad buttons"""
        cell.input_value(text)
        return

