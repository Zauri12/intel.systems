import numpy as np
def corell(x, y):
    otvet = 0
    k = 0
    k1 = 0
    srx = np.mean(x)
    sry = np.mean(y)
    x1 = []
    y1 = []
    x2 = 0
    y2 = 0
    for i in range(len(x)):
        x1.append(x[i] - srx)
        y1.append(y[i] - sry)
    for i in range(len(x)):
        
        k += (x1[i] * y1[i])
    for i in range(len(x)):
        x2 += x1[i]**2
        y2 += y1[i]**2
    otvet = k/(x2*y2)**0.5
    return(otvet)