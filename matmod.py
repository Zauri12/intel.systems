#ЧАСТЬ 1

# №1
import numpy as np
np.ones((2, 3, 4))

# №2
np.full((8, 8), 42)

# №3
np.random.randint(0, 101, (1, 8))

# №4
np.zeros((2, 3)).T

# №5
a = np.ones((2, 3))
b = np.ones((2, 3))
a + b

# №6
def mult1(a = np.array):
  b = a.tolist()
  c = b[0] + b[1]
  d = max(c) - min(c)
  return d



print(mult1(np.array([[1, 2, 3],
                     [4, 5, 6]])))

# №7
def mult2(a):
  s = a @ a.T
  return np.linalg.inv(s)
print(mult2(np.array([[1, 2, 3],
                     [4, 5, 6]])))

# №8
import matplotlib.pyplot as plt
x = np.arange(-10, 11)
y = x * x * x/12 + x * (x-15) - 72
plt.plot(x, y)
plt.show()

# №9
import matplotlib.pyplot as plt
x = np.arange(-10, 11, 0.1)
y = x * x * x/12 + x * (x-15) - 72
plt.plot(x, y)
plt.show()



#ЧАСТЬ 2

# №1
np.ones((5, 2), dtype = int)

# №2
import numpy as np
a = np.ones((2, 3))
b = np.ones((2, 3))
a @ b.T

# №3
a = np.random.randint(0, 10, 20)
x = a[a > 5]
x

# №4
a = np.random.randint(0, 10, (3, 5))
b = np.where(a < 5, 0, 1)
b

# №5
np.ones((4, 3))

# №6
import numpy as np
a = np.random.randint(1, 10, (4, 4))
b = np.random.randint(1, 10, (4, 4))
x = np.random.randint(1, 5, 4)
y = 1/25 * a @ a.T @ x.T + b @ x.T + 5
y


# №7
def f3(x):
  y = x*x*np.sin(x/300) + 300*x
  return y
def fu(a, b):
  for i in range(a, b):
    if f3(i) == 0:
      plt.plot(i, f3(i), 'gs')
fu(-10, 10)

# №8
k = 0
for i in range(1001):

  a = np.random.randint(-5, 5, (5, 5))
  b = np.random.randint(-5, 5, (5, 5))
  ab = a @ b
  ba = b @ a
  c = 0
  for m in range(5):
    for n in range(5):
      if ab[m, n] == ba[m, n]:
        c += 1
        if c == 25:
          k += 1

k





