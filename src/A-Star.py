import os
import sys
import time

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
        self.maze = Maze(1011, 1011, 10, 101, 101, False)
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
                cell = Cell(int(line[0]), int(line[1]), 10, self.maze.screen,
                            json.loads(line[2].replace("'", '"').strip()), True)
                self.maze_cells.append(cell)
                self.nodes.append(Node(int(line[0]), int(line[1]), None, None, None))

                if int(line[0]) == 0 and int(line[1]) == 0:
                    self.start_node = self.nodes[-1]
                elif int(line[0]) == 100 and int(line[1]) == 100:
                    self.goal_node = self.nodes[-1]

    @staticmethod
    def heuristic(current_node, goal_node):
        return abs(current_node.x - goal_node.x) + abs(current_node.y - goal_node.y)

    def update_node(self, current_node, neighbor_node, adaptive):
        if not adaptive:
            neighbor_node.g_score = current_node.g_score + 1
            neighbor_node.h_score = self.heuristic(neighbor_node, self.goal_node)
            neighbor_node.f_score = neighbor_node.g_score + neighbor_node.h_score

        if neighbor_node not in self.closed_list:
            neighbor_node.parent = current_node
            return neighbor_node
        return None

    def get_neighbors(self, current_node, adaptive=False, g_bigger=True):
        current_cell = self.maze_cells[current_node.x + current_node.y * 101]
        neighbor_nodes = []

        if current_cell.walls["NORTH"] is False and self.nodes[
            current_node.x + (current_node.y - 1) * 101] not in self.closed_list:
            neighbor_node = self.update_node(current_node, self.nodes[current_node.x + (current_node.y - 1) * 101],
                                             adaptive)
            if neighbor_node is not None:
                neighbor_nodes.append(neighbor_node)
        if current_cell.walls["SOUTH"] is False and self.nodes[
            current_node.x + (current_node.y + 1) * 101] not in self.closed_list:
            neighbor_node = self.update_node(current_node, self.nodes[current_node.x + (current_node.y + 1) * 101],
                                             adaptive)
            if neighbor_node is not None:
                neighbor_nodes.append(neighbor_node)
        if current_cell.walls["EAST"] is False and self.nodes[
            (current_node.x + 1) + current_node.y * 101] not in self.closed_list:
            neighbor_node = self.update_node(current_node, self.nodes[(current_node.x + 1) + current_node.y * 101],
                                             adaptive)
            if neighbor_node is not None:
                neighbor_nodes.append(neighbor_node)
        if current_cell.walls["WEST"] is False and self.nodes[
            (current_node.x - 1) + current_node.y * 101] not in self.closed_list:
            neighbor_node = self.update_node(current_node, self.nodes[(current_node.x - 1) + current_node.y * 101],
                                             adaptive)
            if neighbor_node is not None:
                neighbor_nodes.append(neighbor_node)

        # neighbor_nodes = [node for node in neighbor_nodes if node.g_score is not None]

        if adaptive:
            for node in neighbor_nodes:
                if node.g_score is None:
                    node.g_score = current_node.g_score + 1
                    node.h_score = self.adaptive_heuristic(node, self.goal_node)
                    node.f_score = node.g_score + node.h_score

        if g_bigger:
            neighbor_nodes.sort(key=lambda node: (node.f_score, -node.g_score))  # Sort by f_score, then by the largest g_score (Some clever code here, but it's short and effective)
        else:
            neighbor_nodes.sort(key=lambda node: (node.f_score, node.g_score))  # Sort by f_score, then by the largest g_score (Some clever code here, but it's short and effective)

        for neighbor_node in neighbor_nodes:
            # The one inserted first gets popped first
            self.open_list.insert(neighbor_node)

    def forward_a_star(self, g_bigger):
        self.start_node.g_score = 0
        self.start_node.h_score = self.heuristic(self.start_node, self.goal_node)
        self.start_node.f_score = self.start_node.g_score + self.start_node.h_score
        self.open_list.insert(self.start_node)

        while self.open_list.is_empty() is False:
            current_node = self.open_list.pop()
            self.closed_list.append(current_node)

            if current_node.x == self.goal_node.x and current_node.y == self.goal_node.y:
                return self.get_shortest_path(current_node)

            self.get_neighbors(current_node, g_bigger=g_bigger)

        return None

    def get_shortest_path(self, current_node):
        shortest_path = [current_node]

        while current_node.parent is not None:
            shortest_path.append(current_node.parent)
            current_node = current_node.parent

        return shortest_path

    def reverse_a_star(self, g_bigger):
        self.goal_node.g_score = 0
        self.goal_node.h_score = self.heuristic(self.goal_node, self.start_node)
        self.goal_node.f_score = self.goal_node.g_score + self.goal_node.h_score
        self.open_list.insert(self.goal_node)

        while self.open_list.is_empty() is False:
            current_node = self.open_list.pop()
            self.closed_list.append(current_node)

            if current_node.x == self.start_node.x and current_node.y == self.start_node.y:
                return self.get_shortest_path(current_node)

            self.get_neighbors(current_node, g_bigger=g_bigger)

        return None

    def adaptive_heuristic(self, current_node, goal_node):
        return goal_node.g_score - current_node.g_score

    def adaptive_a_star(self, g_bigger):
        self.forward_a_star(g_bigger)  # Run forward A* to get the closed list
        self.start_node.g_score = 0
        self.start_node.h_score = self.adaptive_heuristic(self.start_node, self.goal_node)
        self.start_node.f_score = self.start_node.g_score + self.start_node.h_score

        for node in self.closed_list:
            node.h_score = self.adaptive_heuristic(node,
                                                   self.goal_node)  # Update the heuristic of all nodes in the closed list as per directions, this is allowed
            node.f_score = node.g_score + node.h_score

        self.closed_list = []  # Clear the closed list
        self.open_list = BinaryHeap()
        self.open_list.insert(self.start_node)

        while self.open_list.is_empty() is False:
            current_node = self.open_list.pop()
            self.closed_list.append(current_node)

            if current_node.x == self.goal_node.x and current_node.y == self.goal_node.y:
                return self.get_shortest_path(current_node)

            self.get_neighbors(current_node, adaptive=True, g_bigger=g_bigger)

        return None


