import numpy as np 
np.set_printoptions(threshold=1000)
from numba import jit, f8, i8, b1, void
# from numba import jitclass
from functools import wraps
import time

def stop_watch(func) :
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        result = func(*args,**kargs)
        process_time =  time.time() - start
        print(f"{func.__name__} process takes {round(process_time, 1)} seconds")
        return result
    return wrapper

class ImJuggler:

  def __init__(self):
    """ Spec """
    Big = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0
    Reg = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0
    Bns = 168.5, 161.0, 148.6, 142.2, 128.5, 127.5
    Grape = 6.2, 6.2, 6.2, 6.2, 6.2, 5.9
    Cherry = 33.3
    Replay = 7.0
    # Bell = 1092?
    # Crown = 1092?
    Rate = 97.0, 98.0, 99.5, 101.1, 103.3, 105.5

    self.big = np.reciprocal(Big)
    self.reg = np.reciprocal(Reg)
    self.grape = np.reciprocal(Grape)
    self.cherry = np.reciprocal([Cherry for _ in range(6)])# * 1/2
    self.replay = np.reciprocal([Replay for _ in range(6)])
    # self.payout = {"big": 259, "reg": 104, "grape": 8, "cherry": 1, "replay": 3}

  def prob(self, s):
    # bonus 
    lose = 1-(self.big[s]+self.reg[s])
    bonus_p = [lose, self.big[s], self.reg[s]]
    bonus_prob = np.cumsum(bonus_p)
    # small roles
    blank = 1-(self.grape[s]+self.cherry[s]+self.replay[s])
    smallroles_p = [blank, self.grape[s], self.cherry[s], self.replay[s]]
    smallroles_prob = np.cumsum(smallroles_p)

    return bonus_prob, smallroles_prob

  @stop_watch
  def play(self, s, games=8000):
    # 0: blank, 1: grape, 2: cherry, 3: replay, 10: big, 20: reg
    bns_p, roles_p = self.prob(s)
    bns_f = np.vectorize(lambda r: np.where((bns_p < r)==False)[0][0])
    roles_f = np.vectorize(lambda r: np.where((roles_p < r)==False)[0][0])
    rnd = np.random.rand(games+1).astype(np.float32)
    # 同じ乱数を使うと毎回同じ値が重複するので
    result = bns_f(rnd[1:]) * 10 + roles_f(rnd[:-1])

    return result
  
  @stop_watch
  def balance(self, s, games=8000):

    result = self.play(s, games)
    dic = {0: 0, 1: 8, 2: 1, 3: 3, 
      10: 259, 11: 259, 12: 259, 13: 259, 
      20: 104, 21: 104, 22: 104, 23: 104 }
    payout = sum(list(map(lambda x: dic[x], result)))
    # payout = sum(np.fromiter(seq, dtype=int))
    medals = games * -3
    # print(payout)
    # print(medals)
    return payout + medals

if __name__ == '__main__':

  im = ImJuggler()
  for s in [1,2,3,4,5,6]:
    s = s-1
    balance = im.balance(s, 500000)
    print(s+1, balance)