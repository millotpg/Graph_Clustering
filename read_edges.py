from numpy import matlib as mat

# For testing - saves time to type in
FB_DATA = 'graph_data/fb_amherst.edges'
ENZYME_DATA = 'graph_data/enzymes_g10.edges'
TEST_DATA = 'graph_data/test.edges'

class ReadEdges():
    """
    Class for reading an edge file and processing into matricies

    args:
        filename (str): filename containing the edges
    
    attrs:
        edgeset_1 (arr(int)): set of verticies that connect to edgeset_2
        edgeset_2 (arr(int)): set of verticies that connect to edgeset_1
        adjacency (numpy.matrix): adjacency matrix of the graph
        degree (numpy.matrix): degree matrix of the graph
        laplacian (numpy.matrix): laplacian matrix of the graph
    """
    def __init__(self, filename):
        """
        Process the edges into two arrays of corresponding verticies
        ex.) [1,2,3] [4,1,4]
        1-4
        2-1
        4-3 
        """
        self.edgeset_1 = []
        self.edgeset_2 = []
        with open(filename, 'r') as edge_fl:
            for line in edge_fl:
                try:
                    # some edge files have the first line list stats - can ignore
                    x, y = line.split(' ')
                    self.edgeset_1.append(x.strip('\n'))
                    self.edgeset_2.append(y.strip('\n'))
                except ValueError:
                    pass
    
    def print_edges(self):
        """
        Prints the edges contained in edgeset_1 and edgeset_2
        """
        for index in range(0, len(self.edgeset_1)):
            print(self.edgeset_1[index] + ' ' + self.edgeset_2[index])

    def get_adjacency(self):
        """
        Creates an adjacency matrix from edgesets
        * NOTE no. of unique edges in edgeset_1 might not be 
            the same as no. of unique edges in edgeset_2
        * NOTE the total number of unique verticies has to be
            obtained through the union of the two unique edgelists
        """
        unique_verticies = set.union(set(self.edgeset_1), set(self.edgeset_2))
        self.mat_dim = len(unique_verticies)
        self.adj_mat = mat.zeros((self.mat_dim, self.mat_dim))
        for edge_index in range(len(self.edgeset_1)):
            index_1 = int(self.edgeset_1[edge_index])-1
            index_2 = int(self.edgeset_2[edge_index])-1
            self.adj_mat[index_1, index_2] = 1
            self.adj_mat[index_2, index_1] = 1
        return self.adj_mat

    def get_degree(self):
        """
        Creates a Degree matrix from the adjacency matrix
        If the adjacency matrix has not yet been created,
            this method will create one
        """
        try:
            mat_dim = self.mat_dim
        except AttributeError:
            self.get_adjacency()
            mat_dim = self.mat_dim
        self.deg_mat = mat.zeros((self.mat_dim, self.mat_dim))
        for i in range(mat_dim):
            self.deg_mat[i, i] = self.adj_mat[:, i].sum()
        return self.deg_mat

    def get_laplacian(self):
        """
        Creates a laplacian matrix from the adjacency and Degree matrix
        TODO make this more efficent by only computing top right corner
        """
        try:
            adj_mat = self.adj_mat
        except AttributeError:
            adj_mat = self.get_adjacency()
        try:
            deg_mat = self.deg_mat
        except AttributeError:
            deg_mat = self.get_degree()
        self.lap_mat = mat.zeros((self.mat_dim, self.mat_dim))
        for row in range(self.mat_dim):
            for col in range(row, self.mat_dim):
                self.lap_mat[row, col] = deg_mat[row, col] - adj_mat[row, col]
                self.lap_mat[col, row] = deg_mat[row, col] - adj_mat[row, col]
        return self.lap_mat

def main():
    x = ReadEdges(TEST_DATA)
    print(x.get_adjacency())
    print('-------------------')
    print(x.get_degree())
    print('-------------------')
    print(x.get_laplacian())


if __name__ == "__main__":
    main()