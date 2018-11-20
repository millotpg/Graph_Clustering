from sequential.read_edges import ReadEdges
from sequential.eigen import Eigen
from sequential.plot import GraphPlotter

class RunClustering():
    def __init__(self, edge_file):
        self.edge_file = edge_file

    def start(self):
        # Read the edges
        x = ReadEdges(self.edge_file)
        
        # Generate the laplacian Matrix
        x.generate_matricies()
        
        # Calculate it's eigenvectors
        eig = Eigen(x.lap_mat)

        # # Get the top 2 eigen vectors (based on eigen values)
        lap_coords = eig.get_top_eigenvectors(2)
        
        # # Plot the coordinates
        grph = GraphPlotter(x.node_ids, lap_coords.transpose(), None)
        grph.plot_2d()
