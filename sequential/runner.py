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
        print('Time to read the edge file: %0.4fs' % (end-start))
        
        # Generate the laplacian Matrix
        start = timer()
        edges.generate_matricies()
        end = timer()
        print('Time to generate the matrices: %0.4fs' % (end-start))

        # Calculate it's eigenvectors
        start = timer()
        eig = Eigen(edges.lap_mat)
        end = timer()
        print('Time to generate eigenvalues and eigenvectors: %0.4fs' % (end-start))

        # Get the top 2 eigen vectors (based on eigen values)
        lap_coords = eig.get_top_eigenvectors(self.dimension).transpose()

        # Cluster the data points
        start = timer()
        cluster = Cluster(lap_coords, edges.node_ids, self.no_of_clusters)
        cluster.cluster_data()
        end = timer()
        print('Time to cluster data: %0.4fs' % (end-start))

        # Plot the coordinates
        if(self.plot_desired):
            grph = GraphPlotter(edges.node_ids, lap_coords, None)
            grph.plot_2d()
    
    def start(self):
        # Read the edges
        edges = ReadEdges(self.edge_file)
        
        # Generate the laplacian Matrix
        edges.generate_matricies()

        # Calculate it's eigenvectors
        eig = Eigen(edges.lap_mat)

        # Get the top 2 eigen vectors (based on eigen values)
        lap_coords = eig.get_top_eigenvectors(2)

        cluster = Cluster(lap_coords, edges.node_ids, self.no_of_clusters)

        # Plot the coordinates
        if(self.plot_desired):
            grph = GraphPlotter(edges.node_ids, lap_coords.transpose(), None)
            grph.plot_2d()

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