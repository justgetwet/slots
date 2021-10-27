import numpy as np
from numba import njit
from numba.typed import Dict
from numba.types import types

@njit("Tuple((i8[:],f8[:],f8[:]))(i8,i8,i8)", cache=True)
def ge999(base, trial, pick=0):

  rounds = np.int64([10, 5])
  payout_d = Dict.empty(key_type=types.int64,value_type=types.int64)
  # payout_d = {}
  payout_d[10] = 10*10*10-10*10 # 900
  payout_d[5] = 10*10*5-10*5 # 450

  normal_round = np.array([1., 99.]) * 1/100 # 10R, 6R, 4R
  st_round = np.array([72.5, 27.5]) * 1/100  
  
  payout_by = lambda r: payout_d[rounds[np.searchsorted(np.cumsum(r), np.random.rand())]]
  # judge = lambda arr: 1 in arr

  wingames = np.empty(trial, dtype=np.int64)
  payouts = np.empty(trial)
  invests = np.empty(trial)

  for i in np.arange(trial):

    payout = 0
    densup = 0
    is_continue = False
    game = 250 - densup
    if pick:
      game = pick
    arr = np.random.rand(game) < np.reciprocal(99.9) # normal game
    is_win = np.any(arr)
    wingame = arr.size
    if is_win:
      wingame = np.where(arr==1)[0][0]
      payout += payout_by(normal_round)
      densup = 4
      if payout == payout_d[10]: # 10R
        is_continue = True # 50g + 50g
      else: # 50g
        if np.any(np.random.rand(54) < np.reciprocal(99.9)):
          payout += payout_by(st_round)
          is_continue = True
    else: # utime
      if np.any(np.random.rand(379) < np.reciprocal(99.9)):
        payout += payout_by(st_round)
        is_continue = True

    if is_continue:
      densup = 54
    while is_continue: # st
      is_continue = np.any(np.random.rand(50) < np.reciprocal(99.7))
      is_continue += np.any(np.random.rand(54) < np.reciprocal(99.9))
      if is_continue:
        payout += payout_by(st_round)

    invest = wingame * 250/base
    payout = payout * 0.97

    wingames[i] = wingame
    payouts[i] = payout * 0.97
    invests[i] = wingame * 250/base

  return wingames, payouts, invests

@njit("void(i8, i8)", cache=True)
def ge999_base(trial, pick=0):

  for base in np.arange(13, 22, 1):

    wingames, payouts, invests = ge999(base, trial, pick)
    wingame = np.mean(wingames)
    rate = (np.sum(payouts)/np.sum(invests)) * 100
    balance = np.mean(payouts-invests)
    
    print("base", base, "win", round(wingame, 1), "rate", round(rate, 1), "balance", round(balance, 1))

if __name__ == '__main__':
  
  ge999_base(trial=10000, pick=0)