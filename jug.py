import numpy as np
import matplotlib.pyplot as plt
from numba import njit

# @njit("i8[:](i8,i8,i8)", cache=True)
def imJuggler(s, trial, game):

  s = s-1

  rnd = np.random.rand(trial, game)

  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg

  q = np.reciprocal(p)
  lose = 1 - np.sum(q, axis=0)[s]
  bonus_p = np.hstack((np.array([lose]), q[:,s]))
  bonus = np.searchsorted(bonus_p.cumsum(), rnd)

  ret = [np.count_nonzero(b==2) for b in bonus]

  return ret



if __name__ == '__main__':

  a = imJuggler(s=1, trial=10000, game=2000)
  b = imJuggler(s=6, trial=10000, game=2000)

  plt.hist([a, b], bins=16, label=['1', '6'])
  plt.show()