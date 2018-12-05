#include <stdio.h>
#include <stdlib.h>
#include <set>

#include <math.h>
#include <cuda_runtime.h>
#include "cublas_v2.h"
#include <cusolverDn.h>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <iterator>
#include <chrono>

struct MatrixData
{
	std::vector<std::vector<int>> edges;
	std::set<int> uniqueNodes;
};

// Function Prototypes
std::vector<std::vector<float>> eigen(std::vector<std::vector<int>>);
int doCudaStuff(std::vector<std::vector<int>>);
std::vector<std::vector<int>> createLaplacian(MatrixData);
MatrixData readEdges(std::string);
void writeCoordToFile(std::vector<std::vector<float>>, int, std::string);

// Entry point
int main(int argc, char **argv) {
	char * matrixPath = argv[1];
	int dim = std::stoi((std::string)argv[2]);

	auto start_1 = std::chrono::high_resolution_clock::now();
	MatrixData matrix_data = readEdges(matrixPath);
	auto stop_1 = std::chrono::high_resolution_clock::now();
	auto duration_1 = std::chrono::duration_cast<std::chrono::microseconds>(stop_1 - start_1);
	printf("Time to read file: %0.5f \n", (float)duration_1.count() / 1000000);

	auto start_2 = std::chrono::high_resolution_clock::now();
	std::vector<std::vector<int>> laplacian_matrix = createLaplacian(matrix_data);
	auto stop_2 = std::chrono::high_resolution_clock::now();
	auto duration_2 = std::chrono::duration_cast<std::chrono::microseconds>(stop_2 - start_2);
	printf("Time to generate matricies: %0.5f \n", (float)duration_2.count() / 1000000);

	auto start_3 = std::chrono::high_resolution_clock::now();
	std::vector<std::vector<float>> coordinates = eigen(laplacian_matrix);
	auto stop_3 = std::chrono::high_resolution_clock::now();
	auto duration_3 = std::chrono::duration_cast<std::chrono::microseconds>(stop_3 - start_3);
	printf("Time to generate Eigen: %0.5f \n", (float)duration_3.count() / 1000000);

	std::string outfilename = matrixPath;
	outfilename.append(".eigen");
	auto start_4 = std::chrono::high_resolution_clock::now();
	writeCoordToFile(coordinates, dim, outfilename);
	auto stop_4 = std::chrono::high_resolution_clock::now();
	auto duration_4 = std::chrono::duration_cast<std::chrono::microseconds>(stop_4 - start_4);
	printf("Time to write coords to File: %0.5f \n", (float)duration_4.count() / 1000000);
}

MatrixData readEdges(std::string edgePath) {
	std::vector<std::vector<int>> edges;
	std::vector<int> edgeset_1;
	std::vector<int> edgeset_2;
	std::set<int> unique_nodes;
	std::ifstream edgeFile(edgePath);
	std::string line;
	bool isLeadingEdge = true;
	if (edgeFile.is_open()) {
		while (std::getline(edgeFile, line)) {
			std::stringstream lineStream(line);
			int value;
			while (lineStream >> value) {
				unique_nodes.insert(value);
				if (isLeadingEdge) {
					edgeset_1.push_back(value);
					isLeadingEdge = false;
				}
				else {
					edgeset_2.push_back(value);
					isLeadingEdge = true;
				}
			}
		}
		edgeFile.close();
	}
	edges.push_back(edgeset_1);
	edges.push_back(edgeset_2);
	MatrixData returnData;
	returnData.edges = edges;
	returnData.uniqueNodes = unique_nodes;
	return returnData;
}

std::vector<std::vector<int>> createLaplacian(MatrixData input_matrix)
{
	// Create an empty matrix
	std::vector<int> mat_dim;
	mat_dim.push_back(input_matrix.uniqueNodes.size());

	std::vector<int> matrix(input_matrix.uniqueNodes.size()*input_matrix.uniqueNodes.size());

	std::vector<int> edgeset_1 = input_matrix.edges[0];
	std::vector<int> edgeset_2 = input_matrix.edges[1];

	// Create the laplacian edges
	for (int i = 0; i < edgeset_1.size(); ++i) {
		matrix[(edgeset_1[i] - 1) * mat_dim[0] + (edgeset_2[i] - 1)] = -1;
		matrix[(edgeset_2[i] - 1) * mat_dim[0] + (edgeset_1[i] - 1)] = -1;
	}

	// Create the laplacian degrees (diagonal)
	int degree_index = 0;
	int curSum = 0;
	for (int i = 0; i < matrix.size(); i = i + mat_dim[0]) {
		for (int k = 0; k < mat_dim[0]; k++)
		{
			if (matrix[i + k] == -1) {
				curSum++;
			}
		}
		matrix[i + degree_index] = curSum;
		degree_index++;
		curSum = 0;
	}

	std::vector<std::vector<int>> matrix_data;
	matrix_data.push_back(mat_dim);
	matrix_data.push_back(matrix);
	return matrix_data;
}

