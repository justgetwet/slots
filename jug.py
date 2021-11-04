import numpy as np
import matplotlib.pyplot as plt
from numba import njit
from concurrent.futures import ProcessPoolExecutor
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

def im_binomial(s, trial, game):
  # np.random.seed(0)
  s = s - 1
  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  q = np.reciprocal(p)[1]

  return np.random.binomial(game, q[s], trial)

def im_pmf(n, game):
  
  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  q = np.reciprocal(p)[1]
  ret = [binom.pmf(n, game, q[s]) for s in range(6)]
  
  return ret 

def sim_pmf(n, game, settings):

  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  q = np.reciprocal(p)[1]
  pmfs = [binom.pmf(n, game, q[s-1]) for s in settings]
  for s, p in zip(settings, pmfs):
    print(s, round(p/sum(pmfs), 2))


def spam():
  pmf = im_pmf(15, 3000)
  for i, p in enumerate(pmf):
    print(i+1, round(p/sum(pmf), 2))

if __name__ == '__main__':

  trial = 100000
  game = 3000
  # with ProcessPoolExecutor(max_workers=2) as executor:
  #   futures = []
  #   settings = [1,2,3,4,5,6]
  #   for s in  settings:
  #     future = executor.submit(im_binomial, s, trial, game)
  #     print(future)
  #     futures.append(future)

  #   b = [f.result() for f in futures]
  #   plt.hist(b, label=settings)
  
  # plt.title(f"imJugller reg in {game} games")
  # plt.legend()
  # # plt.savefig("reg3000")
  # plt.show()

  pmf = im_pmf(15, game)
  print(pmf)
  p = (pmf[5])/sum(pmf)
  print(u"事前確率", round(1/6, 2))
  print(u"事後確率", round(p, 2))
  plt.title(f"imJugller 15 regs in {game} games")
  plt.bar([1,2,3,4,5,6], pmf)
  # plt.savefig("pmf3000")
  # plt.show()
  
  sim_pmf(15, game, [2,2,2,2,3,3,3,4])
  
  # PH = 1/6
  # print(PH)
  # print((PH * 0.36) / ((PH * 0.36) + (PH * 0.64)))