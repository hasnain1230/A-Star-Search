import os
from subprocess import Popen
import time

if __name__ == "__main__":
    start_time = time.time()
    # os.system("rm -rf ../mazes/*")
    commands = []
    for x in range(50):
        commands.append(["python3", "src/MazeGenerator.py", str(x)])

    processes = [Popen(cmd) for cmd in commands]

    for p in processes:
        p.communicate()

    end_time = time.time()

    print(f"Time taken to generate all 50 mazes: {end_time - start_time} seconds")
