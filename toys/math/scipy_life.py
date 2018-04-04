import numpy as np
from scipy.signal import convolve2d

data = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
"""

data = """
......
......
.###..
......
"""

data = """
.#................
..#...............
###...............
..................
..................
..................
..................
..................
..................
..................
"""

data = data.strip()
board = np.array([
    [c == '#' for c in line]
    for line in data.split('\n')
], dtype=np.int)

print(board)

# print(convolve2d(board, np.ones((3, 3)))[1:-1, 1:-1])
# print(convolve2d(board, np.ones((3, 3)), mode='same'))

def step(board):
    conv1 = convolve2d(board, np.ones((3, 3)), mode='same')
    next_board = (conv1 == 3) | (conv1 - board == 3)
    return next_board.astype(np.int)

for i in range(10):
    board = step(board)
    print(board)
