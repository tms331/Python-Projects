import math
import random
from queue import Queue
from dataclasses import dataclass, field
import numpy as np


f = open('results.proj1', 'a+')

# iterator goes through all neighbors of a given grid square.


@dataclass
class Box:
    open: bool = False
    open_neighbor_count: int = 0
    row: int = 0
    col: int = 0
    has_bot: bool = False
    has_button: bool = False
    has_fire: bool = False
    neighbor_north = None
    neighbor_south = None
    neighbor_east = None
    neighbor_west = None
    part_of_path = False

    def get_neighbor_coords(self):
        neighbors = ("north", self.neighbor_north), ("south", self.neighbor_south), (
            "east", self.neighbor_east), ("west", self.neighbor_west)
        return neighbors

    def set_neighbor_coords(self, i, j):
        self.neighbor_north = (i-1, j) if i-1 >= 0 else None
        self.neighbor_south = (i+1, j) if i+1 < num_rows else None
        self.neighbor_east = (i, j+1) if j+1 < num_cols else None
        self.neighbor_west = (i, j-1) if j-1 >= 0 else None

    def set_neighbors(self, i, j):
        self.neighbor_north = grid[i-1][j] if i-1 >= 0 else None
        self.neighbor_south = grid[i+1][j] if i+1 < num_rows else None
        self.neighbor_east = grid[i][j+1] if j+1 < num_cols else None
        self.neighbor_west = grid[i][j-1] if j-1 >= 0 else None

    def get_neighbors(self):
        return (self.neighbor_north, self.neighbor_south, self.neighbor_east, self.neighbor_west)

    def __iter__(self):
        return NeighborIter(self.neighbor_north, self.neighbor_south, self.neighbor_east, self.neighbor_west)

    # def __post_init__(self):
    #     self.set_neighbors(self.row, self.col)
    def __hash__(self) -> int:

        return hash((self.row, self.col))

    def __str__(self) -> str:

        if self.has_fire and self.has_button:
            self.cell = "🚨"
        elif self.has_fire:
            self.cell = "🔥"
        elif self.has_bot:
            self.cell = "🤖"
        elif self.has_button:
            self.cell = "🔴"
        elif self.open:
            self.cell = "⬜"
        elif self.has_fire and self.has_bot:
            self.cell = "🤯"
        else:
            self.cell = "⬛"

        return self.cell


def init_grid():
    ...


num_rows, num_cols = 50, 50
grid = ([[Box() for i in range(num_cols)] for j in range(num_rows)])


class NeighborIter:
    def __init__(self, neighbor_north, neighbor_south, neighbor_east, neighbor_west):
        self.neighbor_north = neighbor_north
        self.neighbor_south = neighbor_south
        self.neighbor_east = neighbor_east
        self.neighbor_west = neighbor_west
        self.neighbors = (self.neighbor_north, self.neighbor_south,
                          self.neighbor_east, self.neighbor_west)
        self.iter_count = 0

    def __next__(self):
        self.iter_count += 1
        if self.iter_count > 4:
            raise StopIteration
        return self.neighbors[self.iter_count-1]


# Create 2d array
# grid = ([[Box() for i in range(num_cols)] for j in range(num_rows)])
# Create array to hold dead ends
dead_end_array = []


# Loop to update 2d array proper rows/cols
i, j = (0, 0)
for i in range(0, num_rows):
    for j in range(0, num_cols):

        grid[i][j].row = i
        grid[i][j].col = j


def add_neighbors():
    neighbor_array = []
    i, j = (0, 0)

    for i in range(0, num_rows):
        for j in range(0, num_cols):

            if grid[i][j].open_neighbor_count == 1 and grid[i][j].open != True:
                neighbor_array.append(grid[i][j])

    return neighbor_array


def add_dead_ends():
    i, j = (0, 0)

    for i in range(0, num_rows):
        for j in range(0, num_cols):

            if grid[i][j].open_neighbor_count == 1 and grid[i][j].open == True:
                dead_end_array.append(grid[i][j])


def update_neighbors(row, col):

    if (row + 1) < num_rows:
        grid[row + 1][col].open_neighbor_count += 1

    if 0 <= (row - 1):
        grid[row - 1][col].open_neighbor_count += 1

    if (col + 1) < num_cols:
        grid[row][col + 1].open_neighbor_count += 1

    if 0 <= (col - 1):
        grid[row][col - 1].open_neighbor_count += 1


# Keeps track of open cells
# open_cells = {}
open_cells = []
# closed_cells = np.ndarray(grid.closed())
# Begin by opening a random interior box
rand_row = random.randrange(0, num_rows - 1)
rand_col = random.randrange(0, num_cols - 1)
grid[rand_row][rand_col].open = True
# open_cells[(rand_row,rand_col)] = grid[rand_row][rand_col]


# Update neighbors of newly opened box
update_neighbors(rand_row, rand_col)


# Add box with exactly one open neighbor to array
updated_arr = add_neighbors()


# Now randomly open boxes with 1 neighbor
while len(updated_arr) != 0:
    rand_num = random.randrange(0, len(updated_arr))

    updated_arr[rand_num].open = True
    update_neighbors(updated_arr[rand_num].row, updated_arr[rand_num].col)
    updated_arr = add_neighbors()


