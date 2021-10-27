import numpy as np

def machine_rate(s, game):

  if not s in [1,2,3,4,6]:
    raise ValueError("invalid argument")
  f = lambda x: x-2 if x==6 else x-1
  s = f(s)
  # sp3
  big_prob = 295.2, 293.9, 292.6, 280.1, 267.5
  reg_porb = 428.3, 414.8, 385.5, 306.2, 267.5
  sum_prob = 174.8, 172.0, 166.3, 146.3, 133.7
  chr_prob = 7.19, 7.04, 6.89, 6.86, 6.69
  rep_prob = 7.0, 7.0, 7.0, 7.0, 7.0
  mac_rate = 97.1, 98.3, 100.0, 104.1, 108.1

  big = np.reciprocal(big_prob)
  reg = np.reciprocal(reg_porb)
  chr = np.reciprocal(chr_prob)
  rep = np.reciprocal(rep_prob)

  games = np.random.rand(game)
  bb = (games <= big[s]) * 259.0
  rb = ((big[s] < games) & (games <= big[s]+reg[s])) * 104.0
  ch = (games <= chr[s]) * 10.0
  rp = ((chr[s] < games) & (games <= chr[s]+rep[s])) * 3.0
  out_coin = sum(bb+rb+ch+rp)
  in_coin = game*3
  rate = out_coin/in_coin * 100

  return round(rate, 1)

if __name__ == '__main__':

  maker_rate = 97.1, 98.3, 100.0, 104.1, 108.1
  print(maker_rate)
  g = 1000000
  for i in [1,2,3,4,6]:
    print(machine_rate(i, g))

