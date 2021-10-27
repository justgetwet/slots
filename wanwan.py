import numpy as np
from numba import njit

_16bit = 65535
# print(_16bit/656) # 99.900914...
# print(_16bit/2054) # 31.90603...

class WanWanP:

  def __init__(self):
    self.normal_p = np.reciprocal(99.9)
    self.st_p = np.reciprocal(31.9)
    self.normal_games = 250
    self.jt_games = 54
    self.st_games = 50
    self.normal_round = np.array([3, 53, 44]) * 1/100 # 10R, 6R, 4R
    self.st_round = np.array([22, 39, 39]) * 1/100
    self.payout_d = {10: 8*10*10-8*10, 6: 8*10*6-8*6, 4: 8*10*4-8*4}

  def play(self, games, p):

    bools = np.random.rand(games) < p
    is_win = any(bools)
    game = games
    if is_win:
      game = np.where(bools==True)[0][0]
    
    return is_win, game

  def payout_by(self, round):
    
    i = np.random.choice([10, 6, 4], p=round)

    return self.payout_d[i]

  def sim_base(self, trial, pick=0):

    for base in [14, 16, 18, 20, 22]:
      invest = np.empty(trial)
      payout = np.empty(trial)
      wingames = np.empty(trial)
      dsup_games = 0
      for i in range(trial):
        inv = 0
        pay = 0
        # dsup_games = 0
        is_continue = False
        games = self.normal_games - dsup_games
        if pick:
          games = pick
        is_win, game = self.play(games, self.normal_p)
        inv = game * 250/base
        if is_win:
          pay += self.payout_by(self.normal_round)
          if pay == self.payout_d[10]: # 10R
            is_continue = True
          else:
            is_rush, _ = self.play(self.jt_games, self.normal_p)
            if is_rush:
              is_continue = True
              pay += self.payout_by(self.st_round)
              dsup_games = 4
            else:
              dsup_games = 54
        else:
          if np.random.rand() < np.reciprocal(97.5):
            dsup_games = 0
            continue
          is_continue = True # pay += payout_by(st_round)
        
        while is_continue:
          is_continue, _ = self.play(self.st_games, self.st_p)
          if is_continue:
            pay += self.payout_by(self.st_round)
      
        pay = pay * 0.99

        wingames[i] = game
        invest[i] = inv
        payout[i] = pay
      
      m_balance = round((sum(payout)-sum(invest))/trial, 1)
      m_invest = round(np.mean(invest), 1)
      m_wing = round(np.mean(wingames), 1)
      rate = round((sum(payout)/sum(invest))*100, 1)
      print("base", base,"rate", rate, "win", m_wing, "invest", m_invest, "balance", m_balance)

    print("*---*")

if __name__ == '__main__':
  
  wanp = WanWanP()
  wanp.sim_base(trial=10000, pick=0)