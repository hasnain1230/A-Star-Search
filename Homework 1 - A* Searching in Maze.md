# Homework 1 - A* Searching in Maze
This assignment demonstrates variations of the A* searching algorithm. Please refer to the source code for how these algorithms were implemented. It should be contained within this archive in the `src` directory.

# Author
- Hasnain Ali (h430)

# Pre-Requisite
- The code in this archive was tested on Python 3.8 and newer. If you do not have Python 3.8, I highly recommend that you download it. 
- This code was only tested on Linux machines. You can go to Rutger's iLab [weblogin](https://weblogin.cs.rutgers.edu/) page to download access the Linux iLab machines remotely. You need to have a graphical display to run the code, so you **CANNOT** `ssh` into the iLab machines. You must use some kind of graphical display server / driver / device that can display graphics. The weblogin is probably the easiest way. 
	- You can probably also run this on Mac, but it has not been tested. I do not see a reason why that would cause issues however.
	- On Windows, you might get some file path errors. You can go into the source code and escape any file paths with a `\\` since Windows uses `\` for file paths, you need to escape it for it to work.
		- I simply did not have the time to write code to fix this because I was assuming everyone would be testing the code on some kind of a Linux / Unix compliant machine.
- You MUST have PyGame installed. The source code uses this as a dependency. To install it on a Linux system, you can do:
	- `python3 -m pip install pygame`
	- Replace `python3` with your alias for Python.
		- For example, if on your machine, the alias for python is just `python`, then just write `python` instead of `python3`

# Note to Grader
Please Note: The professor said use of LaTeX is optional. That being said, I am writing this report using Markdown, a markup language with various styling choices built into the format. **THIS DOES SUPPORT LaTeX** and I am writing LaTeX equations, simply in Markdown. I have not spoken with the professor yet whether that is okay or not and if it warrants extra credit, but because I am still using LaTeX (which you can confirm, the original Markdown file is in the archive), I hope I am granted the extra credit points. 

- Also, I did create my own `BinaryHeap`. The professor states extra points will be awarded for students who implement their own binary heap.
- Furthermore, in ALL instances of A-Star, the agent starts at point (0, 0) and the goal state for the agent in all instances of A-Star is point (100, 100). Thus, the agent starting node is at the top left corner of the maze and the goal state is at the bottom right corner.
- **READ: IF you are using PyCharm to run this code, you must either set your script path to the `src` folder, or navigate to the `src` folder in the terminal and run the scripts there. Please make sure you run the scripts correctly. They have been tested on the iLab machines. You can also leave a comment in Canvas if you are having an issue and I will help you get the scripts running.** 
- Lastly, all Python source code files are in the `src` directory. Please navigate to `src` before you run any Python files as most files use the relative path from `src` to store maze related files and the functionality may break if you do not do this. Do not run, `python3 src/Generate_Mazes.py` as this will not work and throw errors. You must be in `src` in order to run these files. So, do, `cd path/to/src` and then run `python3 Generate_Mazes.py` for example.
- Also, the run times I got may not be the same run times you get for the algorithms as we are on different machines.
- ALL THE SCRIPTS HAVE BEEN TESTED AND ARE WORKING. HOWEVER, SINCE THESE SCRIPTS USE RELATIVE PATHS TO THE `src` FOLDER, YOU MAY HAVE TO TINKER WITH SOME SETTINGS AND/OR TINKER WITH THE WAY YOU ARE running the script. PLEASE REFER TO THESE WRITTEN DIRECTIONS IF YOU ARE HAVING TROUBLE, OR REACH OUT TO ME VIA CANVAS COMMENT OR EMAIL!!!

## Part 0
The archive that was submitted should have the pre-generated mazes that were already made. To view these mazes, you can go to view them as a `.png` picture, or you can see the walls in text form by viewing a `.maze` file. All the mazes, the `.maze` files, and the `.png` files are stored in the `mazes` directory. The `.maze` files were generated in order to rebuild the maze and perform the A* searches on it. My code does use these files, so make sure they exist before you try to run any of the other files.

If you want generate a single maze, please run `MazeGenerator.py {maze number}` where maze number is the number of maze you want to generate. The maze number **does not** indicate how many mazes you want to generate, it is simply there to name the maze files. The number you provide will not affect the performance, it will simply depend what number the generated files will have.

If you want to generate all 50 new mazes, please run, `python3 Generate_Mazes.py`. **Please Note**: This file will be generating 50 mazes **SIMULTANEOUSLY**. If you decide to run it on your own system, please note, you will, with most systems (even my own high end system), notice *major* performance issues since there are 50 mazes being generated at once. Alternatively, if you wish to not experience this performance lag, you can run `python3 Generate_Mazes single_threaded` and this will generate one maze at a time, but it will probably take three or six hours to generate all these mazes. So, you're best off just simply using the mazes in the `maze` directory.

If you want to visualize a certain maze file again (and not use the picture), you can run `python3 RegenMaze.py {path/to/maze.maze/file` and it will generate a new maze visual for you given a maze file if you'd like to reconstruct the maze file.

To summarize:
- To generate one maze, run `python3 {maze number}` where `{maze_number}` is the maze number the generates files will have. It does not generate multiple mazes, it will generate one maze with a specific number on the generated files. It has no impact on performance.
- To generate all 50 mazes simultaneously, (this will cause performance slow downs on most machines outside of enterprise grade hardware with many threads), run, `python3 Generate_Mazes.py`
- To generate all 50 mazes, one at a time, to reduce the performance impact, run `python3 Generate_Mazes.py single_threaded`
- To generate a single maze from a `.maze` file, run `python3 RegenMaze.py {path/to/maze.maze/file}`

## Part 1A
When the agent starts in this problem, the agent is going to move east first since it does not know about the blockage at E4. It can only see that cell E3 is unblocked. Since the heuristic is essentially seeing a straight line to reach the target, (based on the Manhattan Distance), the agent when it is first starting thinks (based on the heuristic) that it is able to directly reach the target node. Since it can only see one cell far, it is unaware of the blockage. So, the agent is going to move east first, rather than north because it cannot see the blockage east going to the target. This is because of the heuristic we provided. The heuristic simply looks for the Manhattan Distance without paying attention to blocks. After moving to each cell, the agent calculates a new heuristic and $f$ value when it expands a new cell.

## Part 1B
Suppose we visualize the grid world as a graph (assuming it is finite). If there is a path from the starting state to the goal state, there will be a connected component of the graph from the starting state to the goal state. That is, if each cell is a node, and if there is a path from one cell to another, there will be nodes connecting the first and second node. Thus, this is a connected component. 

In other words, suppose $Cell A$ and $Cell B$ are adjacent with no cells in between them and no blockages. Then, that means there is a connected component from $Cell A$ and $Cell B$ in the graph. Applying this principal, if there is a connected component anywhere in the grid world, assuming that the grid world is finite, then that means there is a path from $A$ to $B$. If there is a block from $A$ to $B$, making $A$ and $B$ not to be in connected components, then there is no path.

So, assuming there is no blockage in the grid world, and $A$ and $B$ definitely do exist in the gird world, then that means there is a path between the two since there is a connected component. In other words, all unblocked cells are in a connected component on the graph. So, if $Starting State$ and $Ending State$ are within the same connected component, then that means there must be a path between the two. If the $Starting State$ and $Ending State$ are not in the same connected component, then that means there must be some cells or obstacles blocking a path between them and there is no path. 

Thus, if there is a series of unblocked cells such that it connects $Starting State$ and $Ending State$ such that they satisfy the definition of a connected component in the graph, then there must exist a path between the states. However, if there $Starting State$ and $Ending State$ are not in the same connected component, there no path can be found.

The number of moves the agent must make before determining that $Starting State$ and $Ending State$ are not in the same connected component, is upper-bounded by $\left(unblocked\:cells\right)^2$. Thus, after travelling $\left(unblocked\:cells\right)^2$ cells, the agent can determine whether it found the shortest path between $Starting State$ and $Ending State$, or if no path exists.

It is $\left(unblocked\:cells\right)^2$ because, at any given moment in time, an unblocked cell has $n - 1$ unblocked cells connected to itself since it cannot be connected to itself. Therefore, the total number of connected cells between $Starting State$ and $Ending State$ is $n\:\cdot \left(n-1\right)$ where $n$ is the number of unblocked cells between $Starting State$ and $Ending State$. Thus, the upper bound for the total number of unblocked cells between $Starting State$ and $Ending State$ must be $\left(unblocked\:cells\right)^2$ based on $n - 1$ connected cells to any unblocked cell in the grid world.

**Hence, proved.**

## Part 2
This problem states that one may use either run time, or the number of expanded cells. I have decided to use the run time in my analysis.

To see the results of my run time when tie-breaking $g$ values larger, and $g$ values bigger, please see `mazes/Part2_G_Values/part2_g_bigger_times.txt` for when we were tie breaking based on the larger $g$ value, and `mazes/Part2_G_Values/part2_g_smaller_times.txt` for when we were breaking ties based on the smaller $g$ value.

Please Note:
- Both versions of forward A*, variation with tie breaking of bigger $g$ values and variation with tie breaking of smaller $g$ values used the **EXACT SAME MAZES**
- Also, the timings we got do not include drawing the maze, it only calculates the time it took to find a part from `start_node` to `goal_node`. It does not count the time it took to draw the maze and path, and save the image.

To see the source code for how these tests were written, please the comment in `src/A-Star.py` that says, `# Part 2 of the assignment: Breaking ties with bigger and smaller g scores` to see the implementation of forward A* and how the runtime was calculated, and all other implementation details. When the $g$ values were bigger, `forward_a_star` searching algorithm ran with a total time of $118.61599850654602$$ seconds with an average time of $2.3723199701309206$ seconds per forward A* search per maze. You can view the dump file for all the timings `mazes/Part2_G_Values/part2_g_bigger_times.txt`. When we were breaking ties, if the smallest $f$ values were the same, we would look at all nodes and set the nodes with the bigger $g$ values to be inserted into the open list first, followed the the nodes with the smaller $g$ values after. 

We followed a similar procedure for the breaking ties via the smaller $g$ value. You can view the dump for these values here: `mazes/Part2_G_Values/part2_g_smaller_times.txt`. On average, each maze was solved in $2.4213880586624144$ seconds with a total time to solve all the mazes being, $121.06940293312073$ seconds. 

Clearly, we can see from these numbers, tie breaking equal $f$ values with bigger $g$ values is more optimal than breaking ties with smaller $g$ values. 

Using this formula: $$Percentage\:Difference=\left(\frac{\left|A-B\right|}{\frac{\left(A+B\right)}{2}}\right)\cdot 100$$
We can calculate the percentage difference between the total times, and average times.

Setting $$A = 2.4213880586624144$$ $$and$$ $$B = 2.3723199701309206$$
into the formula, we get: $$Percentage\:Difference=\left(\frac{\left|\left(2.4213880586624144\right)-\left(2.3723199701309206\right)\right|}{\frac{\left(\left(2.4213880586624144\right)+\left(2.3723199701309206\right)\right)}{2}}\right)\cdot \:100=2.04727\:\%$$
Doing the same thing for total time difference, we get:
$$Percentage\:Difference=\left(\frac{\left|\left(121.06940293312073\right)-\left(118.61599850654602\right)\right|}{\frac{\left(\left(121.06940293312073\right)+\left(118.61599850654602\right)\right)}{2}}\right)\cdot \:100=2.04727\:\%$$

Thus, as we can see, when we break equal $f$ values ties using higher $g$ values is better as it yields about a $2$ % benefit in the mazes we generated. 

The reason tie breaking $f$ values with higher $g$ values is better is because a higher $g$ value ensures we are closer to the goal node as that indicates we are further away from the starting node. Since our $StartingState$ and $EndingState$ are on opposite sides of the maze, when the $GoalState$ is founded, the $g$ value will be at the farthest possible point point on the grid, and thus, the $g$ value being bigger ensures we are getting closer to the $GoalState$. The further we are from the $StartingState$ the closer we are getting to a solution, hence the higher $g$ value is better. Additionally, higher $g$ values ensure a more consistent $f$ value since our $GoalState$ must be as far as possible from $StartingState$.

For these optimality and consistency reasons, we can further understand now how we saw a performance increase when breaking $f$ value ties using higher $g$ values.

## Part 3
This problem states that one may use either run time, or the number of expanded cells. I have decided to use the run time in my analysis.

To see the results of my run time when tie-breaking $g$ values larger, and $g$ values bigger, please see `mazes/Forward_A_Star_Solutions/forward_a_star_times.txt` for when we were tie breaking based on the larger $g$ value, and using forward A* search. To see results of reverse A* search, still using larger $g$ value tie breaking, please see, `mazes/Reverse_A_Star_Solutions/reverse_a_star_times.txt`.

Please Note:
- Both forward A* and reverse A* variations were done with tie breaking of bigger $g$ values on the **EXACT SAME MAZES**
- Also, the timings we got do not include drawing the maze, it only calculates the time it took to find a part from `start_node` to `goal_node`. It does not count the time it took to draw the maze and path, and save the image.

To see the source code for how these tests were written, please the `main()`  function in in `src/A-Star.py` to see the implementation of forward A* and reverse A*, how the runtime was calculated, and all other implementation details. To be condense, we will no longer state our $g$ value tie breaking method, please assume this going forward for this part only.

Forward A* search with the previously mentioned tie breaking method took a total of $123.02186870574951$ seconds to find the paths in all mazes. The average time it took to find a path per maze was $2.4604373741149903$ seconds.

Reverse A* search with the previously mentioned tie breaking method took a total of $293.88777685165405$ seconds find the paths in all mazes. The average time it took to find a path per maze was $5.877755537033081$ seconds. 

The reason Reverse A* search was so much slower than Forward A* is because the branching factor when going in reverse is much larger than the branching factor when going forward. There are more nodes and paths to explore when going backwards, hence why it took longer. Because of this large branching factors and may ways to get to one location (there are many ways to get from the $StartingState$ to the $GoalState$), so when we are going backwards, the branching factor is much more significant. This means that more nodes have to be expanded before we find a path which simply takes much longer as compared to forward A* search where based on the heuristic and number of short paths to get to the $GoalState$, in these mazes in our case, Forward A* search was much faster. 

(Also, I was monitoring my CPU temperatures during this test. The CPU was running at it's rated speed for all A-Star path searching algorithms. That was not a limiting factor here. The CPU did not exceed 80**°** C.)

Using this formula: $$Percentage\:Difference=\left(\frac{\left|A-B\right|}{\frac{\left(A+B\right)}{2}}\right)\cdot 100$$
We can calculate the percentage difference between forward A* search and reverse A* search.

We can calculate the percentage difference between the average times.

Setting $$A = 5.877755537033081$$ $$and$$ $$B = 2.4604373741149903$$
into the formula, we get: $$Percentage\:Difference=\left(\frac{\left|\left(5.877755537033081\right)-\left(2.4604373741149903\right)\right|}{\frac{\left(\left(5.877755537033081\right)+\left(2.4604373741149903\right)\right)}{2}}\right)\cdot \:100=81.9678\:\%$$
(Total percentage difference would have the same percentage value as the average percentage distance.)

Based on these results, we can confidently that forward A* search is much more efficient and optimal compared to reverse A* search, based on the runtime alone as $81.9$ % is a significant increase in performance. Please see the explanation above for why this occurred in the differences between the two search algorithms.

## Part 4
Please see `src/A-Star.py` to see the for the implementation details of forward A*, reverse A*, and adaptive A* searching algorithms.

To prove that Manhattan Distances are consistent in grid worlds, we need to prove the following: $$\forall x \in (n, a, n'):h\left(n\right)\le c\left(n,\:a,\:n'\right)+h\left(n'\right)$$
Where $c\left(n,\:a,\:n'\right)$ is the step cost for going from $n$ to $n'$ using action $a$

By definition, we have for Manhattan Distances:
$$Manhattan\:Distance\:=\:\left|x_1-x_2\right|+\left|y_1-y_2\right|$$
Where $x_1$ and $y_1$ are the first coordinate pairs and $x_2$ and $y_2$ are the second coordinate pairs. Suppose we have three points, $A,\:B,\:and\:C$  where $A$ and $B$ are a are adjacent to each other and $C$ is adjacent to $B$. The cost of moving from $A$ to $B$ is $1$ and the cost of moving from $B$ to $C$ is $1$. 

Now we can prove that the Manhattan Distance from A to B is 1, and so is the Manhattan distance from B to C, so the following is true:
$$\left|Manhattan\:Distance\left(A,B\right)-Manhattan\:Distance\:\left(B,C\right)\right|\le ActionCost\left(A,B\right)$$
This means that:
$$\left|\left(\left|Ax-Bx\right|+\left|Ay-By\right|-\left(\left|Cx-Bx\right|+\left|Cy-By\right|\right)\right)\right|\le 1$$
Which means that:
$$\left|\left(Ax-Cx\right)+\left(Ay-Cy\right)\right|\le 1$$
This is true because the distance from A to C must also be 1, so we satisfy the definition of a consistent heuristic as we defined earlier. The heuristic will always be larger than 1, in any case, as long as their exists a gird world. This means that the Manhattan Distance is always consistent as defined by a consistent heuristic. **Thus, this has been proved.**

Furthermore, by definition, Adaptive A* search will initially has a consistent heuristic because of the way the heuristic is calculated and because of the definition of Adaptive A* search. The heuristic used is: 
$$h(s):=g(s_{goal}) - g(s)$$This will initially under estimate the heuristic or be equal to the step cost plus the next heuristic function as stated in the prior definition of a consistent heuristic: $$\forall x \in (n, a, n'):h\left(n\right)\le c\left(n,\:a,\:n'\right)+h\left(n'\right)$$
This is because the cost to get to the goal minus the current cost will always be less than the cost of getting the next node, plus the next heuristic cost. The given heuristic will initially under estimate because the cost for action plus the next heuristic will always be greater than the current heuristic which is calculated by using the goal cost. Because of this property, adaptive A* will initially be consistent, even if the step cost increases.

**Hence, proved.**

## Part 5
Please see `src/A-Star.py` to see the for the implementation details of forward A*, reverse A*, and adaptive A* searching algorithms.

This problem states that one may use either run time, or the number of expanded cells. I have decided to use the run time in my analysis.

To see the results of my run time when tie-breaking $g$ values larger, and $g$ values bigger, please see `mazes/Forward_A_Star_Solutions/forward_a_star_times.txt` for when we were tie breaking based on the larger $g$ value, and using forward A* search. To see results of adaptive A* search, still using larger $g$ value tie breaking, please see, `mazes/Adaptive_A_Star_Solutions/adaptive_a_star_times.txt`.

Please Note:
- Both forward A* and reverse A* variations were done with tie breaking of bigger $g$ values on the **EXACT SAME MAZES**
- Also, the timings we got do not include drawing the maze, it only calculates the time it took to find a part from `start_node` to `goal_node`. It does not count the time it took to draw the maze and path, and save the image.

To see the source code for how these tests were written, please the `main()`  function in in `src/A-Star.py` to see the implementation of forward A* and reverse A*, how the runtime was calculated, and all other implementation details. To be condense, we will no longer state our $g$ value tie breaking method, please assume this going forward for this part only.

Forward A* search with the previously mentioned tie breaking method took a total of $123.02186870574951$ seconds to find the paths in all mazes. The average time it took to find a path per maze was $2.4604373741149903$ seconds.

Adaptive A* search with the previously mentioned tie breaking method took a total of $242.34785318374634$ seconds with an average of $4.846957063674926$ seconds. 

The reason Adaptive A* search took so long was because it first had to find a path, and therefore calculate the $g$ value of the goal node. This meant first doing forward A* search normally to get the $g$ values and the best path, and then updating the heuristics of every cell in the closed with the new heuristic value. Then we do adaptive A* search with the new heuristics. Normally, we would store the updated heuristic values for all the nodes in the updated list, so when we call adaptive A* search over and over, we do not need to do forward A* search every time. Doing this extra forward A* search to get the closed list is what slowed the algorithm down. Normally, this would not be the case. The purpose of this algorithm is to decrease the branching factor so that we find the $GoalState$ much faster. Normally, we would store the new heuristic values for the nodes in the closed list so we can get right into the search, but in this case, we are not storing the values, so getting the closed list for adaptive A* search is what caused this major decrease in performance, although this is not reflective of a real world performance for the new heuristic values are already known, or are easily calculated. This implementation first had to find the distance to the $GoalState$ by doing forward A* first, and then doing the adaptive A* search which increased the overall runtime of the algorithm. 

Nonetheless, we can calculate the percent difference of forward A* search and adaptive A* search to see how much faster forward A* search was. 

Using this formula: $$Percentage\:Difference=\left(\frac{\left|A-B\right|}{\frac{\left(A+B\right)}{2}}\right)\cdot 100$$
We can calculate the percentage difference between forward A* search and reverse A* search.

We can calculate the percentage difference between the average times.

Setting $$A = 4.846957063674926$$ $$and$$ $$B = 2.4604373741149903$$
into the formula, we get: $$Percentage\:Difference=\left(\frac{\left|\left(4.846957063674926\right)-\left(2.4604373741149903\right)\right|}{\frac{\left(\left(4.846957063674926\right)+\left(2.4604373741149903\right)\right)}{2}}\right)\cdot \:100=65.318\:\%$$
(Total percentage difference would have the same percentage value as the average percentage distance.)

Based on these results, we can confidently that forward A* search is much more efficient and optimal compared to adaptive A* search in the case when we need to first calculate the path to the goal state and then update the heuristic as we did here. If that was not the case, this would have been much faster and comparable against forward A* search. Here, we had to first find the closed list so we could update the heuristics for that closed list because we could run A* search again. This significantly reduced our run time. So, while forward A* search was much faster than adaptive A* search, that is not the entire story as in adaptive A* search, we had to run forward A* search again to get the closed list, to get the $g$ values of the final state to then calculate the heuristic again to do forward A* search more optimally. These steps are significantly more, hence the longer runtime of adaptive A* search. 

## Part 6
A statistical hypothesis test for forward A* search and reverse A* can be done to understand if there is bias in the experimental method, or if the change in performance we saw is simply insignificant and a result of nature (random, with no meaning). We can do this by doing the following:
- First, we need to define the null hypothesis $H_0$ and an alternative hypothesis $H_1$. In this case, $H_0$ may indicate there is no significant difference between forward and backward A* search while $H_1$ would indicate that there is a significant performance difference between the two. 
- Then, we would do a t-test: $$t = \frac{\overline{x}_1 - \overline{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$
	- Where is $s$ is the standard deviation, $n$ is the sample size, and $\overline{x}_1, \overline{x}_2$ are the means average run time of reverse A* for $\overline{x}_1$ and forward A* average runtime for $\overline{x}_2$. 
	- This t-test would allow for a proper statistic for us to use.
- Then, we can find a $p$ value to determine whether or not or not there is a significant difference between forward A* search and reverse A* search. The generally accepted rule is if the $p$ value yields a value higher than 5%, then were is something beyond random natural events that is causing a difference between the two values. In other words, there is a significant difference between the two values (in this case, the average run time of forward A* search and reverse A* search). If that is not the case and the $p$ value is less than $5$%, then 
- We can calculate the $p$ value using this formula to get $z$:
  $$z = \frac{\bar{X_1} - \bar{X_2} - (\mu_1 - \mu_2)}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}$$
- And then using this formula to get the $p$ value: $$p = (1 - z) * 100$$
- Thus, we can find the $p$ value and do a statistical hypothesis test this way.