import numpy as np
# コイン単価＝投資金額/投入枚数 MY:最大獲得枚数

class SpecifiedNumber:
  # 通常モード
  _49g = 0.1, 0.1, 0.1, 0.1, 0.1, 0.1
  _99g = 0.3, 0.3, 0.3, 0.3, 0.3, 0.3
  _149g = 19.9, 19.9, 19.9, 20.4, 20.4, 20.4
  _199g = 1.3, 1.3, 1.3, 3.9, 4.8, 8.1
  _249g = 14.3, 24.4, 24.4, 24.4, 24.5, 32.2
  _299g = 1.0, 1.7, 1.7, 1.7, 1.7, 2.2
  _349g = 1.6, 1.6, 1.6, 4.9, 4.9, 5.4
  _399g = 1.4, 1.4, 1.4, 4.1, 5.0, 8.4
  _449g = 27.3, 24.6, 24.6, 19.3, 18.6, 13.7
  _499g = 2.0, 1.7, 1.7, 1.3, 1.2, 0.8
  _549g = 1.6, 1.6, 1.6, 5.4, 5.4, 5.9
  _599g = 0.1, 0.1, 0.1, 0.4, 0.4, 0.4
  _649g = 27.2, 19.8, 19.8, 12.9, 11.8, 2.0
  _699g = 1.9, 1.4, 1.4, 0.9, 0.8, 0.1
  nrmat = (_49g, _99g, _149g, _199g, _249g, _299g, 
    _349g, _399g, _449g, _499g, _549g, _599g, _649g, _699g)
  
  # 特殊モード
  s149 = 0.8
  s199 = 3.5
  s249 = 2.2
  s299 = 0.9
  s349 = 1.3
  s399 = 3.5
  s449 = 2.2
  s499 = 0.9
  s549 = 4.8
  s599 = 19.2
  s649 = 17.1
  s699 = 28.0
  s737 = 15.7
  spmat = [s149, s199, s249, s299, s349, s399, s449,
    s499, s549, s599, s649, s699, s737]

  # 子役確率
  blank = 22.1
  replay = 7.6
  o_bell = 1.7
  c_bell = 5.0
  s_bell = 1985.9
  suika = 100.2
  w_cherry = 100.2
  s_cherry = 445.8
  chance_a = 412.2
  chance_b = 346.8
  kakutei = 16384.0
  fake = 145.8 # 不明

  _small_roles = [blank, replay, o_bell, c_bell, s_bell, suika, w_cherry, 
    s_cherry, chance_a, chance_b, kakutei, fake]
  
  small_roles = np.array([np.reciprocal(r) for r in _small_roles])

  small_roles_dic = {0: "blank", 1: "replay", 2: "o_bell", 3: "c_bell", 4: "s_bell",
    5: "suika", 6: "w_cherry", 7: "s_cherry", 8: "chance_a", 9: "chance_b",
    10: "kakutei", 11: "fake"}

  # チャンスゾーン抽選（%表示）
  _suika_chance_zone = 18.0, 18.0, 25.0, 25.0, 30.0, 30.0
  # レア役抽選（%表示）
  _normal_prob_chance_ab = 9.8, 9.8, 9.8, 12.5, 18.8, 18.8
  _normal_prob_strong_cherry_bell = 20.3, 20.3, 20.3, 25.4, 25.4, 25.4
  _high_prob_weak_cherry = 0.4, 0.4, 0.4, 0.4, 0.4, 0.4
  _high_prob_chance_ab = 19.9, 19.9, 19.9, 22.3, 25.4, 25.4
  _high_prob_strong_cherry_bell = 50.0, 50.0, 50.0, 50.0, 50.0, 50.0
  # 
  suika_chance_zone = np.array(_suika_chance_zone) * 0.3 * 1/100 # 30%at
  normal_prob_chance_ab = np.array(_normal_prob_chance_ab) * 1/100
  normal_prob_strong_cherry_bell = np.array(_normal_prob_strong_cherry_bell) * 1/100
  high_prob_weak_cherry = np.array(_high_prob_weak_cherry) * 1/100
  high_prob_chance_ab = np.array(_high_prob_chance_ab) * 1/100
  high_prob_strong_cherry_bell = np.array(_high_prob_strong_cherry_bell) * 1/100


