# Graph Clustering - A tool for visualizing and clustering graphes
## Installation
This tool was written for python3. After cloning the repository, run: 

`pip install -r requirements.txt`

Also make sure that tkinter is installed for displaying the plots. This can be done with:

`sudo apt-get install python3-tk`


# Structure
This graph clustering tool contains two packages. A Sequential and Parallel package. Within each package, there is a Runner class (runner.py) that will execute graph clustering with given parameters (edges file, clustering method, min accepted silhouette coefficiet etc.)

## Sequential
Contains all the sequential methods to read an edge file, generate the graph matricies and cluster the graph. Used as a comparison to indicate parallel speed up
 - *read_edges.py* - read an edge file and generates the graph matricies
 - *eigen.py* - takes a matrix as input and generates the eigen values and eigen vectors
 - *cluster.py* - takes vertex ids and their associated *n* points representing that vertex in *n* dimensional space and clusters them
 - *silhouette.py* - calculates the efficiency of the clustering
 - *plot.py* - if the graph is mapped to the 2nd or 3rd dimension, plot the graph using matplotlib and show the clusters (in different colors)
 - *runner.py* - Takes parameters and runs the scripts 

## Parallel
Same as the sequential package except the following scripts execute in parallel for a performance increase
 - *read_edges.py*
 - *eigen.py*
 - *cluster.py*
 - *silhouette.py*

## Runner.py (in /sequential and /parallel)
Class file that will cluster an edge file. Takes the following configuration parameters
 - Input edge file
 - Clustering method (Initially K-Means)
 - Minimum accepted silhouette - measures the effectiveness of the clustering. Defaults to accepting first one
 - Desired dimension - dimension to map the graph into
 - Plot desired - if the dimension is 2 or 3, use matplot lib to generate a plot of the clustered graph and the non clustered graph

 ## Clustering
 Currently, up to 5 clusters can be made and plotted. 

# graph_cluster usage
Executable file that will take command line input and execute runner.py

Usage:

    edgefile              edge file representation of the input graph
    -h                    display help information
    -c (--clusters)       number of clusters (defaults to 2) 
    -d                    dimension to map the graph into (defaults to 2)
    -g (--generate-plot)  will generate a plot (defaults to true)
                          (optional, defaults to false and only works if -d = 2 or 3)
    -p (--parallel)       run graph_clustering in parallel (optional, defaults to true)
    -s (--sequential)     run graph_clustering sequentially (optional, defaults to true)
    -t (--time)           display time information on clustering (optional, defaults to true)


## Examples
Generate a graph clustering using the lattice data. Create two clusters in two dimensions sequentially and time the program:

`./graph_clustering graph_data/lattice.edges -c 2 -d 2 -s -g -t`


## Future Expansion
Add an option for a minimum accepted silhouette value

    --min-sil    minimum accepted silhouette (defaults to accept first)

