import random

import pygame

from MazeGenerator import Maze, Cell
import json
from BinaryHeap import BinaryHeap


class Node:
    def __init__(self, x, y, f_score, g_score, h_score):
        self.x = x
        self.y = y
        self.parent = None
        self.f_score = f_score
        self.g_score = g_score
        self.h_score = h_score

    def __lt__(self, node_to_compare):
        return self.f_score < node_to_compare.f_score

    def __gt__(self, node_to_compare):
        return self.f_score > node_to_compare.f_score


class AStar:
    # This class will run forward A* search, reverse A* search, and Adaptive A* search
    # It will run these searches by loading in the x and y coordinates from the maze file
    # It will also load in the walls from the maze file
    # It will then construct the nodes for that maze
    # The A* searches will run on these nodes

    # Create 50 maze objects in a list

    def __init__(self, maze_file):
        self.maze = Maze(1011, 1011, 10, 101, 101)
        self.maze_file = maze_file
        self.maze_cells = []
        self.nodes = []
        self.open_list = BinaryHeap()
        self.closed_list = []
        self.start_node = None
        self.goal_node = None

        with open(self.maze_file, 'r') as maze_file:
            maze_file_lines = [line.replace("\n", "").split(",", 2) for line in maze_file.readlines()]

            for line in maze_file_lines:
                cell = Cell(int(line[0]), int(line[1]), 10, self.maze.screen, json.loads(line[2].replace("'", '"').strip()), True)
                self.maze_cells.append(cell)
                self.nodes.append(Node(int(line[0]), int(line[1]), None, None, None))

                if int(line[0]) == 0 and int(line[1]) == 0:
                    self.start_node = self.nodes[-1]
                elif int(line[0]) == 100 and int(line[1]) == 100:
                    self.goal_node = self.nodes[-1]

    def heuristic(self, current_node):
        return abs(current_node.x - self.goal_node.x) + abs(current_node.y - self.goal_node.y)

    def update_node(self, current_node, neighbor_node):
        neighbor_node.g_score = current_node.g_score + 1
        neighbor_node.h_score = self.heuristic(neighbor_node)
        neighbor_node.f_score = neighbor_node.g_score + neighbor_node.h_score

        if neighbor_node not in self.closed_list:
            neighbor_node.parent = current_node
            self.open_list.insert(neighbor_node)

    def get_neighbors(self, current_node):
        current_cell = self.maze_cells[current_node.x + current_node.y * 101]

        if current_cell.walls["NORTH"] is False:
            self.update_node(current_node, self.nodes[current_node.x + (current_node.y - 1) * 101])
        if current_cell.walls["SOUTH"] is False:
            self.update_node(current_node, self.nodes[current_node.x + (current_node.y + 1) * 101])
        if current_cell.walls["EAST"] is False:
            self.update_node(current_node, self.nodes[(current_node.x + 1) + current_node.y * 101])
        if current_cell.walls["WEST"] is False:
            self.update_node(current_node, self.nodes[(current_node.x - 1) + current_node.y * 101])

    def forward_a_star(self):
        self.start_node.g_score = 0
        self.start_node.h_score = self.heuristic(self.start_node)
        self.start_node.f_score = self.start_node.g_score + self.start_node.h_score
        self.open_list.insert(self.start_node)

        while self.open_list.is_empty() is False:
            current_node = self.open_list.pop()
            self.closed_list.append(current_node)

            if current_node.x == self.goal_node.x and current_node.y == self.goal_node.y:
                return self.get_shortest_path(current_node)

            self.get_neighbors(current_node)

        return self.closed_list

    def get_shortest_path(self, current_node):
        shortest_path = [current_node]

        while current_node.parent is not None:
            shortest_path.append(current_node.parent)
            current_node = current_node.parent

        return shortest_path

    def reverse_a_star(self): # THIS IS NOT CORRECT BY THE WAY
        self.goal_node.g_score = 0
        self.goal_node.h_score = self.heuristic(self.goal_node)
        self.goal_node.f_score = self.goal_node.g_score + self.goal_node.h_score
        self.open_list.insert(self.goal_node)

        while self.open_list.is_empty() is False:
            current_node = self.open_list.pop()
            self.closed_list.append(current_node)

            if current_node.x == self.start_node.x and current_node.y == self.start_node.y:
                return self.get_shortest_path(current_node)

            self.get_neighbors(current_node)

        return self.closed_list

if __name__ == "__main__":
    a_star = AStar("../mazes/maze0.maze")
    path = a_star.forward_a_star()
    [cell.draw() for cell in a_star.maze_cells]

    for node in path:
        # Draw a blue circle at the node
        pygame.draw.circle(a_star.maze.screen, (0, 0, 255), (node.x * 10 + 5, node.y * 10 + 5), 2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.image.save(a_star.maze.screen, "../A-Star.png")
        pygame.display.flip()



