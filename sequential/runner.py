from sequential.read_edges import ReadEdges
from sequential.eigen import Eigen
from sequential.plot import GraphPlotter
from sequential.cluster import Cluster
from timeit import default_timer as timer

class RunClustering():
    def __init__(self, edge_file, clusters, dimension, plot_desired):
        self.edge_file = edge_file
        self.no_of_clusters = clusters
        self.dimension = dimension
        self.plot_desired = plot_desired

    def start_timed(self):
        # Read the edges
        start = timer()
        edges = ReadEdges(self.edge_file)
        end = timer()
        t1 = end - start
        print('Time to read the edge file: %0.4fs' % t1)
        
        # Generate the laplacian Matrix
        start = timer()
        edges.generate_matricies()
        end = timer()
        t2 = end - start
        print('Time to generate the matrices: %0.4fs' % t2)

        # Calculate it's eigenvectors
        start = timer()
        eig = Eigen(edges.lap_mat)
        end = timer()
        t3 = end - start
        print('Time to generate eigenvalues and eigenvectors: %0.4fs' % t3)

        # Get the top 2 eigen vectors (based on eigen values)
        lap_coords = eig.get_top_eigenvectors(self.dimension).transpose()

        # Cluster the data points
        start = timer()
        cluster = Cluster(lap_coords, edges.node_ids, self.no_of_clusters)
        (data_frame, centroids, labels) = cluster.cluster_data()
        end = timer()
        t4 = end - start
        print('Time to cluster data: %0.4fs' % t4)

        # Plot the coordinates
        if(self.plot_desired):
            grph = GraphPlotter(edges.node_ids, lap_coords, None)
            grph.plot_2d_unclustered()
            grph.plot_2d_clustered(labels, centroids, data_frame)

        data_frame['labels'] = labels
        data_frame.to_csv(self.edge_file+".clustered.csv")
    
    def start(self):
        # Read the edges
        edges = ReadEdges(self.edge_file)
        
        # Generate the laplacian Matrix
        edges.generate_matricies()

        # Calculate it's eigenvectors
        eig = Eigen(edges.lap_mat)

        # Get the top 2 eigen vectors (based on eigen values)
        lap_coords = eig.get_top_eigenvectors(self.dimension).transpose()

        cluster = Cluster(lap_coords, edges.node_ids, self.no_of_clusters)
        (data_frame, centroids, labels) = cluster.cluster_data()

        # Plot the coordinates
        if(self.plot_desired):
            grph = GraphPlotter(edges.node_ids, lap_coords, None)
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