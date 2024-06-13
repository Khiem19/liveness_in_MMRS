import numpy as np

def display_state(state_num, finish_statuses, positions, paths, file_path):
    with open(file_path, 'a') as f:
        f.write(f"\nNo. {state_num}:\n")
        f.write("\nFinish Status:\n")
        for i, finish in enumerate(finish_statuses):
            f.write(f"Process {i+1}: Finish = {finish}\n")
        f.write("\nPositions of Robots in Their Paths:\n")
        for i, pos in enumerate(positions):
            current_position = paths[i][pos] if pos < len(paths[i]) else "Completed"
            f.write(f"Process {i+1}: Position in Path = {current_position} \n")
        f.write("\n")
        f.write("State: ")
        for i, pos in enumerate(positions):
            if pos < len(paths[i]):
                f.write(f"({pos+1}) ")
        f.write("\n" + "="*30+ "\n")

def find_next_private_cell(current_index, paths, positions):
    path = paths[current_index]
    current_position = positions[current_index]
    
    furthest_private_cell = current_position  # Initialize with current position
    shared_found = False
    
    for idx in range(current_position + 1, len(path)):
        current_cell = path[idx]
        if any(current_cell in paths[other_idx] for other_idx in range(len(paths)) if other_idx != current_index):
            shared_found = True
        elif shared_found:
            if all(current_cell != paths[other_idx][positions[other_idx]] for other_idx in range(len(paths)) if other_idx != current_index):
                return idx
        else:
            furthest_private_cell = idx  # Update furthest private cell before the first shared cell
    
    return furthest_private_cell

def find_next_before_shared_cell(current_index, paths, positions):
    path = paths[current_index]
    current_position = positions[current_index]

    for idx in range(current_position + 1, len(path)):
        current_cell = path[idx]
        if any(current_cell in paths[other_idx] for other_idx in range(len(paths)) if other_idx != current_index):
            return idx - 1  # Return the cell before the first shared cell

    return len(path) - 1  # Return the end of the path if no shared cells found

def calculate_needs(positions, paths, round_robin_counter):
    needs = []
    for i, pos in enumerate(positions):
        if round_robin_counter[i] % 2 == 0:
            next_position = find_next_private_cell(i, paths, positions)
        else:
            next_position = find_next_before_shared_cell(i, paths, positions)
        needs.append(next_position - pos)
    return np.array(needs)

def is_safe_state(available_resources, max_resources, allocated_resources, needs, positions, paths, output_file, round_robin_counter):
    work = available_resources
    finish_statuses = [False] * len(paths)
    state_num = 1  # Start state numbering from 1
    total_processes = len(paths)
    current_process = 0  # Start with the first process

    while not all(finish_statuses):
        made_progress = False

        if needs[current_process] <= work and not finish_statuses[current_process]:
            if round_robin_counter[current_process] % 2 == 0:
                next_position = find_next_before_shared_cell(current_process, paths, positions)
            else:
                next_position = find_next_private_cell(current_process, paths, positions)

            if positions[current_process] != next_position:  # If progress can be made
                allocated_resources[current_process] += next_position - positions[current_process]
                work -= next_position - positions[current_process]
                positions[current_process] = next_position

                if positions[current_process] >= len(paths[current_process]) - 1:
                    finish_statuses[current_process] = True
                    work += allocated_resources[current_process]  # Release resources
                    allocated_resources[current_process] = 0

                # Recalculate needs for the next iteration
                round_robin_counter[current_process] += 1
                needs = calculate_needs(positions, paths, round_robin_counter)
                made_progress = True

                # Display the state only when progress is made
                display_state(state_num, finish_statuses, positions, paths, output_file)
                state_num += 1

        # Move to the next process in round-robin fashion
        current_process = (current_process + 1) % total_processes

        if not made_progress and current_process == 0:  # No progress means potential deadlock
            display_state(state_num, finish_statuses, positions, paths, output_file)
            return False

    return True

def bankers_algorithm(paths, max_resources, output_file):
    num_processes = len(paths)
    max_resources_array = np.array([len(path) for path in paths], dtype=int)
    positions = [0] * num_processes
    available_resources = max_resources
    round_robin_counter = [0] * num_processes
    needs = calculate_needs(positions, paths, round_robin_counter)
    allocated_resources = np.zeros(num_processes, dtype=int)
    is_safe_state(available_resources, max_resources_array, allocated_resources, needs, positions, paths, output_file, round_robin_counter)

# Example Usage
paths = [
    [11, 12, 13, 14, 24, 34, 44, 54, 64, 65, 66, 67, 68], 
    [86, 76, 66, 65, 64, 63, 62, 61],
]
max_resources = 100
output_file = 'result/banker_output.txt'
open(output_file, 'w').close()  # Clear file before writing
bankers_algorithm(paths, max_resources, output_file)
