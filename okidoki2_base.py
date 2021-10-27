import numpy as np

def okidoki2(s, game=1000):
  s = s-1
  """ spec """
  Big = 681.8, 687.8, 605.4, 582.9, 539.2, 535.7
  Reg = 967.6, 968.3, 883.4, 873.9, 807.8, 808.3
  bns = 399.9, 399.0, 359.2, 349.7, 323.3, 322.2
  rate = 97.0, 98.6, 101.0, 103.1, 105.0, 107.0

  BellA = 117.9, 124.1, 131.1, 138.8, 147.6, 157.5
  BellB = 157.1, 147.6, 138.8, 131.1, 124.1, 117.9
  oBell = 1.3
  Cherry = 40.0, 38.9, 37.8, 36.8, 35.9, 35.0
  Replay = 8.9, 9.0, 9.1, 9.1, 9.2, 9.2

  Blank = 24.6
  Suika = 128.0
  Reach = 16384.0
  kCherry = 16384.0
  cCherry =16384.0

  modeA = 999
  modeB = 999
  chance = 256
  prepara = 500
  heaven = 32

  big = np.reciprocal(Big)
  reg = np.reciprocal(Reg)

  bella = np.reciprocal(BellA)
  bellb = np.reciprocal(BellB)
  cbell = (bella + bellb) * 1/2 # A,Bの出目に差があるが実際は同じ共通ベル
  obell = np.reciprocal(np.full(6, oBell)) * 1/4 # 4択の押し順

  blank = np.reciprocal(np.full(6, Blank))
  replay = np.reciprocal(Replay)
  cherry = np.reciprocal(Cherry)
  suika = np.reciprocal(np.full(6, Suika))

  reach = np.reciprocal(np.full(6, Reach))
  kcherry = np.reciprocal(np.full(6, kCherry))
  ccherry = np.reciprocal(np.full(6, cCherry))

  bonus_seq = 1-(big[s]+reg[s]), big[s], reg[s]
  bonus_p = np.array(bonus_seq)
  # print(np.cumsum(bonus_p))

  obell_miss = 1-(blank[s] + cbell[s] + obell[s] + replay[s] + cherry[s] + suika[s] + reach[s] + kcherry[s] + ccherry[s])
  roles_seq = obell_miss, blank[s], cbell[s], obell[s], replay[s], cherry[s], suika[s], reach[s], kcherry[s], ccherry[s]
  roles_p = np.array(roles_seq)
  # print(np.cumsum(roles_p))

  func = lambda p, rnd: np.searchsorted(np.cumsum(p), rnd)
  rnd = np.random.rand(game)

  bonus = func(bonus_p, rnd)
  roles = func(roles_p, rnd)
  b = np.count_nonzero(bonus > 0)
  if not b:
    b = 999

  # dic = Dict.empty(key_type=types.int64,value_type=types.int64)
  dic = {}
  keys = np.int64([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
  medals = np.int64([0, 0, 8, 8, 3, 3, 3, 3, 3, 3])
  for k, m in zip(keys, medals):
    dic[k] = m
  
  result = np.int64([dic[k] for k in roles])
  # 千円あたりベース
  safe = np.sum(result)
  out = game*3
  b = safe/out
  bo = 50/(1-b)
  print(bo/3) # 51.794..

if __name__ == '__main__':

  for i in range(1,7):
    okidoki2(i, game=1000000)