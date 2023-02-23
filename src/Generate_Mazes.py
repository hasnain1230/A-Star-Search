import os
import sys
from subprocess import Popen
import time

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "single_threaded":
        start_time = time.time()
        os.system("rm -rf ../mazes/maze*")
        for x in range(50):
            os.system(f"python3 MazeGenerator.py {x}")
        end_time = time.time()

        print(f"Time taken to generate all 50 mazes: {end_time - start_time} seconds")
    else:
        start_time = time.time()
        os.system("rm -rf ../mazes/maze*")
        commands = []
        for x in range(50):
            commands.append(["python3", "MazeGenerator.py", str(x)])

        processes = [Popen(cmd) for cmd in commands]

        for p in processes:
            p.communicate()

        end_time = time.time()

        print(f"Time taken to generate all 50 mazes: {end_time - start_time} seconds")
