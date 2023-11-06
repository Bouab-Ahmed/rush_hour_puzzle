from copy import deepcopy
from rush_node import Node


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append(node)

    def remove(self):
        min = 0
        for i in range(len(self.queue)):
            if self.queue[i].f < self.queue[min].f:
                min = i
        node = self.queue[min]
        del self.queue[min]
        return node

    def empty(self):
        return len(self.queue) == 0

    def contains_state(self, state):
        return any(node.state == state for node in self.queue)


class RushHourPuzzle:
    def __init__(self, board, w, h):
        # Initialize the Rush Hour puzzle Board
        self.setVehicles(board, w, h)
        self.setBoard()

    def __eq__(self, other):
        if isinstance(other, RushHourPuzzle):
            return self.board == other.board
        return False

    def setVehicles(self, board, w, h):
        self.board_width, self.board_height = int(w), int(h)
        self.vehicles = []
        self.walls = []
        for line in board:
            if line[0] == "#":
                self.walls.append((int(line[1]), int(line[2])))
            else:
                id, x, y, orientation, length = line
                vehicle = {
                    "id": id,
                    "x": int(x),
                    "y": int(y),
                    "orientation": orientation,
                    "length": int(length),
                }
                self.vehicles.append(vehicle)

    def setBoard(self):
        self.board = [
            [" " for _ in range(self.board_width)] for _ in range(self.board_height)
        ]
        for x, y in self.walls:
            self.board[y][x] = "#"
        for vehicle in self.vehicles:
            x, y = vehicle["x"], vehicle["y"]
            if vehicle["orientation"] == "H":
                for i in range(vehicle["length"]):
                    self.board[y][x + i] = vehicle["id"]
            else:
                for i in range(vehicle["length"]):
                    self.board[y + i][x] = vehicle["id"]

    # check if the red car is at the goal position
    def isGoal(self):
        for vehicle in self.vehicles:
            if vehicle["id"] == "X" and vehicle["x"] == self.board_width - 2:
                return True
        return False

    # Generate the successors
    def successorFunction(self):
        succs = list()
        for index, vehicle in enumerate(self.vehicles):
            x_position = vehicle["x"]
            y_position = vehicle["y"]

            # check if the vehicle is oriented horizontal
            if vehicle["orientation"] == "H":
                # move left if it's not on the edge of the board and it's not blocked by another vehicle
                if x_position > 0 and self.board[y_position][x_position - 1] == " ":
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["x"] = x_position - 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:L".format(vehicle["id"]), successor))

                # move right if it's not on the edge of the board and it's not blocked by another vehicle
                if (
                    x_position + vehicle["length"] < self.board_width
                    and self.board[y_position][x_position + vehicle["length"]] == " "
                ):
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["x"] = x_position + 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:R".format(vehicle["id"]), successor))

            # check if the vehicle is oriented vertical
            else:
                # move up if it's not on the edge of the board and it's not blocked by another vehicle
                if y_position > 0 and self.board[y_position - 1][x_position] == " ":
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["y"] = y_position - 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:U".format(vehicle["id"]), successor))

                # move down if it's not on the edge of the board and it's not blocked by another vehicle
                if (
                    y_position + vehicle["length"] < self.board_height
                    and self.board[y_position + vehicle["length"]][x_position] == " "
                ):
                    successor = deepcopy(self)
                    successor.vehicles = deepcopy(self.vehicles)
                    # update the vehicle's position
                    successor.vehicles[index]["y"] = y_position + 1
                    # update the board
                    successor.setBoard()
                    succs.append(("{}:D".format(vehicle["id"]), successor))
        return succs

        """ First heuristic: Distance from target vehicle to the exit """

    def heuristic1(state):
        for vehicle in state.vehicles:
            if vehicle["id"] == "X":
                return state.board_width - 2 - vehicle["x"]

    """ Second heuristic: number of vehicles that block the way to the exit """

    def heuristic2(state):
        for vehicle in state.vehicles:
            if vehicle["id"] == "X":
                unique_vehicles = set(state.board[vehicle["y"]][vehicle["x"] :])
                # print(f"unique vehicles: {unique_vehicles}")
                # print()
                if " " in unique_vehicles:
                    return state.heuristic1() + len(unique_vehicles) - 2
                return state.heuristic1() + len(unique_vehicles) - 1

    @staticmethod
    def a_star(start, depth_limit=2):
        # Create the initial node
        initial_node = Node(start, None, "", 1, 0)
        initial_node.g = initial_node.h = initial_node.f = 0

        # Check if the start element is the goal
        if initial_node.state.isGoal():
            return initial_node, 0

        # Create the OPEN FIFO queue and the CLOSED list
        open = PriorityQueue()
        closed = []

        open.add(initial_node)
        step = 0
        running = True
        while not open.empty() and running:
            print(f"*** Step {step} ***")
            if open.empty():
                print("No solution found.")
                return None, step
            # Get the first element of the OPEN queue
            current = open.remove()

            # Check if it is the goal
            if current.state.isGoal():
                print("goal found")
                print("solution: ", current.getSolution())
                running = False
                return current.getSolution(), step

            if current.depth >= depth_limit:
                continue

            # Put the current node in the CLOSED list
            closed.append(current.state)
            # Generate the successors of the current node
            for action, successor in current.state.successorFunction():
                # Create the successor node
                h = RushHourPuzzle.heuristic1(successor)
                bc = RushHourPuzzle.heuristic2(successor)
                successor_node = Node(successor, current, action, 1, h + bc)

                # Check if the successor is in the CLOSED list and not in the OPEN list
                if (
                    not open.contains_state(successor_node.state)
                    and successor_node.state not in closed
                ):
                    open.add(successor_node)
                # Check if the successor is in the OPEN list and if it has a lower f value
                elif open.contains_state(successor_node.state):
                    for node in open.queue:
                        if node.state == successor_node.state:
                            if node.f > successor_node.f:
                                open.queue.remove(node)
                                open.add(successor_node)
                                break
            step += 1


# initial_state = RushHourPuzzle("./levels/1.csv")

# solution, steps = RushHourPuzzle.a_star(initial_state)

# print(f"Solution: {solution}")
