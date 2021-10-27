import matplotlib.pyplot as plt
import numpy as np

def monte_pi(N):
  x = np.random.rand(N)
  y = np.random.rand(N)
  i = np.sum(x**2+y**2 < 1.0)
  pi = 4.0*i/N 
  print(pi)

  return x, y


if __name__ == '__main__':

  fig = plt.figure(dpi=100, figsize=(4, 4))
  ax = fig.gca()
  ax.set_title("monte")
  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)

  points = monte_pi(10000000)
  # x, y = points
  # for px, py in zip(x, y):
  #   if px**2+py**2 < 1.0:
  #     ax.plot(px, py, ".", color="magenta")

  # plt.show()