class Madoka4(SpecifiedNumber):
  
  def __init__(self):
    self.at_prob = 269.4, 251.3, 241.9, 222.2, 205.5, 188.8
    self.payout = 97.3, 99.8, 102.0, 104.1, 107.1, 110.0
    self.base = 39.0
    
    self.high_prob_change = {"w_cherry": 25.0} # 1/100.2 * 25/100
    # wcherry 23.8 + 1.2 10g or 20g + α 転落 o_bell 1.7 * 0.125 = 0.2125 10+6g



if __name__ == '__main__':

  m4 = Madoka4()
  print(m4.at_prob)

  def dict_rare_roles(s):
    dic = {}
    dic[5] = m4.suika_chance_zone[s]
    dic[25] = m4.suika_chance_zone[s] # suika -> suika 朽ちた墓地 9.4% total 0.1% 10G epb抽選
    dic[8] = m4.normal_prob_chance_ab[s]
    dic[9] = m4.normal_prob_chance_ab[s]
    dic[4] = m4.normal_prob_strong_cherry_bell[s]
    dic[7] = m4.normal_prob_strong_cherry_bell[s]
    dic[26] = m4.high_prob_weak_cherry[s]
    dic[28] = m4.high_prob_chance_ab[s]
    dic[29] = m4.high_prob_chance_ab[s]
    dic[24] = m4.high_prob_strong_cherry_bell[s]
    dic[27] = m4.high_prob_strong_cherry_bell[s]
    dic[10] = 1. # 確定役
    dic[30] = 1.
    dic.update({i: 0. for i in range(12) if i not in dic})
    dic.update({i: 0. for i in range(20, 32) if i not in dic})
    
    return dic

  small_roles_prob = np.cumsum(m4.small_roles)
  small_roles_prob[-1] = 1.

  GAMES = 1000
  # レア役、チャンスゾーン抽選
  for s in [1,2,3,4,5,6]:
    s = s-1
    win_games = []
    for _ in range(GAMES):
      win_game = 700
      func = np.vectorize(lambda x: np.where((small_roles_prob < x)==False)[0][0])
      rnd = np.random.rand(700)
      rolls = func(rnd)
      # idx_wcherries = [i for i, x in enumerate(rolls) if x == 6]
      idx_wcherries = np.where(rolls == 6)[0]
      for i in idx_wcherries: # 高確移行抽選 blank c-bell homra-fake -> 0.4%
        if rolls[i] < 20 and np.random.rand() < 0.25: # weak cherry 23.8 + 1.2 
          rng = 16
          if i > 683:
            rng = 699 - i
          for j in range(rng):
            rolls[i+j+1] = rolls[i+j+1] + 20 # ex: 高確弱チェ -> 26
      # print(rolls)
      dic = dict_rare_roles(s)
      rare_roles_prob = np.array(list(map(lambda x: dic[x], rolls)))
      is_win_roles = rare_roles_prob > np.random.rand(700)
      is_win_roles[-1] = True
      win_game = np.where(is_win_roles==True)[0][0]
  
      win_games.append(win_game)
      # print(s+1, np.mean(win_games))
    
    # 規定ゲーム数解除
    m = np.array(m4.nrmat)
    p = m.T[s]/100
    specified_p = np.cumsum(p)
    specified_p[-1] = 1.
    game_dic = { k: game  for k, game in zip(range(14), range(25, 699, 50))}
    f = np.vectorize(lambda x: game_dic[np.where((specified_p < x)==False)[0][0]])
    rnd = np.random.rand(GAMES)
    specified_games = f(rnd)    
    # print(s+1, np.mean(specified_games))

    games = [min(w,s) for w,s in zip(win_games, specified_games)]
    print(s+1, np.mean(games))
      
