import numpy as np
from numba import njit
from numba.typed import Dict
from numba.types import types

# _16bit = 65535
# print(_16bit/656) # 99.900914...
# print(_16bit/2054) # 31.90603...

@njit("Tuple((i8,f8,f8))(i8,i8)", cache=True)
def wanp(base, pick=0):

  rounds = np.int64([10, 6, 4])
  payout_d = Dict.empty(key_type=types.int64,value_type=types.int64)
  payout_d[10] = 8*10*10-8*10 # 720
  payout_d[6] = 8*10*6-8*6 # 432
  payout_d[4] = 8*10*4-8*4 # 288

  normal_round = np.array([3., 53., 44.]) * 1/100 # 10R, 6R, 4R
  st_round = np.array([22., 39., 39.]) * 1/100  
  
  payout_by = lambda r: payout_d[rounds[np.searchsorted(np.cumsum(r), np.random.rand())]]
  judge = lambda arr: 1 in arr

  payout = 0
  densup = 0
  is_continue = False
  game = 250 - densup
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
    if judge(np.random.rand(379) < np.reciprocal(99.9)):
      payout += payout_by(st_round)
      is_continue = True

  while is_continue: # st
    is_continue = judge(np.random.rand(50) < np.reciprocal(31.9))
    is_continue += judge(np.random.rand(4) < np.reciprocal(99.9))
    if is_continue:
      payout += payout_by(st_round)

  invest = wingame * 250/base
  payout = payout * 0.97

  return wingame, invest, payout

@njit("void(i8, i8)", cache=True)
def wanp_base(trial, pick=0):

  for base in np.arange(13, 23, 1):
    wingame = np.empty(trial, dtype=np.int64)
    invests = np.empty(trial)
    payouts = np.empty(trial)
    for i in np.arange(trial, dtype=np.int64):
      win, invest, payout = wanp(base, pick)
      wingame[i] = win
      invests[i] = invest
      payouts[i] = payout
    win = np.mean(wingame)
    rate = (np.sum(payouts)/np.sum(invests)) * 100
    balance = np.mean(payouts-invests)
    
    print(base, "win", round(win, 1), "rate", round(rate, 1), "balance", round(balance, 1))

if __name__ == '__main__':
  
  wanp_base(trial=10000, pick=0)