def a_star_maze(maze_number, a_star_obj, a_star_algorithm, folder_name_path, start_time):
    time_taken = time.time() - start_time
    path = a_star_algorithm

    [cell.draw() for cell in a_star_obj.maze_cells]

    for x, node in enumerate(path):
        pygame.draw.circle(a_star_obj.maze.screen, (0, 191, 255), (node.x * 10 + 5, node.y * 10 + 5), 2)

    pygame.image.save(a_star_obj.maze.screen, f"{folder_name_path}/maze{maze_number}.png")

    return time_taken


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "-9999, -9999"  # This is to hide the pygame window

    forward_a_star_times = []
    reverse_a_star_times = []
    adaptive_a_star_times = []
    total_forward_a_star_time = 0
    total_reverse_a_star_time = 0
    total_adaptive_a_star_time = 0

    for _maze_number in range(50):
        _maze_file = f"../mazes/maze{_maze_number}.maze"
        _folder_name_path = f"../mazes/Forward_A_Star_Solutions/"
        _a_star = AStar(_maze_file)
        _start_time = time.time()
        _time_taken = a_star_maze(_maze_number, _a_star, _a_star.forward_a_star(g_bigger=True), _folder_name_path, start_time=_start_time)
        total_forward_a_star_time += _time_taken
        forward_a_star_times.append(f"Maze {_maze_number} solved in {_time_taken} seconds with forward A*")
        print(forward_a_star_times[_maze_number])

    for _maze_number in range(50):
        _maze_file = f"../mazes/maze{_maze_number}.maze"
        _folder_name_path = f"../mazes/Reverse_A_Star_Solutions/"
        _a_star = AStar(_maze_file)
        _start_time = time.time()
        _time_taken = a_star_maze(_maze_number, _a_star, _a_star.reverse_a_star(g_bigger=True), _folder_name_path, start_time=_start_time)
        total_reverse_a_star_time += _time_taken
        reverse_a_star_times.append(f"Maze {_maze_number} solved in {_time_taken} seconds with reverse A*")
        print(reverse_a_star_times[_maze_number])

    for _maze_number in range(50):
        _maze_file = f"../mazes/maze{_maze_number}.maze"
        _folder_name_path = f"../mazes/Adaptive_A_Star_Solutions/"
        _a_star = AStar(_maze_file)
        _start_time = time.time()
        _time_taken = a_star_maze(_maze_number, _a_star, _a_star.adaptive_a_star(g_bigger=True), _folder_name_path, start_time=_start_time)
        total_adaptive_a_star_time += _time_taken
        adaptive_a_star_times.append(f"Maze {_maze_number} solved in {_time_taken} seconds with adaptive A*")
        print(adaptive_a_star_times[_maze_number])

    with open("../mazes/Forward_A_Star_Solutions/forward_a_star_times.txt", "w") as f:
        for _line in forward_a_star_times:
            f.write(f"{_line}\n")
        f.write(f"Total time taken for forward A* is {total_forward_a_star_time} seconds.\nThe average time taken for forward A* is {total_forward_a_star_time / 50} seconds")

    with open("../mazes/Reverse_A_Star_Solutions/reverse_a_star_times.txt", "w") as f:
        for _line in reverse_a_star_times:
            f.write(f"{_line}\n")
        f.write(f"Total time taken for reverse A* is {total_reverse_a_star_time} seconds.\nThe average time taken for reverse A* is {total_reverse_a_star_time / 50} seconds")

    with open("../mazes/Adaptive_A_Star_Solutions/adaptive_a_star_times.txt", "w") as f:
        for _line in adaptive_a_star_times:
            f.write(f"{_line}\n")
        f.write(f"Total time taken for adaptive A* is {total_adaptive_a_star_time} seconds.\nThe average time taken for adaptive A* is {total_adaptive_a_star_time / 50} seconds")


