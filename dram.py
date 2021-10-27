import numpy as np

class DramUmi:
  
  def __init__(self):
    self.normal_p = np.reciprocal(99.9)
    self.st_p = np.reciprocal(19.3)
    self.cjt_p = np.reciprocal(163.8)
    self.cjt_round = np.array([20, 80]) * 1/100
    self.normal_games = 290
    self.jt_games = 25
    self.st_games = 10
    self.round = np.array([8, 46, 46]) * 1/100 # 10R, 6R, 4R
    self.payout_d = {10: 10*10*10-10*10, 6: 10*10*6-10*6, 4: 10*10*4-10*4}

  def play(self, games):

    bools = np.random.rand(games) < self.normal_p
    is_win = any(bools)
    game = games
    if is_win:
      game = np.where(bools==True)[0][0]

    return is_win, game

  def c_jitan(self, game, jt_game=None):
    if jt_game is None:
      jt_game = 0
    if game <= 0:
      return jt_game
    bools = np.random.rand(game) < self.cjt_p
    if any(bools):
      g = np.random.choice([40, 20], p=self.cjt_round)
      idx = np.where(bools==True)[0][0]
      jt_game += g
      game = game - idx - g
    else:
      game = 0

    return self.c_jitan(game, jt_game)

  def play_st_and_jt(self):

    bools_st = np.random.rand(self.st_games) < self.st_p
    bools_jt = np.random.rand(self.jt_games) < self.normal_p
    bools = np.concatenate([bools_st, bools_jt])
    is_win = any(bools)

    return is_win

  def payout_by_round(self):

    i = np.random.choice([10, 6, 4], p=self.round)

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
        is_continue = False
        games = self.normal_games - dsup_games
        if pick:
          games = pick
        is_win, game = self.play(games)
        jt_game = self.c_jitan(game)
        # print(jt_game)
        inv = (game-jt_game) * 250/base
        if is_win:
          pay += self.payout_by_round()
          dsup_games = 45
          if pay == self.payout_d[10]: # 10R
            is_continue = True
          else:
            is_continue = self.play_st_and_jt()
        else:
          if np.random.rand() < np.reciprocal(97.5):
            dsup_games = 0
            continue
          is_continue = True
          
        while is_continue:
          pay += self.payout_by_round()
          if pay == self.payout_d[10]: # 10R
            continue
          is_continue = self.play_st_and_jt()
      
        pay = pay * 0.97

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
  
  dram = DramUmi()
  dram.sim_base(10000, pick=150)