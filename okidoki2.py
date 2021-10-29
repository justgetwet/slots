import numpy as np
from numba import njit
from numba.typed import Dict
from numba.types import types
from okidoki2_mode import set_mode, change_mode

""" 沖ドキ2
  Big =   681.8, 687.8, 605.4, 582.9, 539.2, 535.7
  Reg =   967.6, 968.3, 883.4, 873.9, 807.8, 808.3
  bns =   399.9, 399.0, 359.2, 349.7, 323.3, 322.2
  rate =   97.0,  98.6, 101.0, 103.1, 105.0, 107.0
"""

@njit("Tuple((f8,f8,f8,f8,f8,f8,f8,f8,f8))(i8)", cache=True)
def ab(s):
  p = np.empty((4, 6))
  p[0] =  0.19,  0.19,  0.21,  0.21,  0.23,  0.23 # % cbell, obell, replay
  p[1] =  1.0,   1.0,   1.27,  1.43,  1.56,  1.56 # cherry
  p[2] =  4.02,  4.02,  4.41,  4.75,  5.00,  5.00 # suika
  p[3] = 100.0, 100.0, 100.0, 100.0, 100.0, 100.0 # reach, kakutei chudan
  p *= 1/100
  q = p[:, s]
  # print(q)
  return 0., q[0], q[0], q[0], q[1], q[2], q[3], q[3], q[3]

@njit("Tuple((f8,f8,f8,f8,f8,f8,f8,f8,f8))()", cache=True)
def chance():
  p = np.empty(4)
  p[0] =   0.56 # cbell, obell, replay
  p[1] =   2.5  # cherry
  p[2] =  10.0  # suika
  p[3] = 100.0  # reach, kakutei cherry, chudan cherry
  p *= 1/100
  return 0., p[0], p[0], p[0], p[1], p[2], p[3], p[3], p[3]

@njit("Tuple((f8,f8,f8,f8,f8,f8,f8,f8,f8))()", cache=True)
def heaven():
  p = np.empty(4)
  p[0] =  10.42 # cbell, obell, replay
  p[1] =   6.25 # cherry
  p[2] =  25.0  # suika
  p[3] = 100.0  # reach, kakutei cherry, chudan cherry
  p *= 1/100
  return 0., p[0], p[0], p[0], p[1], p[2], p[3], p[3], p[3]

@njit("i8(i8,i8)", cache=True)
def okidoki2(s, game=967):
  s = s - 1
  # 小役確率
  p = np.empty((10, 6))
  p[0] =  24.6,  24.6,  24.6,  24.6,  24.6,  24.6 # blank
  p[1] = 117.9, 124.1, 131.1, 138.8, 147.6, 157.5 # bellA
  p[2] = 157.5, 147.6, 138.8, 131.1, 124.1, 117.9 # bellB
  p[3] =   1.3,   1.3,   1.3,   1.3,   1.3,   1.3 # O-bell
  p[4] =   8.9,   9.0,   9.1,   9.1,   9.2,   9.2 # replay
  p[5] =  40.0,  38.9,  37.8,  36.8,  35.9,  35.0 # cherry
  p[6] = 128.0, 128.0, 128.0, 128.0, 128.0, 128.0 # suika
  p[7][:] = 16384.0 # reach
  p[8][:] = 16384.0 # kakutei cherry
  p[9][:] = 16384.0 # chudan cherry
  # p[10]  =  40.0,  38.9,  37.8,  36.8,  35.9,  35.0 # cherry <= round_error.size
  q = np.reciprocal(p)
  sum_row = np.sum(q, axis=0)
  round_error = 1 - sum_row[s]
  r = q[:, s]
  seq = r[0]+round_error, r[1]+r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9]
  role = np.array(seq)

  # モード抽選
  ceiling = 967, 967, 224, 468, 32
  # mode_p = ab(s) # モード
  # mode_p = chance()
  mode_p = heaven()

  rnd = np.random.rand(game)
  roles = np.searchsorted(np.cumsum(role), rnd) # 小役抽選
  role_p = [mode_p[i] for i in roles]
  result = np.array(role_p) > np.random.rand(game) # ボーナス抽選
  wingame = game
  if np.any(result):
    i, = np.where(result==True)
    wingame = i[0]

  return wingame
  # role = 0
  # while not role:
  #   role = func(p, np.random.rand())

  # mode = set_mode(s, role)
  # print(s, role, mode)
@njit("void(i8, i8)", cache=True)
def main(s, trial=1000):
  w = np.empty(trial)
  for i in range(trial):
    w[i] = okidoki2(s, game=5000)
  
  print(np.mean(w))
    

if __name__ == '__main__':

  main(s=6, trial=10000)