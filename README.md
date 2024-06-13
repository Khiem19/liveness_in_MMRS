# liveness_in_MMRS

The management of Multiple Mobile Robot Systems (MMRS) involves significant challenges in ensuring efficient, safe, and collision-free operations. MMRS, consisting of autonomous mobile robots, require dynamic modification of motion control to maintain disjoint areas of operation and accomplish missions within finite time intervals. The primary objective is to achieve collision-free motion while preventing deadlocks, thus ensuring system liveness.

The aim of this thesis is to investigate the application of Petri nets as a modeling framework for MMRS, focusing on ensuring system liveness. The research explores the use of Petri nets for their formal and graphical representation capabilities to capture and analyze complex interactions within MMRS. Two algorithms, a Depth-First Search (DFS)-based algorithm and a modified Banker’s algorithm, are developed to enhance MMRS control strategies.

The DFS-based algorithm optimally trims the state-space, ensuring only live states are reachable by identifying transitions from live to non-live states. The modified Banker’s algorithm,  provides a polynomial-time complexity solution by ensuring state reachability based on sufficient conditions. Experimental results demonstrate the effectiveness of these algorithms in preventing deadlocks and maintaining smooth operation in shared environments.

The study concludes that the proposed algorithms effectively avoid deadlocks and ensure the smooth operation of MMRS.
