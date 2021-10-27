import numpy as np

def modeAB_lots(s):
  """  """
  Bell_Replay = 0.19, 0.19, 0.21, 0.21, 0.23, 0.23
  Cherry = 1.00, 1.00, 1.27, 1.43, 1.56, 1.56
  Suika = 4.02, 4.02, 4.41, 4.75, 5.00, 5.00
  Reach = 100.0
  kCherry = 100.0
  cCherry = 100.0

  bell = np.array(Bell_Replay) * 1/100 # 2,3
  replay = np.array(Bell_Replay) * 1/100 # 4
  cherry = np.array(Cherry) * 1/100 # 5
  suika = np.array(Suika) * 1/100 # 6
  reach  = np.full(6, Reach) * 1/100 # 7
  kcherry = np.full(6, kCherry) * 1/100 # 8
  ccherry = np.full(6, cCherry) * 1/100 # 9

  p = 0. , 0., bell[s], bell[s], replay[s], cherry[s], suika[s], reach[s], kcherry[s], ccherry[s] 

  return p

def chance_lots():
  
  Bell_Replay = 0.56
  Cherry = 2.5
  Suika = 10.0
  Reach = 100.0
  kCherry = 100.0
  cCherry = 100.0

  bell = np.array(Bell_Replay) * 1/100 # 2,3
  replay = np.array(Bell_Replay) * 1/100 # 4
  cherry = np.array(Cherry) * 1/100 # 5
  suika = np.array(Suika) * 1/100 # 6
  reach  = np.array(Reach) * 1/100 # 7
  kcherry = np.array(kCherry) * 1/100 # 8
  ccherry = np.array(cCherry) * 1/100 # 9

  p = 0. , 0., bell, bell, replay, cherry, suika, reach, kcherry, ccherry 

  return p

def heaven_lots():

  Bell_Replay = 10.42
  Cherry = 6.25
  Suika = 25.0
  Reach = 100.0
  kCherry = 100.0
  cCherry = 100.0

  bell = np.array(Bell_Replay) * 1/100 # 2,3
  replay = np.array(Bell_Replay) * 1/100 # 4
  cherry = np.array(Cherry) * 1/100 # 5
  suika = np.array(Suika) * 1/100 # 6
  reach  = np.array(Reach) * 1/100 # 7
  kcherry = np.array(kCherry) * 1/100 # 8
  ccherry = np.array(cCherry) * 1/100 # 9

  p = 0. , 0., bell, bell, replay, cherry, suika, reach, kcherry, ccherry 

  return p

