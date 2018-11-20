from sequential.runner import RunClustering

# import test data
from sequential.read_edges import TEST_DATA
from sequential.read_edges import ENZYME_DATA
from sequential.read_edges import FB_DATA

def main():
    runner = RunClustering(TEST_DATA)
    runner.start()

if __name__ == "__main__":
    main()