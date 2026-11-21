
import numpy as np

ratings = np.array([
    [5, 4, 0, 0],
    [4, 5, 0, 0],
    [0, 0, 5, 4],
    [0, 0, 4, 5]
])

user1 = ratings[0]
similarity = []

for i in range(len(ratings)):
    if i == 0:
        similarity.append(-1)
    else:
        sim = np.dot(user1, ratings[i]) / (
            np.linalg.norm(user1) * np.linalg.norm(ratings[i])
        )
        similarity.append(sim)

best_user = np.argmax(similarity)

for i in range(ratings.shape[1]):
    if ratings[0][i] == 0:
        print("Recommended Item:", i + 1)
        break
