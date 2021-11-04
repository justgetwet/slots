import numpy as np

def imBinomial(game):
  
  p = np.empty((7, 6))
  p[0] = 273.1, 269.7, 269.7, 259.0, 259.0, 255.0 # big
  p[1] = 439.8, 399.6, 331.0, 315.1, 255.0, 255.0 # reg
  p[2] = 6.02, 6.02, 6.02, 6.02, 6.02, 5.78 # grape (proslo96)
  p[3][:] = 33.3   # cherry
  p[4][:] = 1024.0 # bell
  p[5][:] = 1024.0 # crown
  p[6][:] = 7.0    # replay
  q = np.reciprocal(p)
  o = np.array([252, 96, 8, 1, 14, 10, 3])
  func = np.frompyfunc(lambda x: np.random.binomial(game, x), 1, 1)

  
  
  for s in [1,2,3,4,5,6]:
    rate = sum(func(q[:,s-1]) * o) / (game * 3)
    rate *= 100
    print(s, round(rate, 2))

if __name__ == '__main__':
  # add .
  imBinomial(10**18)