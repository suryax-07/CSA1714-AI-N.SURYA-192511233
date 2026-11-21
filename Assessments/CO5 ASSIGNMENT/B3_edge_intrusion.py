
import random
import time
import statistics
import math

def create_data():
    random.seed(23)
    data = []

    for i in range(1000):
        if i % 2 == 0:
            x = [random.randint(0,2), 0,
                 random.randint(10,500)]
            label = 0
        else:
            x = [random.randint(3,10),
                 random.randint(1,5),
                 random.randint(500,2000)]
            label = 1

        data.append((x,label))

    random.shuffle(data)
    return data

def train(data):
    groups = {0:[], 1:[]}

    for x,y in data:
        groups[y].append(x)

    centers = {}

    for label, values in groups.items():
        centers[label] = [
            sum(row[i] for row in values)/len(values)
            for i in range(3)
        ]

    return centers

def predict(x, centers):
    distances = {}

    for label, center in centers.items():
        distances[label] = sum(
            (a-b)**2 for a,b in zip(x,center)
        )

    return min(distances, key=distances.get)

def main():
    print("NETWORK INTRUSION DETECTION")

    data = create_data()

    train_data = data[:700]
    test_data = data[700:]

    full_model = train(train_data)

    edge_model = {
        label: [round(v/10)*10 for v in values]
        for label, values in full_model.items()
    }

    actual = [y for x,y in test_data]

    for name, model in [
        ("Full model", full_model),
        ("Edge model", edge_model)
    ]:
        predicted = [
            predict(x,model) for x,y in test_data
        ]

        correct = sum(
            a == b for a,b in zip(actual,predicted)
        )

        print("\\n", name)
        print("Accuracy:", round(correct/len(actual)*100,2), "%")

        tp = sum(a==1 and b==1 for a,b in zip(actual,predicted))
        tn = sum(a==0 and b==0 for a,b in zip(actual,predicted))
        fp = sum(a==0 and b==1 for a,b in zip(actual,predicted))
        fn = sum(a==1 and b==0 for a,b in zip(actual,predicted))

        precision = tp/(tp+fp) if tp+fp else 0
        recall = tp/(tp+fn) if tp+fn else 0
        f1 = 2*precision*recall/(precision+recall) if precision+recall else 0

        print("Precision:", round(precision,3))
        print("Recall:", round(recall,3))
        print("F1 Score:", round(f1,3))
        print("Confusion Matrix:", [[tn,fp],[fn,tp]])

    times = []

    for x,y in test_data:
        start = time.perf_counter()
        predict(x,edge_model)
        times.append((time.perf_counter()-start)*1000)

    mean = statistics.mean(times)
    p95 = sorted(times)[int(.95*(len(times)-1))]

    print("\\nEDGE PERFORMANCE")
    print("Mean latency:", round(mean,5), "ms")
    print("P95 latency:", round(p95,5), "ms")
    print("Throughput:", round(1000/mean,2), "samples/sec")
    print("50 ms budget met:", p95 < 50)

if __name__ == "__main__":
    main()
