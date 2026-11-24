
inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
outputs = [0, 0, 0, 1]

w1 = 0
w2 = 0
bias = 0
lr = 0.1

for epoch in range(10):
    for i in range(4):
        x1, x2 = inputs[i]
        target = outputs[i]

        net = w1*x1 + w2*x2 + bias
        pred = 1 if net > 0 else 0

        error = target - pred

        w1 += lr * error * x1
        w2 += lr * error * x2
        bias += lr * error

    print("Iteration:", epoch + 1)
    print("Weights:", w1, w2, "Bias:", bias)

print("\nAND Gate Output:")
for x1, x2 in inputs:
    net = w1*x1 + w2*x2 + bias
    pred = 1 if net > 0 else 0
    print(x1, x2, "=", pred)
