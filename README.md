There are 200 input files in the directory named "input", and 100 output files in the directory named "output".  
Every two input files correspond to one output file.  
For example, input_0.dat and input_1.dat correspond to output_0.dat; input_2.dat and input_3.dat correspond to output_2.dat, and so on.  
The first input file contains the first N flows, and the second input file contains N additional flows.

## In each input file:
1. The first line is the number of flows (N).
2. The second line is the number of links (M).
3. The following N lines are utilizations of flows (U).
4. The following N lines are the numbers of possible paths of flows (P).
5. The follwing (P_i * M) matrices represent the links in paths of flows.  
   For example,  
   1 0 0 1 1  
   0 1 1 0 0  
   means the flow has two possible paths(because two rows),   
   and the 1st possible path uses link 0, link 3, and link 4,  
   and the 2nd possible path uses link 1 and link 2.  
     
Example of input:  
2   
5  
0.1  
0.2   
2  
2  
1 1 0 0 0  
0 0 1 1 1  
0 0 1 0 0  
1 1 0 1 1  
  
It means there are 2 flows and 5 links.  
The utilization of flow 0 is 0.1.  
The utilization of flow 1 is 0.2.  
Flow 0 has 2 possible paths.  
Flow 1 has 2 possible paths.  
The path 0 of flow 0 uses link 0, 1.  
The path 1 of flow 0 uses link 2, 3, 4.  
The path 0 of flow 1 uses link 2.  
The path 1 of flow 1 uses link 0, 1, 3, 4.  
  
  
## In each output file:  
There are 4N lines, and each line contains a number 0 or 1 or -1.  
0 means clockwise; 1 means counterclockwise; -1 means no path can be used(remaining capacity of some links are not enough for this flow).  
(I assume the link with the smallest index as the source link.)   
The first 2N lines are the directions of paths chosen for flows by MILP.  
The following 2N lines are the directions of paths chosen for flows by All Shortest Path.  
