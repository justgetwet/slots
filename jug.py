import numpy as np
import matplotlib.pyplot as plt
from numba import njit
from scipy.stats import binom

#@njit("i8[:](i8,i8,i8)", cache=True)
def imJuggler(s, trial, game):

  s = s - 1
  rnd = np.random.rand(trial, game)
  ret = np.empty(trial, dtype=np.int64)

  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg

  q  = np.reciprocal(p)
  nb = 1 - np.sum(q, axis=0)[s] # no bonus
  h = np.hstack((np.array([nb]), q[:,s]))
  b = np.searchsorted(h.cumsum(), rnd)

  for i in range(trial):
    ret[i] = np.count_nonzero(b[i]==2)
  # ret = [np.count_nonzero(x==2) for x in b]

  return ret

def reg_binomial(s):
  np.random.seed(0)
  s = s - 1
  trial = 10000
  game = 2000
  rb = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0
  p = np.reciprocal(rb)
  ret = np.random.binomial(game, p[s], trial)
  return ret

def spam(n):
  game = 8000
  rb = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0
  p = np.reciprocal(rb)
  pmf = []
  for s in [1,2,3,4,5,6]:
    s = s - 1
    pmf.append(binom.pmf(n, game, p[s]))
  
  return pmf 

if __name__ == '__main__':

  pmf = spam(30)
  # a = imJuggler(s=1, trial=10000, game=2000)
  # b = imJuggler(s=6, trial=100000, game=2000)
  #c = reg_binomial(1)
  # plt.hist([a, c], bins=16, label=["a", "c"])
  # plt.hist(c)
  plt.bar([1,2,3,4,5,6], pmf)
  # plt.legend()
  plt.show()