def set_mode(s, role):

  # A, B, Chance, Prepara, End(BB), Heaven(BB), DokiDoki(BB), SuperDokiDoki(BB)
  # 0, 1, 2, 3, 4, 5, 6, 7

  # A, B, Chance, Prepara
  br1 = np.array([76.2, 16.8, 6.2, 0.8]) * 1/100
  br2 = np.array([64.1, 25.0, 10.1, 0.8]) * 1/100
  br3 = np.array([74.2, 18.8, 6.2, 0.8]) * 1/100
  br4 = np.array([64.1, 25.0, 10.1, 0.8]) * 1/100
  br5 = np.array([74.2, 18.8, 6.2, 0.8]) * 1/100
  br6 = np.array([55.5, 31.2, 12.5, 0.8]) * 1/100
  br = np.array([br1, br2, br3, br4, br5, br6])
  bellrep_p = np.cumsum(br[s])
  
  # A, B, Chance, Prepara, End(BB), Heaven(BB)
  cr1 = np.array([54.3, 37.5, 6.2, 0.8, 0.8, 0.4]) * 1/100
  cr2 = np.array([37.9, 50.0, 10.1, 0.8, 0.8, 0.4]) * 1/100
  cr3 = np.array([54.3, 37.5, 6.2, 0.8, 0.8, 0.4]) * 1/100
  cr4 = np.array([37.5, 50.0, 10.1, 0.8, 0.8, 0.8]) * 1/100
  cr5 = np.array([53.9, 37.5, 6.2, 0.8, 0.8, 0.8]) * 1/100
  cr6 = np.array([35.1, 50.0, 12.5, 0.8, 0.8, 0.8]) * 1/100
  cr = np.array([cr1, cr2, cr3, cr4, cr5, cr6])
  cherry_p = np.cumsum(cr[s])

  # A, B, Chance, Prepara, End(BB), Heaven(BB), DokiDoki(BB)
  sk1 = np.array([39.1, 50.0, 6.2, 0.8, 2.3, 1.2, 0.4]) * 1/100
  sk2 = np.array([22.7, 62.5, 10.1, 0.8, 2.3, 1.2, 0.4]) * 1/100
  sk3 = np.array([39.1, 50.0, 6.2, 0.8, 2.3, 1.2, 0.4]) * 1/100
  sk4 = np.array([21.9, 62.5, 10.1, 0.8, 2.7, 1.6, 0.4]) * 1/100
  sk5 = np.array([38.3, 50.0, 6.2, 0.8, 2.7, 1.6, 0.4]) * 1/100
  sk6 = np.array([19.5, 62.5, 12.5, 0.8, 2.7, 1.6, 0.4]) * 1/100
  sk = np.array([sk1, sk2, sk3, sk4, sk5, sk6])
  suika_p = np.cumsum(sk[s])

  # End(BB), Heaven(BB), DokiDoki(BB)
  reachRole = np.array([59.4, 37.5, 3.1]) * 1/100
  reach_p = np.cumsum(reachRole)
  # End(BB), Heaven(BB), DokiDoki(BB)
  kCherry = np.array([59.4, 37.5, 3.1]) * 1/100
  kcherry_p = np.cumsum(kCherry)
  # Heaven(BB), DokiDoki(BB), SuperDokiDoki(BB)
  cCherry = np.array([37.5, 12.5, 50.0]) * 1/100
  ccherry_p = np.cumsum(cCherry)

  blank = np.array([0., 1.])
  role_p = blank, bellrep_p, bellrep_p, bellrep_p, cherry_p, suika_p, reach_p, kcherry_p, ccherry_p
  for arr in role_p:
    arr[-1] = 1.

  p = role_p[role]
  m = np.searchsorted(p, np.random.rand())
  if role == 6 or role == 7:
    m = m + 4
  if role == 8:
    m = m + 5

  return m



def okidoki2(s, game=1000):
  s = s-1
  """ spec """
  Big = 681.8, 687.8, 605.4, 582.9, 539.2, 535.7
  Reg = 967.6, 968.3, 883.4, 873.9, 807.8, 808.3
  bns = 399.9, 399.0, 359.2, 349.7, 323.3, 322.2
  rate = 97.0, 98.6, 101.0, 103.1, 105.0, 107.0

  BellA = 117.9, 124.1, 131.1, 138.8, 147.6, 157.5
  BellB = 157.5, 147.6, 138.8, 131.1, 124.1, 117.9
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
  cbell = (bella + bellb)#  * 1/2 # A,Bの出目に差があるが実際は同じ共通ベル
  obell = np.reciprocal(np.full(6, oBell)) #  * 1/4 # 4択の押し順

  blank = np.reciprocal(np.full(6, Blank))
  replay = np.reciprocal(Replay)
  cherry = np.reciprocal(Cherry)
  suika = np.reciprocal(np.full(6, Suika))

  reach = np.reciprocal(np.full(6, Reach))
  kcherry = np.reciprocal(np.full(6, kCherry))
  ccherry = np.reciprocal(np.full(6, cCherry))

  round_error = 1-(blank[s] + cbell[s] + obell[s] + replay[s] + cherry[s] + suika[s] + reach[s] + kcherry[s] + ccherry[s])
  seq = blank[s]+round_error, cbell[s], obell[s], replay[s], cherry[s], suika[s], reach[s], kcherry[s], ccherry[s]
  roles_p = np.array(seq)
  # print(np.cumsum(roles_p))

  func = lambda p, rnd: np.searchsorted(np.cumsum(p), rnd)
  rnd = np.random.rand(game)
  roles = func(roles_p, rnd)
  
  role = 0
  while not role:
    role = func(roles_p, np.random.rand())


  mode = set_mode(s, role)
  print(s, role, mode)

if __name__ == '__main__':

  for i in range(1,7):
    okidoki2(i, game=1000)
  # okidoki2(1, game=1000)