from sklearn.cluster import KMeans
import pandas as pd

class Cluster:
    def __init__(self, data_pts, data_ids, number_of_clusters):
        self.data_pts = data_pts
        self.data_ids = data_ids
        self.number_of_clusters = number_of_clusters

    def cluster_data(self):
        dimension_columns = []
        for i in range(self.data_pts.shape[1]):
            dimension_columns.append('d'+str(i+1))
        data_frame = pd.DataFrame(
            data=self.data_pts[:, :],
            index=self.data_ids, #Check this?
            columns=dimension_columns
        )
        kmeans = KMeans(n_clusters=self.number_of_clusters)
        kmeans.fit(data_frame)
        labels = kmeans.predict(data_frame)
        centroids = kmeans.cluster_centers_
        return (data_frame, centroids, labels)