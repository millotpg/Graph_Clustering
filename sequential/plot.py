import matplotlib.pyplot as plt
import numpy as np

class GraphPlotter():
    """
    Plotter for graph data. Takes a list of vertex coordinates
    and edges and plots them in a 2 or 3 dimentional grid

    Args:
        vertex_ids (arr): ids of verticies from edge file
        vertex_coords (numpy.arr): coordinates of verticies
        edges (arr(tuples)): array of tuples containing connected edges
    """
    def __init__(self, vertex_ids, vertex_coords, edges):
        self.vertex_ids = vertex_ids
        self.vertex_coords = vertex_coords
        self.edges = edges
    
    def plot_2d_unclustered(self):
        """
        Plots the coordinates in a 2 dimensional space. No clusters
        """
        plt.plot(self.vertex_coords[:, 0], self.vertex_coords[:, 1], 'ro', [])
        for i in range(len(self.vertex_ids)):
            plt.annotate(
                str(self.vertex_ids[i]),
                xy = (self.vertex_coords[i, 0], self.vertex_coords[i, 1]),
            )
        plt.ylim(-0.6, 0.6)
        plt.xlim(-0.6, 0.6)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.title('Input Graph: Unclustered')
        plt.show()

    def plot_2d_clustered(self, labels, centroids, data_frame):
        """
        Plots the coordinates in a 2 dimensional space with colors representing the colors
        """
        colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'y', 5: 'k'}
        fig = plt.figure()
        colors = list(map(lambda x: colmap[x+1], labels))
        plt.scatter(data_frame['d1'], data_frame['d2'], color=colors, alpha=0.5)
        for i, centroid in enumerate(centroids):
            plt.scatter(*centroid, color=colmap[i+1])
        for i in range(len(self.vertex_ids)):
            plt.annotate(
                str(self.vertex_ids[i]),
                xy = (self.vertex_coords[i, 0], self.vertex_coords[i, 1]),
            )
        plt.ylim(-0.6, 0.6)
        plt.xlim(-0.6, 0.6)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.title('Input Graph: Clustered')
        plt.show()

def main():
    test_vertex_ids = [1,2,3,4]
    test_vertex_coords = np.array([[1,1], [2, 1], [1, 2], [2, 2]])
    gp = GraphPlotter(test_vertex_ids, test_vertex_coords, None)
    gp.plot_2d()
66
if __name__ == "__main__":
    main()