import random
import copy

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_x = (col // 3) * 3
    box_y = (row // 3) * 3
    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if board[i][j] == num:
                return False
    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solve(board)
    return board

def generate_puzzle(num_visible=40):
    board = generate_full_board()
    puzzle = copy.deepcopy(board)
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for i in range(81 - num_visible):
        r, c = cells[i]
        puzzle[r][c] = 0
    return puzzle, board  # zwróć planszę startową i rozwiązanie
