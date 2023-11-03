def apply_solution(initial_state, solution):
    # Create a list to hold all the states
    states = []

    # Add the initial state to the list
    states.append(initial_state)

    # Apply each action in the solution to the current state
    for action in solution:
        if action == "":
            continue

        # Split the action into the vehicle ID and the direction
        vehicle_id, direction = action.split(":")

        # Find the vehicle in the current state
        for vehicle in states[-1]:
            if vehicle[0] == vehicle_id:
                # Create a copy of the current state and apply the action
                new_state = [list(vehicle) for vehicle in states[-1]]
                for new_vehicle in new_state:
                    if new_vehicle[0] == vehicle_id:
                        if direction == "L":
                            new_vehicle[1] = str(int(new_vehicle[1]) - 1)
                        elif direction == "R":
                            new_vehicle[1] = str(int(new_vehicle[1]) + 1)
                        elif direction == "U":
                            new_vehicle[2] = str(int(new_vehicle[2]) - 1)
                        elif direction == "D":
                            new_vehicle[2] = str(int(new_vehicle[2]) + 1)

                # Add the new state to the list
                states.append(new_state)
                break

    return states
