import json
import random
import sys
import time
import pygame


class Maze:
    FRAME_RATE = 10000

    def __init__(self, width, height, cell_size, rows, cols, show_window=True):
        self.width = width  # Width of the screen
        self.height = height  # Height of the screen
        self.cell_size = cell_size  # Size of each cell
        self.cols, self.rows = rows, cols  # Number of rows and columns (rows * cols = total cells)

        if show_window:
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            self.screen = pygame.Surface((self.width, self.height), pygame.HIDDEN)

        self.clock = pygame.time.Clock()
        self.screen.fill((169, 169, 169))  # gray

    def initialize_gui(self, iteration_number):
        pygame.init()
        pygame.display.set_caption(f"Maze Generator - Maze # {iteration_number}")

        grid_cells = [Cell(x, y, self.cell_size, self.screen) for y in range(self.cols) for x in range(self.rows)]

        current_cell = grid_cells[0]
        stack = []

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            [cell.draw() for cell in grid_cells]
            current_cell.visited = True
            # current_cell.paint_current_cell() # Uncomment this line to see the current cell being visited

            next_cell = current_cell.check_neighbors(self.rows, self.cols, grid_cells)

            if next_cell is not False:
                next_cell.visited = True
                stack.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

            if not stack:
                for cell in grid_cells:
                    with open(f'../mazes/maze{iteration_number}.maze', 'a') as f:
                        f.write(f"{cell.x}, {cell.y}, {json.dumps(cell.walls)}\n")
                        f.close()
                break

            pygame.display.flip()
            self.clock.tick(self.FRAME_RATE)

    @staticmethod
    def remove_walls(current_cell, next_cell):
        x = current_cell.x - next_cell.x
        y = current_cell.y - next_cell.y

        if x == 1:
            current_cell.walls['WEST'] = False # False indicates that there is no wall here
            next_cell.walls['EAST'] = False
        elif x == -1:
            current_cell.walls['EAST'] = False
            next_cell.walls['WEST'] = False

        if y == 1:
            current_cell.walls['NORTH'] = False
            next_cell.walls['SOUTH'] = False
        elif y == -1:
            current_cell.walls['SOUTH'] = False
            next_cell.walls['NORTH'] = False


class Cell:
    def __init__(self, x, y, cell_size, screen, walls=None, visited=False):
        self.x = x
        self.y = y
        self.cell_size = cell_size

        if walls is None:
            self.walls = {'NORTH': True, 'EAST': True, 'SOUTH': True, 'WEST': True}
        else:
            self.walls = walls

        self.visited = visited
        self.screen = screen

    def paint_current_cell(self):
        x, y = self.x * self.cell_size, self.y * self.cell_size
        pygame.draw.rect(self.screen, (0, 255, 0), (x + 10, y + 10, self.cell_size - 20, self.cell_size - 20))  # x and y are the top left corner of the rectangle and the last two are the width and height

    def draw(self):
        x, y = self.x * self.cell_size, self.y * self.cell_size

        if self.visited:
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size))

        if self.walls['NORTH']:  # Draw the "walls" of the cell
            pygame.draw.line(self.screen, (255, 255, 255), (x, y), (x + self.cell_size, y))
        if self.walls['EAST']:
            pygame.draw.line(self.screen, (255, 255, 255), (x + self.cell_size, y),
                             (x + self.cell_size, y + self.cell_size))
        if self.walls['SOUTH']:
            pygame.draw.line(self.screen, (255, 255, 255), (x + self.cell_size, y + self.cell_size),
                             (x, y + self.cell_size))
        if self.walls['WEST']:
            pygame.draw.line(self.screen, (255, 255, 255), (x, y + self.cell_size), (x, y))

    def check_cell(self, x, y, cols, rows, grid_cells):
        if x < 0 or y < 0 or x > cols - 1 or y > rows - 1:
            return False

        return grid_cells[x + y * cols]

    def check_neighbors(self, cols, rows, grid_cells):
        neighbors = []

        north = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        south = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        east = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        west = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)

        if north and not north.visited:
            neighbors.append(north)
        if south and not south.visited:
            neighbors.append(south)
        if east and not east.visited:
            neighbors.append(east)
        if west and not west.visited:
            neighbors.append(west)

        if neighbors:
            return random.choice(neighbors)
        else:
            return False


if __name__ == "__main__":
    maze_number = int(sys.argv[1]) # The maze number that is being generated.
    print(f"Generating maze {maze_number + 1} of 50")
    maze = Maze(1011, 1011, 10, 101, 101)  # Create the maze object; the first two arguments are the width and height of the screen, the third is the size of the cells, the fourth is the number of rows and the fifth is the number of columns
    start = time.time()
    maze.initialize_gui(maze_number) # Initialize the GUI and generate the maze
    end = time.time()
    pygame.image.save(maze.screen, f"../mazes/maze{maze_number}.png") # Save the maze as a png file
    print(f"Time taken to generate maze {maze_number + 1} of 50: {end - start} seconds")
    print("====================================================================================================================================\n")




