from numba import njit
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

# Rate = 97.0, 98.0, 99.5, 101.1, 103.3, 105.5

@njit("Tuple((i8,i8,i8,i8))(i8,i8)", cache=True)
def imJuggler(s, game):
  
  p = np.empty((7, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  p[2] = 6.02, 6.02, 6.02, 6.02, 6.02, 5.78 # grape (proslo96)
  p[3][:] = 33.3   # cherry
  p[4][:] = 1024.0 # bell
  p[5][:] = 1024.0 # crown
  p[6][:] = 7.0    # replay
  q = np.reciprocal(p[:,s-1])
  o = np.array([252, 96, 8, 1, 14, 10, 3])
  # result = np.random.binomial(game, q)
  result = np.empty(7)
  for i, x in enumerate(q):
    result[i] = np.random.binomial(game, x)
  
  bb, rb = result[:2]
  payout = np.sum(result * o)
  invest = game * 3

  return bb, rb, payout, invest

def im_pmf(n, game):
  # n = regの回数
  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  q = np.reciprocal(p)
  ret = [binom.pmf(n, game, q[1,s]) for s in range(6)]
  
  rate = np.array([97.0, 98.0, 99.5, 101.1, 103.3, 105.5])
  rate *= 0.01
  # print(rate)
  pmf = [r/sum(ret) for r in ret]
  spam = np.array(pmf) * rate
  print(sum(spam)) # 103%

  return ret

@njit("void(i8,i8[:])", cache=True)
def main(trial, setting):
  n = 0
  payout = 0
  invest = 0
  count = 0
  while count < trial:
    n += 1
    r = np.empty((setting.size, 3))
    for i, s in enumerate(setting):
      bb, rb, po, iv = imJuggler(s, 3000)
      r[i] = s, rb, po-iv 
    v = max(r[:,1])
    if v > 14:
      idx, = np.where(r[:,1]==v)
      balance = r[:,2][idx[0]]
      if balance > 0:
        s = r[:,0][idx[0]]
        _, _, p, i = imJuggler(int(s), 3000)
        payout += p
        invest += i
        count += 1
  rate = payout / invest
  print(round((trial/n)*100, 1))
  print(round(rate*100, 1))

if __name__ == '__main__':
  
  # im_pmf(16, 3000)
  # print(imJuggler(3, 8000))
  setting = np.int64([2,2,2,2,3,3,4,4,2,2,2,2,3,3,4,5])
  main(10000, setting)
  