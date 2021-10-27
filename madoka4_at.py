import numpy as np

class AtLank:

  normal_prob_chance_ab_plus1 = 100, 100, 100, 100, 100, 100
  kakutei_plus1 = 50, 50, 50, 50, 50, 50
  kakutei_plus2 = 25, 25, 25, 25, 25, 25
  kakutei_plus3 = 25, 25, 25, 25, 25, 25
  normal_prob_strong_cherry_bell_plus1 = 98.1, 98.1, 98.1, 98.5, 98.5, 98.5
  normal_prob_strong_cherry_bell_plus2 = 1.9, 1.9, 1.9, 1.5, 1.5, 1.5
  high_prob_weak_cherry_plus3 = 100, 100, 100, 100, 100, 100
  high_prob_strong_cherry_bell_plus1 = 99.2, 99.2, 99.2, 99.2, 99.2, 99.2
  high_prob_strong_cherry_bell_plus2 = 0.8, 0.8, 0.8, 0.8, 0.8, 0.8

  high_prob_chance_ab_plus1 = 98.0, 98.0, 98.0, 98.2, 98.5, 98.5
  high_prob_chance_ab_plus1 = 2.0, 2.0, 2.0, 1.8, 1.5, 1.5

  # 本前兆中
  # runkup_lot = {chance_ab: 2.0, s_cherry: 3.9, s_bell: 3.9, kakutei: 100.0}
  # runkup_share_plus1 = {chance_ab: 2.0, s_cherry: 90.0, s_bell: 90.0, kakutei: 100.0}
  # runkup_share_plus2 = {chance_ab: 3.9, s_cherry: 10.0, s_bell: 10.0}
  
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
  
  samll_roles = np.array([np.reciprocal(r) for r in _small_roles])

  small_roles_dic = {0: "blank", 1: "replay", 2: "o_bell", 3: "c_bell", 4: "s_bell",
    5: "suika", 6: "w_cherry", 7: "s_cherry", 8: "chance_a", 9: "chance_b",
    10: "kakutei", 11: "fake"}


  # AT中のスイカで抽選、さらに0.4でmagica attackへ
  _suika_magica_battle = 16.8, 17.2, 17.6, 17.6, 18.4, 18.8 # 0.4 -> attack
  suika_magica_battle = np.array(_suika_magica_battle) * 1/100

  
  # magica attack 2G (1G soul gems lighting 2G rare roll)
  # magica attack wcherry +?? 59.5, bb 35.0, walpru 5.0, epb 0.4
  _wcherry_magica_attack = 18.0, 18.4, 19.5, 19.5, 20.3, 21.1
  _chance_ab_magica_attack = 38.7, 40.2, 42.6, 42.6, 44.5, 45.7
  wcherry_magica_attack = np.array(_wcherry_magica_attack) * 1/100
  chance_ab_magica_attack = np.array(_chance_ab_magica_attack) * 1/100
  # magica attack level blue 1- green 2- red 3- gold 4
  # 
  magica_attack_level = 86.3, 12.5, 0.8, 0.4 

  # 1/76000-1/64000 ロングフリーズ = 「アルティメットボーナス」 2000 over!
  # 本前兆中(CZ,AT,EPB)の確定役、その他で確定役の12.5%で発生

class Madoka4(AtLank):

  def __init__(self):
    self.at_prob = 269.4, 251.3, 241.9, 222.2, 205.5, 188.8
    self.payout = 97.3, 99.8, 102.0, 104.1, 107.1, 110.0
    self.base = 39.0
    self.rush = 2.5
    self.at_lank = 1, 2, 3, 4
    # 1 rush 2 rush+epb 3 rush+epb+walpur50 4 rush+epb+walpru80
    # at_stage = artist_witch, class_leader_witch, bird_cage_witch, stage_equipment_witch
    


    self.walpur = 9.4, 9.8, 11.7, 11.7, 13.3, 14.5

    self.magica_attack_level = 1, 2, 3, 4, 5, 6

