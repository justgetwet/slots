import numpy as np 
from numba import njit
# from numba.typed import Dict
# from numba.types import types
# dic = Dict.empty(key_type=types.int64,value_type=types.int64)

# Rate = 97.0, 98.0, 99.5, 101.1, 103.3, 105.5
# Bns = 168.5, 161.0, 148.6, 142.2, 128.5, 127.5

# @njit("Tuple((i8,i8))(i8,i8)", cache=True)
def imJuggler(s, game=8000):

  s = s-1

  p = np.empty((2, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg

  q = np.empty((5, 6))
  q[0] = 6.02, 6.02, 6.02, 6.02, 6.02, 5.78 # grape (proslo96)
  q[1][:] = 33.3   # cherry
  q[2][:] = 1024.0 # bell
  q[3][:] = 1024.0 # crown
  q[4][:] = 7.0    # replay

  _p = np.reciprocal(p)
  no_bonus = 1 - np.sum(_p, axis=0)[s]
  bonus_p = np.hstack((np.array([no_bonus]), _p[:,s]))
  
  _q = np.reciprocal(q)
  no_role = 1 - np.sum(_q, axis=0)[s]
  role_p = np.hstack((np.array([no_role]), _q[:,s]))

  rnd = np.random.rand(game)
  bonus = np.searchsorted(np.cumsum(bonus_p), rnd)
  roles = np.searchsorted(np.cumsum(role_p), rnd)
  idx, = bonus.nonzero()
  roles[idx] = 0
  arr = bonus * 10 + roles

  keys    = 0, 1, 2, 3, 4, 5, 10, 20
  payouts = 0, 8, 1, 14, 10, 3, 252, 96
  dic = {}
  for key, payout in zip(keys, payouts):
    dic[key] = payout

  f = np.frompyfunc(lambda x: dic[x], 1, 1) # numpy
  result = f(arr)
  # result = np.array([dic[x] for x in arr]) # numba

  payout = result.sum()
  invest = result.size * 3

  return payout, invest

if __name__ == '__main__':
  
  for s in [1,2,3,4,5,6]:
    p, i = imJuggler(s, game=1000000)
    print(f"{s} rate {round((p/i)*100, 1)} balance {p-i}")