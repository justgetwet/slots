import numpy as np
from numba import njit

@njit("void(i8)", cache=True)
def genrnd(trial):

  rnd = np.random.rand(trial, 200)
  wingames = np.empty(trial)
  
  for i in range(trial):
    bool_arr = rnd[i] < np.reciprocal(99.9) # normal game
    wingame = 200
    if np.sum(bool_arr):
      wingame = np.where(bool_arr==1)[0][0]

    wingames[i] = wingame

  m = np.mean(wingames)
  print(round(m, 1))

@njit("i8[:](i8)")
def main(trial):
  rounds = np.int64([10, 6, 4])
  # payout_d = Dict.empty(key_type=types.int64,value_type=types.int64)
  payout_d = {}
  payout_d[10] = 8*10*10-8*10 # 720
  payout_d[6] = 8*10*6-8*6 # 432
  payout_d[4] = 8*10*4-8*4 # 288

  normal_round = np.array([3., 53., 44.]) * 1/100 # 10R, 6R, 4R
  st_round = np.array([22., 39., 39.]) * 1/100
  
  payout_by = lambda r: payout_d[rounds[np.searchsorted(np.cumsum(r), np.random.rand())]]

  payouts = np.empty(trial, dtype=np.int64)

  for i in range(trial):
    payout = payout_by(normal_round)
    payouts[i] = payout

  return payouts

if __name__ == '__main__':
  
  p = main(100000)
  tenr = [q for q in p if q==720]
  print(len(tenr)/100000)

  genrnd(10000)
