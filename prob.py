import numpy as np
import matplotlib.pyplot as plt

# 同時確率 p(X, Y)
# p(X=1, Y=1) = 0.25
# p(X=1, Y=0) = 0.25
# p(X=0, Y=1) = 0.25
# p(X=0, Y=0) = 0.25

# 周辺確率 p(X)

# 条件付き確率 P(X|Y)

# 確率変数 X,Y について
# p(X, Y) = p(X|Y)p(X) の等式が成り立つ

# ベイズの公式
# p(X|Y) = p(X|Y)p(X)/p(Y)

if __name__ == '__main__':
  
  X = np.array([0.02, 0.12, 0.19, 0.27, 0.42, 0.51, 0.64, 0.84, 0.88, 0.99])
  t = np.array([0.05, 0.87, 0.94, 0.92, 0.54, -0.11, -0.78, -0.89, -0.79, -0.04])

  fig = plt.figure(figsize=(4, 3))
  ax = fig.gca()

  phi = lambda x: [1, x, x**2, x**3]

  PHI = np.array([phi(x) for x in X])
  # print(PHI)

  # w = np.dot(np.linalg.inv(np.dot(PHI.T, PHI)), np.dot(PHI.T, t))
  w = np.linalg.solve(np.dot(PHI.T, PHI), np.dot(PHI.T, t)) 
  print(w)

  def f(w, x): return np.dot(w, phi(x))

  xlist = np.arange(0, 1, 0.01)
  ylist = [f(w, x) for x in xlist]

  ax.plot(X, t, "go")
  ax.plot(xlist, ylist)
  plt.show()