# Add dead ends to deadEndArray
add_dead_ends()


# Cut deadEndArray in half
half_end_array = []
for i in range(0, math.floor(len(dead_end_array) / 2)):
    half_end_array.append(dead_end_array[i])


# Out of half the dead ends, randomly open one of their neighbors
for i in range(0, len(half_end_array)):
    rand_num = random.randrange(0, 3)
    dead_end = dead_end_array[i]

    # open neighbor above
    if rand_num == 1 and grid[dead_end.row - 1][dead_end.col].open == False and 0 <= (dead_end.row - 1):
        grid[dead_end.row - 1][dead_end.col].open = True
        update_neighbors(dead_end.row - 1, dead_end.col)

    # open neighbor below
    elif rand_num == 2 and grid[dead_end.row + 1][dead_end.col].open == False and (dead_end.row + 1) < num_rows:
        grid[dead_end.row + 1][dead_end.col].open = True
        update_neighbors(dead_end.row + 1, dead_end.col)

    # open left neighbor
    elif rand_num == 3 and grid[dead_end.row][dead_end.col - 1].open == False and 0 <= (dead_end.col - 1):
        grid[dead_end.row][dead_end.col - 1].open = True
        update_neighbors(dead_end.row, dead_end.col - 1)

    # open right neighbor
    elif rand_num == 4 and grid[dead_end.row][dead_end.col + 1].open == False and (dead_end.col + 1) < num_cols:
        grid[dead_end.row][dead_end.col + 1].open = True
        update_neighbors(dead_end.row, dead_end.col + 1)


for i in range(len(grid)):
    for j in range(len(grid[i])):
        cell_open = grid[i][j].open
        # print("O" if cell_open else ".", end=' ')
        if cell_open:
            open_cells.append(((i, j), grid[i][j]))
    print()


class Bot:
    def __init__(self, pos) -> None:
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos


class Button:
    def __init__(self, pos) -> None:
        self.pos = pos

    def get_pos(self):
        return self.pos


class Fire:
    def __init__(self, pos) -> None:
        self.pos = pos

    def get_pos(self):
        return self.pos

# randomly place the things, distributed uniformly


roll_bot = int(random.uniform(1, len(open_cells))) - 1
roll_fire = int(random.uniform(1, len(open_cells))) - 1
roll_button = int(random.uniform(1, len(open_cells))) - 1
open_cells[roll_bot][1].has_bot = True
open_cells[roll_button][1].has_button = True
open_cells[roll_fire][1].has_fire = True

fire_cells = []
bot_init_pos = open_cells[roll_bot][0]
button_init_pos = open_cells[roll_button][0]
fire_init_pos = open_cells[roll_fire][0]
# now bfs
fire_cells.append(grid[fire_init_pos[0]][fire_init_pos[1]])


def breadth_first_search(init_state, goal_state, restricted_condition):
    #
    #
    fringe = Queue()
    fringe.put(init_state)

    closed_set = set()
    prev = {}
    prev[init_state] = None
    while not (fringe.empty()):
        current_state = fringe.get()

        if current_state == goal_state:
            return "Found", current_state, prev
        for child in current_state:
            # if child not in restricted_states and child not in closed_set:
            # print(child.row, child.col)
            if not restricted_condition(child) and child not in closed_set:
                fringe.put(child)
                prev[child] = current_state
        closed_set.add(current_state)
    return "Failed", None, None


def depth_first_search(init_state, goal_state, restricted_condition):
    #
    #
    fringe = []
    fringe.append(init_state)

    closed_set = set()
    prev = {}
    prev[init_state] = None
    while not (len(fringe) <= 0):
        current_state = fringe.pop()

        if current_state == goal_state:
            return "Found", current_state, prev
        for child in current_state:
            # if child not in restricted_states and child not in closed_set:
            # print(child.row, child.col)
            if not restricted_condition(child) and child not in closed_set:
                fringe.append(child)
                prev[child] = current_state
        closed_set.add(current_state)
    return "Failed", None, None


def backtrack(prev, current_state):

    if current_state is None:
        return []
    else:
        current_state.part_of_path = True
        path = backtrack(prev, prev[current_state])
        path.append(current_state)
        return path


# post init
for row in grid:
    for box in row:
        box.set_neighbors(box.row, box.col)

# UNUSED


def print_board(show_path=False):

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # TODO: add case where all 3 are present on one square(?)
            cell_open = grid[i][j].open
            cell_bot = grid[i][j].has_bot
            cell_button = grid[i][j].has_button
            cell_fire = grid[i][j].has_fire
            if cell_fire and cell_button:
                print("🚨", end='')
            elif cell_fire:
                print("🔥", end='')
            elif cell_bot:
                print("🤖", end='')
            elif cell_button:
                print("🚭", end='')
            elif cell_open:
                print("⬜", end='')
            elif cell_fire and cell_bot:
                print("🤯", end='')
            else:
                print("⬛", end='')
            # if cell_open:
            #     open_cells.append(((i, j), grid[i][j]))
        print()


