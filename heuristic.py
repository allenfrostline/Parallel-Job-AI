from factory import BOTTLENECK, COLS, ROWS

# Below are several intrumental functions
def is_block(cell):
    return cell not in [0, -2]

def is_empty(cell):
    return cell in [0, -2]

def u_score(hours, k):
    return abs(k**2 / (hours - 1e-2) + 1. / (BOTTLENECK - hours + 1e-2) - (k + 1)**2 / BOTTLENECK) / 4

# Below are all the heuristics with scores normalized to [0,1] and weights assigned in ai.py
def max_height(state):
    board = state.board
    for idx, row in enumerate(board):
        for cell in row:
            if is_block(cell):
                return (len(board) - idx - 1.) / ROWS

def avg_height(state):
    board = state.board
    total_height = 0
    for height, row in enumerate(reversed(board[1:])):
        for cell in row:
            if is_block(cell):
                total_height += height
    return (total_height / COLS) / ROWS

def avg_hours(state):
    return u_score(state.avghours, 7)

def max_hours(state):
    return u_score(state.maxhours, 4)

def scv_hours(state):
    return 1e-2 / (state.scvhours + 1e-2)

def avg_machines(state):
    return state.avgmachines / COLS

def max_machines(state):
    return state.avgmachines / COLS

def scv_machines(state):
    return 1e-2 / (state.scvmachines + 1e-2)