import numpy as np

def set_mode(s, role):
  
  dic = dict()
  dic[0], dic[1], dic[2], dic[3] = "No rare", "No rare", "No rare", "No rare"
  dic[4] = "cherry"
  dic[5] = "suika"
  dic[6] = "reach"
  dic[7] = "kcherry"
  dic[8] = "ccherry"

  def lottery(p):
    i, = p.nonzero()
    q = p[i]
    q *= 1/100
    # print(q.sum())
    arr = q.cumsum()
    arr[-1] = 1.
    rnd = np.random.rand()
    return i[0] + np.searchsorted(arr, rnd)

  p = np.empty((6, 8))

  if dic[role] == "No rare":
    # A, B, chance, prepare, end, heaven, dokidoki, superdokidoki
    p[0] = 76.2, 16.8,  6.2,  0.8,  0.0,  0.0,  0.0,  0.0
    p[1] = 64.1, 25.0, 10.1,  0.8,  0.0,  0.0,  0.0,  0.0
    p[2] = 74.2, 18.8,  6.2,  0.8,  0.0,  0.0,  0.0,  0.0
    p[3] = 64.1, 25.0, 10.1,  0.8,  0.0,  0.0,  0.0,  0.0
    p[4] = 74.2, 18.8,  6.2,  0.8,  0.0,  0.0,  0.0,  0.0
    p[5] = 55.5, 31.2, 12.5,  0.8,  0.0,  0.0,  0.0,  0.0

  if dic[role] == "cherry":
    p[0] = 54.3, 37.5,  6.2,  0.8,  0.8,  0.4,  0.0,  0.0
    p[1] = 37.9, 50.0, 10.1,  0.8,  0.8,  0.4,  0.0,  0.0
    p[2] = 54.3, 37.5,  6.2,  0.8,  0.8,  0.4,  0.0,  0.0
    p[3] = 37.5, 50.0, 10.1,  0.8,  0.8,  0.8,  0.0,  0.0
    p[4] = 53.9, 37.5,  6.2,  0.8,  0.8,  0.8,  0.0,  0.0
    p[5] = 35.1, 50.0, 12.5,  0.8,  0.8,  0.8,  0.0,  0.0

  if dic[role] == "suika":
    p[0] = 39.1, 50.0,  6.2,  0.8,  2.3,  1.2,  0.4,  0.0
    p[1] = 22.7, 62.5, 10.1,  0.8,  2.3,  1.2,  0.4,  0.0
    p[2] = 39.1, 50.0,  6.2,  0.8,  2.3,  1.2,  0.4,  0.0
    p[3] = 21.9, 62.5, 10.1,  0.8,  2.7,  1.6,  0.4,  0.0
    p[4] = 38.3, 50.0,  6.2,  0.8,  2.7,  1.6,  0.4,  0.0
    p[5] = 19.5, 62.5, 12.5,  0.8,  2.7,  1.6,  0.4,  0.0

  if dic[role] in ["reach", "kcherry"]:
    p[:] =  0.0,  0.0,  0.0,  0.0, 59.4, 37.5,  3.1,  0.0

  if dic[role] == "ccherry":
    p[:] =  0.0,  0.0,  0.0,  0.0,  0.0, 37.5, 12.5, 50.0

  mode = lottery(p[s-1])
  
  return mode

