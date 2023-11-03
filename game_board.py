# type: ignore
import pygame
import sys
import csv
from transform_solution import apply_solution
import rushHourPuzzle as rh
from button import Button


def drawGrid(screen, w, h):
    # Grid parameters
    grid_width = w  # Number of columns
    grid_height = h  # Number of rows
    cell_size = 100  # Size of each grid cell in pixels
    grid_color = (0, 0, 0)  # Color of the grid lines (white in RGB)

    # Calculate the width and height of the grid in pixels
    grid_pixel_width = grid_width * cell_size
    grid_pixel_height = grid_height * cell_size

    # Calculate the position of the grid's top-left corner to center it on the screen
    grid_x = ((w * 100 + 100) - grid_pixel_width) // 2
    grid_y = ((h * 100 + 100) - grid_pixel_height) // 2

    for row in range(grid_height):
        num_pos = grid_x + row * cell_size + 50
        pygame.font.init()
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(row + 1), False, (0, 0, 0))
        screen.blit(text, (num_pos, grid_y - 20))

    for col in range(grid_width):
        num_pos = grid_y + col * cell_size + 50
        pygame.font.init()
        font = pygame.font.SysFont(None, 20)
        text = font.render(str(col + 1), False, (0, 0, 0))
        screen.blit(text, (grid_x - 20, num_pos))

    for row in range(grid_height):
        for col in range(grid_width):
            x = grid_x + col * cell_size
            y = grid_y + row * cell_size
            pygame.draw.rect(
                screen, grid_color, (x, y, cell_size, cell_size), 1
            )  # Draw grid cell

    # draw the outer border
    pygame.draw.rect(
        screen,
        grid_color,
        (grid_x, grid_y, grid_pixel_width, grid_pixel_height),
        4,
    )

    # draw the exit rectangle on (6,3)
    pygame.draw.polygon(
        screen,
        (0, 0, 0),
        [
            (grid_x + 600, grid_y + 230),
            (grid_x + 600, grid_y + 270),
            (grid_x + 620, grid_y + 250),
        ],
        0,
    )


def transform_list(input_list):
    result = []
    counts = {}
    rows = len(input_list)
    cols = len(input_list[0])

    for row in range(rows):
        for col in range(cols):
            element = input_list[row][col]

            if element != " ":
                if element in counts:
                    counts[element] += 1
                else:
                    counts[element] = 1

                if element in result:
                    index = result.index(element)
                    result[index].append(str(col))
                else:
                    result.append([element, str(col)])

    for i in range(len(result)):
        element = result[i][0]
        result[i].append(str(counts[element]))
        if i % 2 == 0:
            result[i].append("H")
            result[i].append("2")
        else:
            result[i].append("V")
            result[i].append("2")

    return result


def loadPuzzle(puzzle_file):
    board = []
    w = 0
    h = 0
    with open(puzzle_file) as file:
        reader = csv.reader(file)
        w, h = [int(i) for i in next(reader)]
        for row in reader:
            board.append(row)
    state = rh.RushHourPuzzle(board, w, h)
    solution, steps = state.a_star(state)
    states = apply_solution(board, solution)
    return w, h, states, steps


# Function to draw vehicles on the grid
def drawVehicles(screen, w, h, state):
    for row in state:
        object_type = row[0]
        x = int(row[1]) * 100 + ((w * 100 + 100) - (w * 100)) // 2
        y = int(row[2]) * 100 + ((h * 100 + 100) - (h * 100)) // 2

        if object_type != "#":
            if row[3] == "H":
                width = int(row[4]) * 100 - 14
                height = 86
            else:
                width = 86
                height = int(row[4]) * 100 - 14
        else:
            width = 86
            height = 86

        if object_type == "#":
            color = (0, 0, 0)
        elif object_type == "X":
            color = (255, 0, 0)
        else:
            color = (51, 136, 153)

        pygame.draw.rect(screen, color, (x + 7, y + 7, width, height), 0, 10)


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Load the puzzle
    w, h, states, steps = loadPuzzle("./levels/1.csv")

    screen = pygame.display.set_mode((int(w) * 100 + 100, int(h) * 100 + 200))
    pygame.display.set_caption("Rush Hour Puzzle")

    # load images
    prev_img = pygame.image.load("./prev_btn.jpg").convert_alpha()
    next_img = pygame.image.load("./start_btn.jpg").convert_alpha()
    congrats_img = pygame.image.load("./congrats.jpg").convert_alpha()
    congrats = congrats_img.get_rect(left=0, top=0)

    # create button instances
    prev_btn = Button(150, 700, prev_img, 0.5)
    next_btn = Button(400, 700, next_img, 0.5)

    # Create a variable to track the current state index
    state_index = 0

    # Draw the current state
    drawVehicles(screen, w, h, states[state_index])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((220, 220, 220))
        drawGrid(screen, w, h)

        # Handle button events
        if prev_btn.draw(screen):
            # If the previous button is clicked, go back to the previous state
            state_index -= 1
            if state_index < 0:
                state_index = len(states) - 1

        elif next_btn.draw(screen):
            # If the next button is clicked, go to the next state
            state_index += 1
            if state_index >= len(states):
                state_index = 0

        # Make sure the state index is within bounds
        state_index = state_index % len(states)

        # Draw the updated state
        drawVehicles(screen, w, h, states[state_index])

        pygame.display.update()
        clock.tick(60)

    sys.exit()


if __name__ == "__main__":
    main()
