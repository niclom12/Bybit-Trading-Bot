
import numpy as np
from math import sqrt


#data has to be rearanged from least recent at index 0 
def raw_hma(data, period):
    out = 2*wma(data, round(period/2)) - wma(data, period)
    return out
    
def wma(data, period):
    weights = list(range(1, period+1)) 
    wma = sum(weight*price for weight, price in zip(weights, data[-period:])) / sum(weights)
    return wma

def create_data_set(data):
    data_new = create_arrays(data, 55, 12)
    return [raw_hma(np.flip(array), 55) for array in data_new]

def create_arrays(data, x, rang):
    return [data[i:i+x] for i in range(rang)]


def Hulls(array):
    arrays = create_arrays(array, round(sqrt(55)), 5)
    return np.array([wma(np.flip(array), round(sqrt(55))) for array in arrays]).astype(float)

def logic(data):
    raw_hma = create_data_set(data)
    hull = Hulls(raw_hma)
    hul1 = hull[0] - hull[2]
    hul2 = hull[1] - hull[3]
    if ((hul1 >= 0) and (hul2 < 0)):
        print("Buy")
        return "Buy"
    elif ((hul1 < 0) and (hul2 >= 0)):
        print("Sell")
        return "Sell"
    elif(hul1 >= 0):
        print("Bullish")
        return
    else:
        print("Bearish")
        return


