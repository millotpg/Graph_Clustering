from sequential.eigen import Eigen
from sequential.plot import GraphPlotter
from sequential.cluster import Cluster
from timeit import default_timer as timer

import os
import subprocess
import numpy

class RunClustering():
    def __init__(self, edge_file, clusters, dimension, plot_desired):
        self.edge_file = edge_file
        self.no_of_clusters = clusters
        self.dimension = dimension
        self.plot_desired = plot_desired

    def start_timed(self):
        args = "parallelSpectral.exe " + self.edge_file + " " + str(self.dimension)
        subprocess.call(args)

        coords = []
        with open(self.edge_file+'.eigen', 'r') as eigenfl:
            for line in eigenfl:
                coords.append([float(x) for x in line.strip('\n').split(' ')[:-1]])
        
        node_ids = range(1, len(coords[0])+1)
        lap_coords = numpy.array(coords).transpose()
        os.remove(self.edge_file+'.eigen')

        start = timer()
        cluster = Cluster(lap_coords, node_ids, self.no_of_clusters)
        (data_frame, centroids, labels) = cluster.cluster_data()
        end = timer()
        t4 = end - start
        print('Time to cluster data: %0.4fs' % t4)

        # Plot the coordinates
        if(self.plot_desired):
            grph = GraphPlotter(node_ids, lap_coords, None)
            grph.plot_2d_unclustered()
            grph.plot_2d_clustered(labels, centroids, data_frame)
        
        data_frame['labels'] = labels
        data_frame.to_csv(self.edge_file+".clustered.csv")
    
    def start(self):
        FNULL = open(os.devnull, 'w')
        args = "parallelSpectral.exe " + self.edge_file + " " + str(self.dimension)
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

        coords = []
        with open(self.edge_file+'.eigen', 'r') as eigenfl:
            for line in eigenfl:
                coords.append([float(x) for x in line.strip('\n').split(' ')[:-1]])
        
        node_ids = range(1, len(coords[0])+1)
        lap_coords = numpy.array(coords).transpose()
        os.remove(self.edge_file+'.eigen')

        cluster = Cluster(lap_coords, node_ids, self.no_of_clusters)
        (data_frame, centroids, labels) = cluster.cluster_data()

        # Plot the coordinates
        if(self.plot_desired):
            grph = GraphPlotter(node_ids, lap_coords, None)
            grph.plot_2d_unclustered()
            grph.plot_2d_clustered(labels, centroids, data_frame)

        data_frame['labels'] = labels
        data_frame.to_csv(self.edge_file+".clustered.csv")

def print_matrix(mat_str, mat):
    """
    Prints a numpy matrix for debugging
    """
    print(mat_str)
    (rows, cols) = mat.shape
    for i in range(rows):
        for k in range(cols):
            print(int(mat[i, k]), end=' ')
        print()