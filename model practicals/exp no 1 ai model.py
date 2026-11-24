
def fuzzy_temperature(temp):
    if temp <= 20:
        cold = 1
    elif temp <= 30:
        cold = (30 - temp) / 10
    else:
        cold = 0

    if 20 < temp < 30:
        warm = (temp - 20) / 10
    elif 30 <= temp <= 35:
        warm = 1
    elif 35 < temp < 40:
        warm = (40 - temp) / 5
    else:
        warm = 0

    if temp <= 30:
        hot = 0
    elif temp < 40:
        hot = (temp - 30) / 10
    else:
        hot = 1

    if cold >= warm and cold >= hot:
        speed = "Low"
    elif warm >= hot:
        speed = "Medium"
    else:
        speed = "High"

    print("Temperature:", temp)
    print("Fan Speed:", speed)


temp = float(input("Enter temperature: "))
fuzzy_temperature(temp)
