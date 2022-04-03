import requests
from bs4 import BeautifulSoup
from Generator.sudoku_generator import SudokuGenerator
import numpy as np

class SudokuScrapperSudokuweb(SudokuGenerator):
    web_url = 'https://www.sudokuweb.org/'

    def get_sudoku(self):
        htmlContent = self.get_html_content()
        return self.parse_html(htmlContent)

    def get_html_content(self):
        sudoku_response = requests.get(self.web_url)
        return sudoku_response.text

    def parse_html(self, htmlContent):
        soup = BeautifulSoup(htmlContent, 'lxml')
        table_body = soup.table
        sudoku = np.empty((0,9), str)
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [elem.text.strip() for elem in cols]
            sudoku = np.append(sudoku, np.array([cols]), axis=0)
        return sudoku

SudokuScrapperSudokuweb().get_sudoku()