if __name__ == '__main__':
  
  m4 = Madoka4()
  # print(m4.at_prob)

  def soul_gems():
    _soul_gems = 64.1, 3.4, 19.7, 1.1, 9.9, 0.5, 1.2, 0.1
    soul_gems = np.array(_soul_gems) * 1/100
    soul_gems_prob = np.cumsum(soul_gems)
    func = np.vectorize(lambda x: np.where((soul_gems_prob < x)==False)[0][0])
    p = np.random.rand()
    key = int(func(p))
    dic = {0: "sayaka3", 1: "sayaka5", 2: "mami3", 3: "mami5", 
      4: "kyoko3", 5: "kyoko5", 6: "homura3", 7: "homura5"}

    return dic[key]

  def soul_gems_system(small_roles):
    roles = np.copy(small_roles)
    for i, r in enumerate(small_roles):
      if r == 0:
        p = np.random.rand()
        if p < 0.301:
          m = soul_gems()
          # print(m)
          rng = int(m[-1])
          if (i+rng+1) > len(roles):
            rng = len(roles)-1-i
          if m[:-1] == "sayaka":
            for j in range(1, rng+1):
              if small_roles[i+j] == 1: # rep
                roles[i+j] = 8 # chance
              if 7 < small_roles[i+j] < 10: # chance
                roles[i+j] = 10 # kakutei
          if m[:-1] == "mami":
            for j in range(1, rng+1):
              if 1 < small_roles[i+j] < 4: # 2 o-bell 3 c-bell
                roles[i+j] = 5 # wcherry
              if small_roles[i+j] == 4: # s-bell
                roles[i+j] = 10
          if m[:-1] == "kyoko":
            for j in range(1, rng+1):
              if 1 < small_roles[i+j] < 4: # 2 o-bell 3 c-bell
                roles[i+j] = 5 # wcherry
              if small_roles[i+j] == 0: # blank
              # はずれを書き換えるとジェム抽選と矛盾するので自分も書き換える
                small_roles[i+j] = 8
                roles[i+j] = 8 # chance
              if small_roles[i+j] == 5: # wcherry
                roles[i+j] = 6 # scherry
              if small_roles[i+j] == 6:
                roles[i+j] = 10
          if m[:-1] == "homura":
            for j in range(1, rng+1):
              if 4 < small_roles[i+j] < 7: # 5 wcherry 6 suika
                roles[i+j] = 6 # scherry
              elif small_roles[i+j] == 4 or 6 < small_roles[i+j] < 10:
              # s-bell scherry chance
                roles[i+j] = 10
              elif small_roles[i+j] == 0:
                small_roles[i+j] = 8
                roles[i+j] = 8 # chance
              else:
                roles[i+j] = 8 # chance
    if any(np.not_equal(small_roles, roles)):
      arr = np.not_equal(small_roles, roles)
      print("index", np.where(arr==True)[0][0], "- changed!")
    return roles

  def walpru(s, roles):

    # レア役での抽選
    d = {}
    d[5] = 0.4 * 1/100 # suika
    d[8] = 9.8 * 1/100 # chance_a
    d[9] = 9.8 * 1/100 # chance_b
    d[4] = 19.5 * 1/100 # s-bell
    d[7] = 19.5 * 1/100 # scherry
    d[10] = 100.0 * 1/100
    d.update({i: 0. for i in range(12) if i not in d})

    walpru_prob = np.array(list(map(lambda x: d[x], rolls)))
    walprus = walpru_prob > np.random.rand(len(roles))
    
    # AT開始時と周期抽選
    w = np.array([12.5, 12.5, 75.0]) * 1/100
    s_games = np.array([30, 50, 100])
    specified_games = 0, np.random.choice(s_games, p=w)
    print("walpru", specified_game)
    # dic = {0: 30, 1: 50, 2: 100} # 周期
    # specified_games = np.cumsum(np.array([12.5, 12.5, 75.0]) * 1/100)
    # func = np.vectorize(lambda x: np.where((specified_games < x)==False)[0][0])
    # key = int(func(np.random.rand()))
    # specified_game = dic[key]

    walpru_rate = np.array([9.4, 9.8, 11.7, 11.7, 13.3, 14.5]) * 1/100
    
    b0 = any(walprus)
    b1 = walpru_rate[s] > np.random.rand()
    b2 = walpru_rate[s] > np.random.rand()

    return any([b0, b1, b2])


  def dict_rare_roles(s):
    suika = np.array([16.8, 17.2, 17.6, 17.6, 18.4, 18.8]) * 1/100 * 0.4
    wcherry = np.array([18.0, 18.4, 19.5, 19.5, 20.3, 21.1]) * 1/100
    chance_a = np.array([38.7, 40.2, 42.6, 42.6, 44.5, 45.7]) * 1/100
    chance_b = np.array([38.7, 40.2, 42.6, 42.6, 44.5, 45.7]) * 1/100
    dic = {}
    dic[4] = 1. # s-bell
    dic[5] = suika[s]
    dic[6] = wcherry[s]
    dic[7] = 1. # scherry
    dic[8] = chance_a[s]
    dic[9] = chance_b[s]
    dic[10] = 1. # 確定役
    dic.update({i: 0. for i in range(12) if i not in dic})

    return dic

  # print(dict_rare_roles(5))
  small_roles_prob = np.cumsum(m4.samll_roles)
  small_roles_prob[-1] = 1.

  s=4
  coin = 100
  games = int(coin / 2.5)
    # while games:
  cnt = 0
  w_cnt = 0
  for i in range(100):
    func = np.vectorize(lambda x: np.where((small_roles_prob < x)==False)[0][0])
    rnd = np.random.rand(games)
    rolls = func(rnd)
    # print(rolls)
    # soul_gems

    rolls = soul_gems_system(rolls)
    # print(rolls)
    ret = walpru(s, rolls)
    print("walpru", ret)
    if ret:
      w_cnt += 1

    dic = dict_rare_roles(s)
    rare_roles_prob = np.array(list(map(lambda x: dic[x], rolls)))
    # print(rare_roles_prob)
    is_win_roles = rare_roles_prob > np.random.rand(games)
    if any(is_win_roles):
      print(i+1, "attack!", np.where(is_win_roles==True)[0][0])
    else:
      print(i+1, "no attack!")
      cnt += 1

  print("attack", (100-cnt), "%")
  print("walprl", w_cnt, "%")
  