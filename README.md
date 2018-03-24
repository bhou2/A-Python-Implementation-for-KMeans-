# A Python Implementation for KMeans

This is the implementation of the classic K-Means algorithm for the CSC 7442 course project at LSU,
aiming to test the K-Means algorithm with different K values. 

kmeans.py contains the source code; clusterdata.csv contains the data points. 

Note that there are generally two stop conditions for the clustering process: 
(1) setting a maximum iteration number; 
(2) setting a threshold for SSE (the sum of standard errors). 
In the current implementation, as required by the course project, stop condition (1) is used; 
the default iteration number is 1,000.

In addition, the current implementation focuses on clustering two-dimensional points, but is 
easy to be extended to fit for points of higher dimensions.

The code has been tested to work well on Ubuntu 16.04 with Python 2.7.12. 

