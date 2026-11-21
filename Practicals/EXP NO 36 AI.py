
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

x = [[2, 4], [3, 5], [4, 6], [5, 8], [6, 9]]

scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

pca = PCA(n_components=1)
result = pca.fit_transform(x_scaled)

print("Original Data:")
print(x)

print("Reduced Data:")
print(result)
