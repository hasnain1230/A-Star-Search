import sys

import pygame.display

from MazeGenerator import Maze
from MazeGenerator import Cell
import json


if __name__ == '__main__':
    maze = Maze(1011, 1011, 10, 101, 101)
    cells = []
    with open(sys.argv[1], 'r') as maze_file:
        maze_file_lines = [line.replace("\n", "").split(",", 2) for line in maze_file.readlines()]

        for line in maze_file_lines:
            cell = Cell(int(line[0]), int(line[1]), 10, maze.screen, json.loads(line[2].replace("'", '"').strip()), True)
            cells.append(cell)

    [cell.draw() for cell in cells]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # pygame.image.save(maze.screen, "maze0.png")
        pygame.display.flip()
