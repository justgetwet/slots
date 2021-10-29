import numpy as np
from numba import njit

@njit("i8(f8[:])", cache=True)
def mode_lottery(p):
  
  i, = p.nonzero()
  q = p[i]
  q *= 1/100
  acc = q.cumsum()
  acc[-1] = 1.

  return i[0] + np.searchsorted(acc, np.random.rand())

@njit("i8(i8,i8)", cache=True)
def set_mode(s, role):
  
  gets = np.empty(9, dtype=np.object_)
  gets[0:4] = "No rare"
  gets[4] = "cherry"
  gets[5] = "suika"
  gets[6] = "reach"
  gets[7] = "kcherry"
  gets[8] = "ccherry"

  p = np.empty((6, 8))

  if gets[role] == "No rare":
    # A, B, chance, prepare, end, heaven, dokidoki, superdokidoki
    p[0] = 76.2, 16.8,  6.2,  0.8,  0.0,  0.0,  0.0,  0.0
    p[1] = 64.1, 25.0, 10.1,  0.8,  0.0,  0.0,  0.0,  0.0
    p[2] = 74.2, 18.8,  6.2,  0.8,  0.0,  0.0,  0.0,  0.0
    p[3] = 64.1, 25.0, 10.1,  0.8,  0.0,  0.0,  0.0,  0.0
    p[4] = 74.2, 18.8,  6.2,  0.8,  0.0,  0.0,  0.0,  0.0
    p[5] = 55.5, 31.2, 12.5,  0.8,  0.0,  0.0,  0.0,  0.0

  if gets[role] == "cherry":
    p[0] = 54.3, 37.5,  6.2,  0.8,  0.8,  0.4,  0.0,  0.0
    p[1] = 37.9, 50.0, 10.1,  0.8,  0.8,  0.4,  0.0,  0.0
    p[2] = 54.3, 37.5,  6.2,  0.8,  0.8,  0.4,  0.0,  0.0
    p[3] = 37.5, 50.0, 10.1,  0.8,  0.8,  0.8,  0.0,  0.0
    p[4] = 53.9, 37.5,  6.2,  0.8,  0.8,  0.8,  0.0,  0.0
    p[5] = 35.1, 50.0, 12.5,  0.8,  0.8,  0.8,  0.0,  0.0

  if gets[role] == "suika":
    p[0] = 39.1, 50.0,  6.2,  0.8,  2.3,  1.2,  0.4,  0.0
    p[1] = 22.7, 62.5, 10.1,  0.8,  2.3,  1.2,  0.4,  0.0
    p[2] = 39.1, 50.0,  6.2,  0.8,  2.3,  1.2,  0.4,  0.0
    p[3] = 21.9, 62.5, 10.1,  0.8,  2.7,  1.6,  0.4,  0.0
    p[4] = 38.3, 50.0,  6.2,  0.8,  2.7,  1.6,  0.4,  0.0
    p[5] = 19.5, 62.5, 12.5,  0.8,  2.7,  1.6,  0.4,  0.0

  if gets[role] in ["reach", "kcherry"]:
    p[:] = np.array([0.0,  0.0,  0.0,  0.0, 59.4, 37.5,  3.1,  0.0])

  if gets[role] == "ccherry":
    p[:] = np.array([0.0,  0.0,  0.0,  0.0,  0.0, 37.5, 12.5, 50.0])

  mode = mode_lottery(p[s])
  
  return mode

