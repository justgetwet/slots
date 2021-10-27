import numpy as np
from numba import njit
from numba.typed import Dict
from numba.types import types



@njit("Tuple((i8,f8,f8))(i8,i8)", cache=True)
def komonchama(base, pick=0):

  rounds = np.int64([10, 3])
  payout_d = Dict.empty(key_type=types.int64,value_type=types.int64)
  payout_d[10] = 10*10*10-10*10 # 900
  payout_d[3] = 10*10*3-10*3 # 270

  normal_round = np.array([1., 99.]) * 1/100 # 10R, 6R, 4R
  st_round = np.array([25., 75.]) * 1/100  
  
  payout_by = lambda r: payout_d[rounds[np.searchsorted(np.cumsum(r), np.random.rand())]]
  judge = lambda arr: 1 in arr

  payout = 0
  densup = 0
  is_continue = False
  game = 265 - densup
  if pick:
    game = pick
  arr = np.random.rand(game) < np.reciprocal(99.9) # normal game
  is_win = judge(arr)
  wingame = arr.size
  if is_win:
    wingame = np.where(arr==1)[0][0]
    payout += payout_by(normal_round)
    densup = 4
    if payout == payout_d[10]: # 10R
      is_continue = True
    else: # jitan
      if judge(np.random.rand(54) < np.reciprocal(99.9)):
        payout += payout_by(st_round)
        is_continue = True
      else:
        densup = 54
  else: # utime
    if judge(np.random.rand(310) < np.reciprocal(99.9)):
      payout += payout_by(st_round)
      is_continue = True

  while is_continue: # st
    is_continue = judge(np.random.rand(100) < np.reciprocal(59.5))
    is_continue += judge(np.random.rand(4) < np.reciprocal(99.9))
    if is_continue:
      payout += payout_by(st_round)

  invest = wingame * 250/base
  payout = payout * 0.97

  return wingame, invest, payout

@njit("void(i8, i8)", cache=True)
def komonchama_base(trial, pick=0):

  for base in np.arange(12, 22, 1):
    wingame = np.empty(trial, dtype=np.int64)
    invests = np.empty(trial)
    payouts = np.empty(trial)
    for i in np.arange(trial, dtype=np.int64):
      win, invest, payout = komonchama(base, pick)
      wingame[i] = win
      invests[i] = invest
      payouts[i] = payout
    win = np.mean(wingame)
    rate = (np.sum(payouts)/np.sum(invests)) * 100
    balance = np.mean(payouts-invests)
    
    print(base, "win", round(win, 1), "rate", round(rate, 1), "balance", round(balance, 1))

if __name__ == '__main__':
  
  komonchama_base(trial=10000, pick=130)