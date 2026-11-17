
import numpy as np
from sklearn.linear_model import LinearRegression

x = np.array([[1], [2], [3], [4], [5]])
y = np.array([10, 20, 30, 40, 50])

model = LinearRegression()
model.fit(x, y)

prediction = model.predict([[6]])

print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)
print("Predicted value:", prediction[0])