def print_board_2(path, show_path=False):
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    print('   ', end='')
    for j, cell in enumerate(grid[0]):
        print(f'{j:0>2}'[0], end='')

        print(' ', end='')
    print()
    print('   ', end='')
    for j, cell in enumerate(grid[0]):
        print(f'{j:0>2}'[1], end='')

        print(' ', end='')
    print()
    for i, row in enumerate(grid):
        print(f'{i:0>2}', end='')
        for col in row:
            # if show_path == True and col.part_of_path and not (col.has_button or col.has_bot or col.has_button or col.has_fire):
            if show_path == True and col in path and not (col.has_button or col.has_bot or col.has_button or col.has_fire):
                print("🔵", end='')
            else:
                print(col, end='')
        print()


# def spread_fire(q):
#     closed = set()
#     burning_cells = []
#     for fire in fire_cells:

#         cells_of_interest = [neighbor for neighbor in fire.get_neighbors(
#         ) if neighbor is not None and neighbor.open and neighbor not in closed]
#         for neighbor2 in cells_of_interest:
#             closed.add(neighbor2)
#             fire_count = 0
#             neighbors_neighbors = neighbor2.get_neighbors()
#             for neighbors_neighbor in neighbors_neighbors:
#                 fire_count += 1 if neighbors_neighbor is not None and neighbors_neighbor.has_fire else 0
#         K = fire_count

#         caught_fire = np.random.random() < 1-(1-q)**K
#         if caught_fire:
#             burning_cells.append(neighbor2)
#     for cell in burning_cells:
#         cell.has_fire = True
#         fire_cells.append(cell)


def spread_fire(q):
    closed = set()
    burning_cells = []
    for row in grid:
        for col in row:
            if not col.open:
                continue
            adjacent_fires = 0
            # closed.add(col)
            neighbors = col.get_neighbors()
            for neighbor in neighbors:
                if neighbor is not None and neighbor.has_fire:
                    adjacent_fires += 1
            caught_fire = np.random.random() < 1-(1-q) ** adjacent_fires
            if caught_fire:
                burning_cells.append(col)
    for cell in burning_cells:
        cell.has_fire = True
        fire_cells.append(cell)


bot_state = grid[bot_init_pos[0]][bot_init_pos[1]]
goal_state = grid[button_init_pos[0]][button_init_pos[1]]
# result, final_state, prev = breadth_first_search(
#     bot_state, goal_state, lambda b: b.open == False or b.has_fire if b is not None else True
# )
# print_board_2(show_path=True)
# bot_state = grid


def neighbors_have_fire(cell):
    non_none_neighbors = [
        neighbor for neighbor in cell.get_neighbors() if neighbor is not None]
    return any([neighbor.has_fire for neighbor in non_none_neighbors])
    ...


# disable for performance
# print_board_2([], show_path=True)

step = 0
q = 0.1
# everything except bot 1
while bot_state != goal_state:
    # BFS
    # result, final_state, prev = breadth_first_search(
    #     bot_state, goal_state, lambda b: b.open == False or b.has_fire
    #     or neighbors_have_fire(b) if b is not None else True
    # )
    # DFS
    result, final_state, prev = depth_first_search(
        bot_state, goal_state, lambda b: b.open == False or b.has_fire or neighbors_have_fire(b) if b is not None else True
    )
    # check to see if path exists while ignoring 1 space requirement. comment this out for non-bot-3
    if result == "Failed":
        result, final_state, prev = depth_first_search(
            bot_state, goal_state, lambda b: b.open == False or b.has_fire if b is not None else True)
    # if result == "Failed":
    #     result, final_state, prev = breadth_first_search(
    #         bot_state, goal_state, lambda b: b.open == False or b.has_fire if b is not None else True)
    path = backtrack(prev, final_state)
    if path == []:
        # print("FAILED")
        # f.write(f"bot 2, {q}, {result}")
        break
    bot_state = path[1]
    bot_state.has_bot = True
    path[0].has_bot = False
    # if step > 0:
    #     spread_fire(q)
    spread_fire(q)
    # disable for performance
    # print_board_2(path, show_path=True)

# bot1
# result, final_state, prev = breadth_first_search(
#     bot_state, goal_state, lambda b: b.open == False or b.has_fire
#     or neighbors_have_fire(b) if b is not None else True
# )
# #DFS
# # result, final_state, prev = depth_first_search(
# #     bot_state, goal_state, lambda b: b.open == False or b.has_fire if b is not None else True
# # )
# path = backtrack(prev, final_state)
# while bot_state != goal_state:
#     # BFS
#     if bot_state.has_fire or path is None:
#         # print("FAILED")
#         # f.write(f"bot 2, {q}, {result}")
#         result = "Failed"
#         break
#     bot_state = path[step]
#     bot_state.has_bot = True
#     # if step > 0:
#     #     spread_fire(q)
#     spread_fire(q)
#     # disable for performance
#     print_board_2(path, show_path=True)

#     step += 1
#     path[step-1].has_bot = False
print(result)
f.write(f"bot4,{q},{result}\n")
# if __name__ == '__main__':
f.close()
# print()
