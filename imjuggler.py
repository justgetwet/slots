import numpy as np 
from numba import njit
# from numba.typed import Dict
# from numba.types import types
# dic = Dict.empty(key_type=types.int64,value_type=types.int64)

# Rate = 97.0, 98.0, 99.5, 101.1, 103.3, 105.5
# Bns = 168.5, 161.0, 148.6, 142.2, 128.5, 127.5

#@njit("Tuple((i8,i8))(i8,i8)", cache=True)
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
  lose = 1 - np.sum(_p, axis=0)[s]
  bonus_p = np.hstack((np.array([lose]), _p[:,s]))
  
  _q = np.reciprocal(q)
  loose = 1 - np.sum(_q, axis=0)[s]
  role_p = np.hstack((np.array([loose]), _q[:,s]))

  rnd = np.random.rand(game)
  bonus = np.searchsorted(bonus_p.cumsum(), rnd)
  role = np.searchsorted(role_p.cumsum(), rnd)
  idx, = bonus.nonzero()
  role[idx] = 0
  arr = bonus * 10 + role

  keys = 0, 1, 2, 3, 4, 5, 10, 20
  outs = 0, 8, 1, 14, 10, 3, 252, 96
  d = {}
  for key, out in zip(keys, outs):
    d[key] = out
  
  f = np.frompyfunc(lambda x: d[x], 1, 1) # numpy
  result = f(arr)
  # result = np.array([d[x] for x in arr]) # numba

  bb = np.count_nonzero(arr==10)
  rb = np.count_nonzero(arr==20)

  payout = result.sum()
  invest = result.size * 3

  return bb, rb, payout, invest

if __name__ == '__main__':
  
  bb, rb, payout, invest = imJuggler(s=2, game=1000)
  print(bb, rb, payout, invest)

  # for s in [1,2,3,4,5,6]:
  #   p, i = imJuggler(s, game=1000000)
  #   print(f"{s} rate {round((p/i)*100, 1)} balance {p-i}")