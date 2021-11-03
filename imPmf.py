import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

def imJuggler(trial, game, slist=[1,2,3,4,5,6]):
  
  p = np.empty((7, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  p[2] = 6.02, 6.02, 6.02, 6.02, 6.02, 5.78 # grape (proslo96)
  p[3][:] = 33.3   # cherry
  p[4][:] = 1024.0 # bell
  p[5][:] = 1024.0 # crown
  p[6][:] = 7.0    # replay
  q = np.reciprocal(p)
  o = np.array([252, 96, 8, 1, 14, 10, 3])
  func = np.frompyfunc(lambda x: np.random.binomial(game, x, trial), 1, 1)

  


def im_pmf(n, game):
  
  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  q = np.reciprocal(p)
  ret = [binom.pmf(n, game, q[1,s]) for s in range(6)]
  
  rate = np.array([97.0, 98.0, 99.5, 101.1, 103.3, 105.5])
  rate *= 0.01
  print(rate)
  pmf = [r/sum(ret) for r in ret]
  spam = np.array(pmf) * rate
  print(sum(spam)) # 103%

  return ret

if __name__ == '__main__':
  
  pmf = im_pmf(15, 3000)
  
  #plt.bar([1,2,3,4,5,6], pmf)
  #plt.show()