import heapq

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)
GOAL_POS = {n: (i // 3, i % 3) for i, n in enumerate(GOAL_STATE)}

def manhattan(state):
    """Heuristic: sum of Manhattan distances for each tile to goal"""
    dist = 0
    for i, val in enumerate(state):
        if val == 0:
            continue
        curr_row, curr_col = divmod(i, 3)
        goal_row, goal_col = GOAL_POS[val]
        dist += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return dist

def get_neighbors(state):
    neighbors = []
    blank_index = state.index(0)
    row, col = divmod(blank_index, 3)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dr, dc in moves:
        r, c = row+dr, col+dc
        if 0 <= r <3 and 0 <= c <3:
            new_index = r*3 + c
            new_state = list(state)
            # swap blank and tile
            new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
            neighbors.append(tuple(new_state))
    return neighbors

def solve_puzzle(start):
    """A* search to solve the puzzle."""
    open_set = []
    heapq.heappush(open_set, (manhattan(start), 0, start, []))
    closed_set = set()

    while open_set:
        est_total_cost, cost_so_far, current, path = heapq.heappop(open_set)
        if current == GOAL_STATE:
            return path + [current]
        if current in closed_set:
            continue
        closed_set.add(current)

        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue
            new_cost = cost_so_far + 1
            est_cost = new_cost + manhattan(neighbor)
            heapq.heappush(open_set, (est_cost, new_cost, neighbor, path + [current]))

    return []