def change_mode(s, role, mode):

  def lottery(p):
    # print("sum", np.sum(p))
    i, = p.nonzero()
    q = p[i]
    q *= 1/100
    # if q.sum() != 1.:
    #   print(q.sum())
    arr = q.cumsum()
    arr[-1] = 1.
    rnd = np.random.rand()
    return 3 + i[0] + np.searchsorted(arr, rnd)

  dic =dict()
  dic[0], dic[1], dic[2], dic[3] = "No rare", "No rare", "No rare", "No rare"
  dic[4] = "cherry"
  dic[5] = "suika"
  dic[6] = "reach"
  dic[7] = "kcherry"
  dic[8] = "ccherry"

  p = np.empty((6, 6))
  q = np.empty((9, 6))

  if dic[role] in ["No rare", "cherry"] and mode == 0: # mode A
    # prepare, end, heaven, dokidoki, superdokidoki, ensure
    p[0] =    0.0, 93.3,  5.9,  0.8,  0.0,  0.0
    p[1] =    0.0, 90.6,  8.6,  0.8,  0.0,  0.0
    p[2] =    0.0, 87.5, 11.7,  0.8,  0.0,  0.0
    p[3] =    0.0, 84.4, 14.8,  0.8,  0.0,  0.0
    p[4] =    0.0, 83.6, 15.6,  0.8,  0.0,  0.0
    p[5] =    0.0, 78.9, 20.3,  0.8,  0.0,  0.0

  if dic[role] in ["No rare", "cherry"] and mode == 1: # mode B
    p[0::2] = 0.0, 50.0, 49.2,  0.4,  0.4,  0.0 # 1, 3, 5
    p[1::2] = 0.0, 39.8, 59.4,  0.4,  0.4,  0.0 # 2, 4, 6
  
  if dic[role] in ["No rare", "cherry"] and mode == 2: # chance
    p[:]   = 18.7, 75.0,  5.5,  0.8,  0.0,  0.0

  if dic[role] == "No rare" and mode == 3: # prepare
    p[:]   =  0.0,  0.0, 99.2,  0.4,  0.4,  0.0

  if dic[role] == "No rare" and mode == 4: # end
    p[:]   =  0.0, 100.0, 0.0,  0.0,  0.0,  0.0

  if dic[role] == "No rare" and mode == 5: # heaven
    p[0::2] = 0.0, 25.8, 73.4,  0.8,  0.0,  0.0 # 1, 3, 5
    p[1::2] = 0.0, 33.6, 65.6,  0.8,  0.0,  0.0 # 2, 4, 6

  if dic[role] == "No rare" and mode > 5:
    q[6]   =  0.0,  0.0,  0.0, 79.7,  0.4, 19.9 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,  0.0, 90.2,  9.8 # superdokidoki
    q[8]   =  0.0,100.0,  0.0,  0.0,  0.0,  0.0 # ensure
    p[:]   = q[mode]

  if dic[role] == "cherry" and mode > 2:
    q[3]   =  0.0,  0.0, 93.7,  5.5,  0.8,  0.0 # prepare
    q[4]   =  0.0, 100.0, 0.0,  0.0,  0.0,  0.0 # end
    q[5]   =  0.0,  0.0, 99.2,  0.8,  0.0,  0.0 # heaven
    q[6]   =  0.0,  0.0,  0.0, 99.6,  0.4,  0.0 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,  0.0, 100.0, 0.0 # superdokidoki
    q[8]   =  0.0,  0.0,  0.4,  0.0,  0.0, 99.6 # ensure
    p[:]   = q[mode]

  if dic[role] == "suika":
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

  if dic[role] in ["reach", "kcherry"]:
    # prepare, end, heaven, dokidoki, superdokidoki, ensure
    q[0]   =  0.0, 59.4, 37.5,  3.1,  0.0,  0.0 # A
    q[1]   =  0.0, 32.8, 42.2, 24.2,  0.8,  0.0 # B
    q[2]   = 33.6, 25.8, 37.5,  3.1,  0.0,  0.0 # chance
    q[3]   =  0.0,  0.0, 60.2, 37.5,  2.3,  0.0 # prepare
    q[4]   =  0.0, 59.4, 37.5,  3.1,  0.0,  0.0 # end
    q[5]   =  0.0,  0.0, 93.7,  5.5,  0.8,  0.0 # heaven
    q[6]   =  0.0,  0.0,  0.0, 96.9,  3.1,  0.0 # dokidoki
    q[7]   =  0.0,  0.0,  0.0,  0.0,100.0,  0.0 # superdokidoki
    q[8]   =  0.0,  0.0,  37.5,  3.1,  0.0, 59.4 # ensure
    p[:]   = q[mode]

  if dic[role] == "ccherry":
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

  next_mode = lottery(p[s-1])

  if dic[role] in ["cherry", "suika"] and mode == 8: # ensure
    if next_mode == 6:
      next_mode += 2
  
  if dic[role] in ["reach", "kcherry"] and mode == 8: # ensure
    if next_mode == 7:
      next_mode += 1

  return next_mode

if __name__ == '__main__':
  
  roles = [3, 4, 5, 6, 7, 8]
  s = 6
  for role in roles:
    print(set_mode(s, role))
    print(change_mode(s, role, mode=1))

  s = 3
  role = 4
  mode = 1
  trial = 1000
  arr = np.empty(trial)
  for i in range(trial):
    arr[i] = change_mode(s, role, mode)

  heaven = np.count_nonzero(arr == 5)
  print(heaven/trial)