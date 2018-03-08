#!/usr/bin/env python

'''
K-Means implementation for the CSC 7442 course project at LSU
'''

import sys
import math
import random

class Cluster:
    '''
    define the generated clusters
    @cpoints: the points assigned to the cluster
    @cent: the centroid of the cluster
    @sse: the sum of squared errors, which is used to measure the quality of a cluster
    @weight: the ratio of the number of points in the cluster to the total number of points
   '''
    def __init__(self,cent):
        self.cpoints = [] 
        self.cent = cent 
        self.sse = 0 
        self.weight = 0  
    def ref_point(self):
        self.cpoints = []
    def add_point(self,point):
        self.cpoints.append(point)
    def get_cent(self):
        return self.cent
    def get_points(self):
        return self.cpoints
    def get_num(self):
        return len(self.cpoints)
    def get_sse(self):
        return self.sse
    def get_weight(self):
        return self.weight
    def cal_weight(self, total):
        self.weight = len(self.cpoints)*1.0/total
    def cal_cent(self): 
        sumx = 0; sumy = 0; num = 0
        for x,y in self.cpoints:
            sumx += float(x)
            sumy += float(y)
            num += 1
        if num > 0:
            self.cent = sumx*1.0/num, sumy*1.0/num
    def cal_sse(self):
        sse = 0.0
        cx,cy = self.cent       
        for x,y in self.cpoints:
            sse += math.pow(float(x)-float(cx),2)+math.pow(float(y)-float(cy),2)
        self.sse = sse

def init_points(filename):
    '''
    load points from data file to memory
    @filename: the path of the datafile

    Note: the points are 2D in the data file 
    '''
    points = []
    fp = open(filename)
    for line in fp.readlines():
        x,y = line.split(',') # points are stored as x,y in the file
        p = x,y
        points.append(p) 
    fp.close()
    return points    

def init_clusters(points, K):
    '''
    initialize the clusters
    @points: the point list
    @K: the number of clusters to be generated 
    '''
    cents = []; clusters = []
    for i in range(K):

        'select a random point as the centroid of the clusters at the first clustering iteration'
        cent = get_rand_cent(points)

        'the while loop is used to prevent two clusters from being assigned the same centroid' 
        while check_exist(cent,cents):
            cent = get_rand_cent(points)
        cents.append(cent)   

        'the cluster is initially empty, with an randomly selected centroid' 
        cluster = Cluster(cent) 
        clusters.append(cluster)
    return clusters

def distance(p1,p2):
    '''
    calculate the Euclidean distance between two points
    @p1: data point x1,y1
    @p2: data point x2,y2
    '''
    x1,y1 = p1
    x2,y2 = p2
    return math.sqrt(math.pow(float(x1)-float(x2),2)+math.pow(float(y1)-float(y2),2))

def check_exist(point,cents):
    '''
    check whether the point has been selected as the centroid for other clusters
    @point: the point to be checked
    @cents: the set of the points that have been selected as the centroids for other clusters
    '''
    px,py = point
    for c in cents:
        cx,cy = c
        if cx == px and cy == py:
            return True
    return False

def get_rand_cent(points):
    '''
    randomly selected a point as a centroid
    @points: the point list
    '''
    pindex=random.randint(0,len(points)-1)
    return points[pindex]

'''
The next three functions: refresh_clusters, refresh_points, refresh_cents
are used to refresh the clusters at different stages of the clustering process
@clusters: the cluster list
'''
def refresh_clusters(clusters):
    'clean the points and calculate the centroid of each cluster'
    
    for cluster in clusters:
        cluster.ref_point() 
        cluster.cal_cent() 

def refresh_points(clusters):
    'clean the points'
    
    for cluster in clusters:
        cluster.ref_point() 

def refresh_cents(clusters):
    'calculate the centroid and SSE of each cluster'
    
    for cluster in clusters: 
        cluster.cal_cent() # calculate the centroid
        cluster.cal_sse()

def total_weighted_sse(clusters):
    'calculate the total SSE of all clusters'

    sse = 0
    for cluster in clusters:
        weight = cluster.get_weight()
        sse += weight*cluster.get_sse()
    return sse

def stat_clusters(clusters):
    'print the info of each cluster'

    i = 0; total = 0
    for cluster in clusters:
        total+=cluster.get_num()

    print "stat info of clusters: "
    for cluster in clusters:
        cluster.cal_weight(total)
        cluster.cal_sse()
        print "cluster "+str(i)+" --> num of points: "+str(cluster.get_num())+\
              " weight: "+str(cluster.get_weight())+ " sse: "+str(cluster.get_sse())
        i+=1
    print "total number of points: "+str(total)
    tsse = total_weighted_sse(clusters)
    print "total weighted sse: "+str(tsse)

def kmeans(points,K):
    '''
    The process of K-Means clustering
    @points: the point list
    @K: the number of clusters to be generated
    
    Note:
    the variable "repeat" defines the number of iterations to stop the clustering process
    other stop condition can be setting a threshold for SSE, which, however is not required by the project     
    '''
    repeat = 1000
    clusters = init_clusters(points,K)
    for r in range(repeat):
        refresh_points(clusters)
        for point in points:
            candidate = ''
            dismin = 10000000
            for cluster in clusters:
                cent = cluster.get_cent()
                dis = distance(point,cent)
                if dis < dismin:
                    dismin = dis
                    candidate = cluster # select the cluster as candidate
            candidate.add_point(point) # add point to the candidate cluster
        refresh_cents(clusters)
    return clusters

if __name__ == "__main__":

    filename='./clusterdata.csv'
    points=init_points(filename)

    print ""
    print "K-Means clustering with different K values begins ... "

    for K in range(3,9): # test K-Means with different K values
        print ""
        print "K: "+str(K)
        clusters = kmeans(points, K)
        stat_clusters(clusters)
    
    print ""
    print "K-Means clustering with different K values ends ... "
    print ""