std::vector<std::vector<float>> eigen(std::vector<std::vector<int>> matrix_data)
{
	cusolverDnHandle_t cusolverH;
	cusolverStatus_t cusolver_status = CUSOLVER_STATUS_SUCCESS;
	cudaError_t cudaStat = cudaSuccess;

	std::vector<int> mat_dim = matrix_data[0];
	std::vector<int> mat = matrix_data[1];

	int m = mat_dim[0];
	int lda = mat_dim[0];

	float *A; // mxm matrix
	float *V; // mxm matrix of eigenvectors
	float *W; // m- vector of eigenvalues

			  // prepare memory on the host
	A = (float *)malloc(lda*m * sizeof(float));
	V = (float *)malloc(lda*m * sizeof(float));
	W = (float *)malloc(m * sizeof(float));

	// define array to be all elements from the matrix
	for (int i = 0; i < lda*m; i++) A[i] = (float)mat[i]; //TODO is the cast safe?

														  // declare arrays on the device
	float *d_A; // mxm matrix A on the device
	float *d_W; // m- vector of eigenvalues on the device
	int *devInfo; // info on the device
	float *d_work; // workspace on the device
	int lwork = 0; // workspace size
	int info_gpu = 0; // info copied from device to host

					  // create cusolver handle
	cusolver_status = cusolverDnCreate(&cusolverH);

	// prepare memory on the device
	cudaStat = cudaMalloc((void **)& d_A, sizeof(float)* lda*m);
	cudaStat = cudaMalloc((void **)& d_W, sizeof(float)*m);
	cudaStat = cudaMalloc((void **)& devInfo, sizeof(int));
	cudaStat = cudaMemcpy(d_A, A, sizeof(float)* lda*m, cudaMemcpyHostToDevice); // copy A- >d_A 

																				 // compute eigenvalues and eigenvectors
	cusolverEigMode_t jobz = CUSOLVER_EIG_MODE_VECTOR;

	// use lower left triangle of the matrix
	cublasFillMode_t uplo = CUBLAS_FILL_MODE_LOWER;

	// compute buffer size and prepare workspace
	cusolver_status = cusolverDnSsyevd_bufferSize(cusolverH, jobz, uplo, m, d_A, lda, d_W, &lwork);
	cudaStat = cudaMalloc((void **)& d_work, sizeof(float)* lwork);

	// compute the eigenvalues and eigenvectors for a symmetric ,
	// real mxm matrix ( only the lower left triangle af A is used )
	cusolver_status = cusolverDnSsyevd(cusolverH, jobz, uplo, m,
		d_A, lda, d_W, d_work, lwork, devInfo);
	cudaStat = cudaDeviceSynchronize();

	cudaStat = cudaMemcpy(W, d_W, sizeof(float)*m, cudaMemcpyDeviceToHost); // copy d_W - >W
	cudaStat = cudaMemcpy(V, d_A, sizeof(float)* lda*m, cudaMemcpyDeviceToHost); // copy d_A - >V
	cudaStat = cudaMemcpy(&info_gpu, devInfo, sizeof(int), cudaMemcpyDeviceToHost); // copy devInfo - > info_gpu

	int counter = 0;
	float curvec = V[counter];
	std::vector<std::vector<float>> coordinates;
	std::vector<float> curDim;
	while (counter != m * m) {
		curDim.push_back(V[counter]);
		++counter;
		if (counter % m == 0) {
			coordinates.push_back(curDim);
			curDim.clear();
		}
	}

	// free memory
	cudaFree(d_A);
	cudaFree(d_W);
	cudaFree(devInfo);
	cudaFree(d_work);
	cusolverDnDestroy(cusolverH);
	cudaDeviceReset();
	if (cusolver_status == 0)
	{
		return coordinates;
	}
	else {
		printf("Error computing Eigen values: \n");
		printf("CuSolver returned %i ", cusolver_status);
		exit(1);
	}
}

void writeCoordToFile(std::vector<std::vector<float>> coordinates, int dim, std::string outfilename) {
	std::ofstream out_file;
	out_file.open(outfilename);
	
	for (int i = 1; i <= dim; ++i) {
		for (int k = 0; k < coordinates[i].size(); k++) {
			out_file << std::fixed << std::setprecision(8) << coordinates[i][k] << " ";
			//printf("%0.12f ", coordinates[i][k]);
		}
		out_file << "\n";
		//printf("\n");
	}
	out_file.close();
}