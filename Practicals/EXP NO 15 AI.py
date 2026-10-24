
data = [
    ["Sunny", "No"],
    ["Sunny", "No"],
    ["Rainy", "Yes"],
    ["Rainy", "Yes"],
    ["Cloudy", "Yes"]
]

print("Weather Prediction using Decision Tree")

weather = input("Enter weather (Sunny/Rainy/Cloudy): ")

if weather == "Sunny":
    result = "No"
elif weather == "Rainy":
    result = "Yes"
elif weather == "Cloudy":
    result = "Yes"
else:
    result = "Invalid input"

print("Play outside:", result)
