import numpy as np
from numba import njit

@njit("void()")
def main():
  trial = 10
  rec = np.empty((trial, 3))
  #rec = np.empty(3)
  rec[:,:] = 2.2, 3.3, 4.4
  # for i in range(trial):
  #   rec[i] = 1
  print(rec)



if __name__ == '__main__':
  
  main()