if __name__ == "__main__":
    # Part 2 of the assignment: Breaking ties with bigger and smaller g scores
    part2_g_bigger_times = []
    part2_g_smaller_times = []
    total_part2_g_bigger_time = 0
    total_part2_g_smaller_time = 0

    for maze_number in range(50):
        maze_file = f"../mazes/maze{maze_number}.maze"
        folder_name_path = f"../mazes/Part2_G_Values/"
        a_star = AStar(maze_file)
        start_time = time.time()
        time_taken = a_star_maze(maze_number, a_star, a_star.forward_a_star(g_bigger=True), folder_name_path, start_time=start_time)
        part2_g_bigger_times.append(f"Maze {maze_number} solved in {time_taken} seconds with forward A* and g values bigger when we encounter a tie")
        total_part2_g_bigger_time += time_taken
        print(part2_g_bigger_times[maze_number])

    for maze_number in range(50):
        maze_file = f"../mazes/maze{maze_number}.maze"
        folder_name_path = f"../mazes/Part2_G_Values/"
        a_star = AStar(maze_file)
        start_time = time.time()
        time_taken = a_star_maze(maze_number, a_star, a_star.forward_a_star(g_bigger=False), folder_name_path, start_time=start_time)
        part2_g_smaller_times.append(f"Maze {maze_number} solved in {time_taken} seconds with forward A* and g values smaller when we encounter a tie")
        total_part2_g_smaller_time += time_taken
        print(part2_g_smaller_times[maze_number])

    with open("../mazes/Part2_G_Values/part2_g_bigger_times.txt", "w") as f:
        for line in part2_g_bigger_times:
            f.write(f"{line}\n")
        f.write(f"Total time taken for forward A* with g values bigger when we encounter a tie is {total_part2_g_bigger_time} seconds.\nThe average time taken for each maze is {total_part2_g_bigger_time/50} seconds")

    with open("../mazes/Part2_G_Values/part2_g_smaller_times.txt", "w") as f:
        for line in part2_g_smaller_times:
            f.write(f"{line}\n")
        f.write(f"Total time taken for forward A* with g values smaller when we encounter a tie is {total_part2_g_smaller_time} seconds.\nThe average time taken for each maze is {total_part2_g_smaller_time/50} seconds")

    main()
