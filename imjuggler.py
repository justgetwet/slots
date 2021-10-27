import numpy as np 
from numba import njit
from numba.typed import Dict
from numba.types import types

# Rate = 97.0, 98.0, 99.5, 101.1, 103.3, 105.5
# Bns = 168.5, 161.0, 148.6, 142.2, 128.5, 127.5

# @njit("Tuple((i8,i8))(i8,i8)", cache=True)
def imJuggler(s, game):
  s = s-1
  """ spec """
  Big = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0
  Reg = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0
  # Grape = 6.2, 6.2, 6.2, 6.2, 6.2, 5.9
  Grape = 6.0, 6.0, 6.0, 6.0, 6.0, 5.75
  Cherry = 33.3
  Bell = 1024.0
  Crown = 1024.0
  Replay = 7.0

  big = np.reciprocal(np.array(Big))
  reg = np.reciprocal(np.array(Reg))
  grape = np.reciprocal(np.array(Grape))
  cherry = np.reciprocal(np.full(6, Cherry)) * 1/2
  bell = np.reciprocal(np.full(6, Bell))
  crown = np.reciprocal(np.full(6, Crown))
  replay = np.reciprocal(np.full(6, Replay))

  bonus_seq = 1-(big[s]+reg[s]), big[s], reg[s]
  norole = 1-(grape[s]+cherry[s]+bell[s]+crown[s]+replay[s])
  roles_seq = norole, grape[s], cherry[s], bell[s], crown[s], replay[s]
  bonus_p = np.array(bonus_seq)
  roles_p = np.array(roles_seq)

  func = lambda p, rnd: np.searchsorted(np.cumsum(p), rnd)
  rnd = np.random.rand(game)
  
  bonus = func(bonus_p, rnd)
  print(type(bonus))
  roles = func(roles_p, rnd)
  indices, = np.where(bonus!=0)
  for idx in indices:
    roles[idx] = 0

  arr = bonus * 10 + roles

  # dic = Dict.empty(key_type=types.int64,value_type=types.int64)
  dic = {}
  keys = np.int64([0, 1, 2, 3, 4, 5, 10, 20])
  items = np.int64([0, 8, 1, 14, 10, 3, 252, 96])
  for k, i in zip(keys, items):
    dic[k] = i
  
  result = np.int64([dic[k] for k in arr])

  payout = np.sum(result)
  invest = result.size * 3

  return payout, invest

if __name__ == '__main__':
  
  for s in [1,2,3,4,5,6]:
    po, iv = imJuggler(s, game=1000000)
    print(s, "rate", round((po/iv)*100, 1),"balance", po-iv)