@njit("i8(i8,i8,i8)")
def change_mode(s, role, mode):

  gets = np.empty(9, dtype=np.object_)
  gets[0:4] = "No rare"
  gets[4] = "cherry"
  gets[5] = "suika"
  gets[6] = "reach"
  gets[7] = "kcherry"
  gets[8] = "ccherry"

  p = np.empty((6, 6))
  q = np.empty((9, 6))

  if gets[role] in ["No rare", "cherry"] and mode == 0: # mode A
    # prepare, end, heaven, dokidoki, superdokidoki, ensure
    p[0] =    0.0, 93.3,  5.9,  0.8,  0.0,  0.0
    p[1] =    0.0, 90.6,  8.6,  0.8,  0.0,  0.0
    p[2] =    0.0, 87.5, 11.7,  0.8,  0.0,  0.0
    p[3] =    0.0, 84.4, 14.8,  0.8,  0.0,  0.0
    p[4] =    0.0, 83.6, 15.6,  0.8,  0.0,  0.0
    p[5] =    0.0, 78.9, 20.3,  0.8,  0.0,  0.0

  if gets[role] in ["No rare", "cherry"] and mode == 1: # mode B
    p[0::2] = np.array([0.0, 50.0, 49.2,  0.4,  0.4,  0.0]) # 1, 3, 5
    p[1::2] = np.array([0.0, 39.8, 59.4,  0.4,  0.4,  0.0]) # 2, 4, 6
  
  if gets[role] == "No rare" and mode == 5: # heaven
    p[0::2] = np.array([0.0, 25.8, 73.4,  0.8,  0.0,  0.0]) # 1, 3, 5
    p[1::2] = np.array([0.0, 33.6, 65.6,  0.8,  0.0,  0.0]) # 2, 4, 6

  if gets[role] == "No rare" and mode > 1 and mode != 5:
    q[2]   = 18.7, 75.0,  5.5,  0.8,  0.0,  0.0 # chance
    q[3]   =  0.0,  0.0, 99.2,  0.4,  0.4,  0.0 # prepare
    q[4]   =  0.0, 100.0, 0.0,  0.0,  0.0,  0.0 # end
    q[6]   =  0.0,  0.0,  0.0, 79.7,  0.4, 19.9 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,  0.0, 90.2,  9.8 # superdokidoki
    q[8]   =  0.0,100.0,  0.0,  0.0,  0.0,  0.0 # ensure
    p[:]   = q[mode]

  if gets[role] == "cherry" and mode > 1:
    q[2]   = 18.7, 75.0,  5.5,  0.8,  0.0,  0.0 # chance
    q[3]   =  0.0,  0.0, 93.7,  5.5,  0.8,  0.0 # prepare
    q[4]   =  0.0, 100.0, 0.0,  0.0,  0.0,  0.0 # end
    q[5]   =  0.0,  0.0, 99.2,  0.8,  0.0,  0.0 # heaven
    q[6]   =  0.0,  0.0,  0.0, 99.6,  0.4,  0.0 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,  0.0, 100.0, 0.0 # superdokidoki
    q[8]   =  0.0,  0.0,  0.4,  0.0,  0.0, 99.6 # ensure
    p[:]   = q[mode]

  if gets[role] == "suika":
    # prepare, end, heaven, dokidoki, superdokidoki, ensure
    q[0]   =  0.0, 66.4, 32.0,  1.6,  0.0,  0.0 # A
    q[1]   =  0.0, 32.8, 65.6,  1.2,  0.4,  0.0 # B
    q[2]   = 37.5, 50.0, 11.7,  0.8,  0.0,  0.0 # chance
    q[3]   =  0.0,  0.0, 75.0, 23.4,  1.6,  0.0 # prepare
    q[4]   =  0.0,100.0,  0.0,  0.0,  0.0,  0.0 # end
    q[5]   =  0.0,  0.0, 98.4,  1.6,  0.0,  0.0 # heaven
    q[6]   =  0.0,  0.0,  0.0, 99.6,  0.4,  0.0 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,100.0,  0.0,  0.0 # superdokidoki
    q[8]   =  0.0,  0.0,  0.4,  0.0,  0.0, 99.6 # ensure
    p[:]   = q[mode]

  if gets[role] in ["reach", "kcherry"]:
    # prepare, end, heaven, dokidoki, superdokidoki, ensure
    q[0]   =  0.0, 59.4, 37.5,  3.1,  0.0,  0.0 # A
    q[1]   =  0.0, 32.8, 42.2, 24.2,  0.8,  0.0 # B
    q[2]   = 33.6, 25.8, 37.5,  3.1,  0.0,  0.0 # chance
    q[3]   =  0.0,  0.0, 60.2, 37.5,  2.3,  0.0 # prepare
    q[4]   =  0.0, 59.4, 37.5,  3.1,  0.0,  0.0 # end
    q[5]   =  0.0,  0.0, 93.7,  5.5,  0.8,  0.0 # heaven
    q[6]   =  0.0,  0.0,  0.0, 96.9,  3.1,  0.0 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,  0.0,100.0,  0.0 # superdokidoki
    q[8]   =  0.0,  0.0, 37.5,  3.1,  0.0, 59.4 # ensure
    p[:]   = q[mode]

  if gets[role] == "ccherry":
    # prepare, end, heaven, dokidoki, superdokidoki, ensure
    q[0]   =  0.0,  0.0, 37.5, 12.5, 50.0,  0.0 # A
    q[1]   =  0.0,  0.0, 37.5, 12.5, 50.0,  0.0 # B
    q[2]   =  0.0,  0.0, 37.5, 12.5, 50.0,  0.0 # chance
    q[3]   =  0.0,  0.0,  0.0, 50.0, 50.0,  0.0 # prepare
    q[4]   =  0.0,  0.0, 37.5, 12.5, 50.0,  0.0 # end
    q[5]   =  0.0,  0.0,  0.0,  0.0, 50.0,  0.0 # heaven
    q[6]   =  0.0,  0.0,  0.0,  0.0,100.0,  0.0 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,  0.0,100.0,  0.0 # superdokidoki
    q[8]   =  0.0,  0.0,  0.0, 50.0, 50.0,  0.0 # ensure
    p[:]   = q[mode]

  next_mode = 3 + mode_lottery(p[s])

  if gets[role] in ["cherry", "suika"] and mode == 8: # ensure
    if next_mode == 6:
      next_mode += 2
  
  if gets[role] in ["reach", "kcherry"] and mode == 8: # ensure
    if next_mode == 7:
      next_mode += 1

  return next_mode

if __name__ == '__main__':
  
  gets = np.empty(9, dtype=np.object_)
  gets[0:4] = "No rare"
  gets[4] = "cherry"
  gets[5] = "suika"
  gets[6] = "reach"
  gets[7] = "kcherry"
  gets[8] = "ccherry"
  role = 8
  print(gets[role])
  trial = 100000
  for s in [1,2,3,4,5,6]:
    s = s-1
    arr = np.empty(trial, dtype=np.int64)
    for i in range(trial):
      arr[i] = set_mode(s, role)
      # arr[i] = change_mode(s, role, mode=1)
    m = np.empty(9)
    for i in range(9):
      x = np.count_nonzero(arr==i)
      m[i] = round(x/trial, 2)
    print(m)
