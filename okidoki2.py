import numpy as np
from numba import njit
from okidoki2_mode import set_mode, change_mode

""" okidoki2
  Big =   681.8, 687.8, 605.4, 582.9, 539.2, 535.7
  Reg =   967.6, 968.3, 883.4, 873.9, 807.8, 808.3
  bns =   399.9, 399.0, 359.2, 349.7, 323.3, 322.2
  rate =   97.0,  98.6, 101.0, 103.1, 105.0, 107.0
"""

@njit("f8[:,:](i8)")
def mode_probability(s):
  # ボーナスの当選率
  m_p = np.empty((9, 9))
  # mode A, B
  p0 = np.empty((4, 6))
  p0[0] =  0.19,  0.19,  0.21,  0.21,  0.23,  0.23 # % cbell, obell, replay
  p0[1] =  1.0,   1.0,   1.27,  1.43,  1.56,  1.56 # cherry
  p0[2] =  4.02,  4.02,  4.41,  4.75,  5.00,  5.00 # suika
  p0[3] =100.0, 100.0, 100.0, 100.0, 100.0, 100.0 # reach, kakutei chudan
  p0 *= 1/100
  q = p0[:, s]
  m_p[:2] = np.array([0., q[0], q[0], q[0], q[1], q[2], q[3], q[3], q[3]])
  # chance mode
  p1 = np.empty(4)
  p1[0] =  0.56 # cbell, obell, replay
  p1[1] =  2.5  # cherry
  p1[2] = 10.0  # suika
  p1[3]= 100.0  # reach, kakutei cherry, chudan cherry
  p1 *= 1/100
  m_p[2] = np.array([0., p1[0], p1[0], p1[0], p1[1], p1[2], p1[3], p1[3], p1[3]])
  # heaven, end mode
  p2 = np.empty(4)
  p2[0] = 10.42 # cbell, obell, replay
  p2[1] =  6.25 # cherry
  p2[2] = 25.0  # suika
  p2[3]= 100.0  # reach, kakutei cherry, chudan cherry
  p2 *= 1/100
  m_p[3:] = np.array([0., p2[0], p2[0], p2[0], p2[1], p2[2], p2[3], p2[3], p2[3]])

  return m_p # 9 x 9

@njit("f8[:](i8)")
def role_probability(s):
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
  r = np.reciprocal(p)
  sum_row = np.sum(r, axis=0)
  round_error = 1 - sum_row[s]
  q = r[:, s]
  seq = q[0]+round_error, q[1]+q[2], q[3], q[4], q[5], q[6], q[7], q[8], q[9]
  
  return np.array(seq) # 1 x 9

@njit("Tuple((i8,i8))(i8,f8[:],f8[:,:],i8)")
def play(s, role_p, mode_p, mode):

  ceilings = np.zeros(9, np.int64)
  ceilings[:2] = 967 # A, B
  ceilings[2]  = 224 # chance
  ceilings[3:] =  32 # heaven
  
  ceiling_game = ceilings[mode]
  mode_prob = mode_p[mode]
  rnd = np.random.rand(ceiling_game)
  roles = np.searchsorted(np.cumsum(role_p), rnd) # 小役抽選
  bonus_p = [mode_prob[role] for role in roles]
  result = np.array(bonus_p) > np.random.rand(ceiling_game) # ボーナス抽選
  wingame = ceiling_game
  role = 0
  if np.any(result):
    i, = np.where(result==True)
    wingame = i[0] + 1
    role = roles[i[0]]

  next_mode = change_mode(s, role, mode)
  
  return wingame, next_mode

@njit("void(i8,i8)")
def main(s, trial):

  wgames = np.zeros(10000000, dtype=np.int64) # 1,000,000 trial x 10 ren
  s = s - 1
  mode_p = mode_probability(s) # 9 x 9
  role_p = role_probability(s) # 1 x 9
  j = 0
  for i in np.arange(trial):
    role = 0
    while not role:
      role = np.searchsorted(np.cumsum(role_p), np.random.rand())

    mode = set_mode(s, role)
    game, next_mode = play(s, role_p, mode_p, mode)
    wgames[j] = game
    if j: wgames[j] += 32
    j += 1
    if next_mode > 3: # end以上
      count = 0
      if next_mode == 4:
        count += 1
      while count < 2:
        game, next_mode = play(s, role_p, mode_p, mode)
        wgames[j] = game
        j += 1
        if next_mode == 4:
          count += 1

  print(wgames[wgames.nonzero()])

if __name__ == '__main__':

  main(2, 3)