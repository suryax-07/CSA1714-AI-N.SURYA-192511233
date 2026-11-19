
from sklearn.svm import SVC

x = [[1, 2], [2, 3], [3, 3], [6, 7], [7, 8], [8, 8]]
y = [0, 0, 0, 1, 1, 1]

model = SVC(kernel='linear')
model.fit(x, y)

prediction = model.predict([[5, 6]])

print("Predicted Class:", prediction[0])
