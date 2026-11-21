
from sklearn.cluster import KMeans

x = [[1, 2], [2, 3], [3, 3],
     [8, 8], [9, 8], [8, 9]]

model = KMeans(n_clusters=2, random_state=0, n_init=10)
model.fit(x)

print("Cluster Labels:")
print(model.labels_)

print("Cluster Centers:")
print(model.cluster_centers_)
