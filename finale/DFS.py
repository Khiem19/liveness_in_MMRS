import networkx as nx
from itertools import product

def generate_next_states(robot_pos, path):
    next_positions = []
    if robot_pos < len(path):
        next_positions.append(robot_pos + 1) 
    if robot_pos == len(path):
        next_positions.append(0)  # Reset to start position after finishing
    return next_positions

def is_valid_state(state, paths):
    position_dict = {}
    for robot_index, robot_pos in enumerate(state):
        if robot_pos == 0:
            continue
        position_in_path = paths[robot_index][robot_pos - 1]
        if position_in_path in position_dict:
            return False, f"Resource conflict at {position_in_path} between robots"
        position_dict[position_in_path] = robot_index
    return True, None

def generate_concurrent_states(current_state, paths):
    state_options = [[current_state[i]] for i in range(len(paths))]  # Start with the current state
    for i, robot_pos in enumerate(current_state):
        next_positions = generate_next_states(robot_pos, paths[i])
        for pos in next_positions:
            new_state = list(current_state)
            new_state[i] = pos
            if is_valid_state(tuple(new_state), paths)[0]:
                state_options[i].append(pos)

    all_combinations = product(*state_options)
    valid_states = []
    for combo in all_combinations:
        new_state = tuple(combo)
        if is_valid_state(new_state, paths)[0]:
            valid_states.append(new_state)
    return valid_states

def dfs_complete_cycle(initial_state, paths, G):
    stack = [(initial_state, None)]
    visited = set()
    state_details = {}
    
    while stack:
        state, transition = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        G.add_node(state)
        valid, _ = is_valid_state(state, paths)
        state_details[state] = {'valid': valid, 'transition': transition}

        next_states = generate_concurrent_states(state, paths)
        for next_state in next_states:
            for i in range(len(state)):
                if state[i] != next_state[i]:
                    transition = (state, f"t({i+1},{next_state[i]})")
            G.add_edge(state, next_state)
            stack.append((next_state, transition))
    
    return state_details

def ensure_liveness_and_deadlocks(initial_state, paths, G, state_details):
    # Check for paths from each state to the initial state to determine liveness
    path_dict = dict(nx.all_pairs_shortest_path(G))
    live_states = []
    issue_states = []

    initial_state_tuple = tuple([0] * len(paths))

    for state in path_dict:
        is_live = any(initial_state_tuple in path_dict[state] for target in path_dict[state])
        if is_live:
            live_states.append(state)
        else:
            issue_states.append(state)

    combined_states = live_states + issue_states

    # Write combined states to the file in the order they were found
    with open('result/dfs.txt', 'w') as combined_file:
        combined_file.write("Reach to Deadlock States:\n")
        combined_file.write("----------------------------------------------------------------------\n")
        combined_file.write("| No. | State       | Previous State | Transition           |\n")
        combined_file.write("----------------------------------------------------------------------\n")
        for i, state in enumerate(combined_states, start=1):
            transition_info = state_details.get(state, {}).get('transition')
            if transition_info:
                previous_state, transition = transition_info
                combined_file.write(f"| {i:<3} | {state} | {previous_state} | {transition:<20} |\n")
            else:
                combined_file.write(f"| {i:<3} | {state} | Initial state  | -                  |\n")
        combined_file.write("----------------------------------------------------------------------\n")

    total_deadlock_states = len(issue_states)
    return live_states, issue_states, total_deadlock_states

# Example usage
paths = [
    [76, 66, 56, 46, 36, 26, 25, 24, 23, 22, 21], 
    [2, 12, 22, 32, 42, 52, 53, 54, 55, 56, 57, 58],
    [49, 48, 47, 46, 45, 44, 43, 42, 52, 62, 72],
    [17, 16, 15, 25, 35, 45, 55, 65],
    [14, 24, 34, 44, 54, 64, 74],
    [87, 86, 85, 84, 83, 82, 81, 71, 61],
    [91, 92, 93, 94, 95, 96, 97, 98, 99]
]


initial_state = tuple([0] * len(paths))  # Start at position 0 for all robots
G = nx.DiGraph()
state_details = dfs_complete_cycle(initial_state, paths, G)
live_states, issue_states, total_deadlock_states = ensure_liveness_and_deadlocks(initial_state, paths, G, state_details)
