
rooms = ["Dirty", "Clean"]
location = 0

while "Dirty" in rooms:
    print("Current Room:", chr(65 + location))
    print("Room Status:", rooms[location])

    if rooms[location] == "Dirty":
        rooms[location] = "Clean"
        print("Room cleaned")

    location = 1 - location

print("Final Status:", rooms)
print("Both rooms are clean")
