import numpy
from queue import PriorityQueue as PQ
from numpy import linalg
try:
    # Currently only used for testing
    from sequential.read_edges import ReadEdges, TEST_DATA
except:
    pass

class Eigen():
    """
    Calculates the eigen vectors and values of a given matrix
    *NOTE the eigenvectors are normalized so they might look off a bit
    TODO: maybe fix that?

    Args:
        input_matrix(numpy.array): nxn Input matrix
    
    Attrs:
        self.matrix(numpy.array): nxn input matrix
        self.eigen_values(numpy.array): n eigen values in an nx1 array
        self.eigen_vectors(numpy.array): n nx1 eigen vectors in an array
    """
    def __init__(self, input_matrix):
        self.matrix = input_matrix
        self.mat_size = input_matrix.shape
        self.eigen_values, self.eigen_vectors = linalg.eig(input_matrix)

    def get_eigenvalues(self):
        return self.eigen_values
    
    def get_eigenvectors(self):
        return self.eigen_vectors
    
    def get_top_eigenvectors(self, n):
        """
        Returns the top n eigenvectors that correspond to the 
        largest eigen values

        Args:
            n (int): number of eigenvectors to return
        
        returns:
            top_n_vectors (numpy.array(numpy.array)): array of eigen vectors  
        """
        if n > self.mat_size[0]:
            raise ValueError("n cannot be greater than number of eigen values")
        top_n_vectors = numpy.zeros((self.mat_size[0], n))
        index_queue = PQ()
        for i in range(self.eigen_values.shape[0]):
            index_queue.put((self.eigen_values[i], i))
        index_queue.queue.sort()
        index_queue.queue.reverse()
        for i in range(n):
            cur_top = index_queue.get()
            top_n_vectors[:, i] = self.eigen_vectors[:, cur_top[1]]
        return top_n_vectors

def main():
    pass
    # test_mat = numpy.array([[6, -1],[2,3]])
    # eig = Eigen(test_mat)
    # print(eig.get_eigenvalues())
    # print(eig.get_eigenvectors())
    # print(eig.get_top_eigenvectors(1))

if __name__ == "__main__":
    main()