import numpy as np

A, B, C, D, _ = 1, 2, 3, 4, 0
tbl1 = B, B, A, B, A, B, D, _
tbl2 = B, A, B, A, B, A, D, _
tbl3 = B, B, A, B, B, C, D, _
tbl4 = B, A, B, A, C, B, D, _
tbl5 = A, A, A, A, A, A, C, D
tbl6 = B, B, B, C, B, C, D, _
tbl7 = B, A, C, B, C, B, D, _
tbl8 = C, C, C, C, C, C, D, _
tbl9 = C, A, C, A, C, B, D, _
tbl10 = B, C, A, B, A, B, D, _
tbl11 = C, B, B, A, B, A, D, _
tbl12 = B, C, B, C, B, C, D, _ 
tbl13 = C, B, C, B, C, B, D, _ 
tbl14 = A, C, A, D, _, _, _, _ 
tbl15 = A, D, _, _, _, _, _, _
tbl16 = D, _, _, _, _, _, _, _ 
mode_tables = [tbl1, tbl2, tbl3, tbl4, tbl5, tbl6, tbl7, tbl8, tbl9, 
  tbl10, tbl11, tbl12, tbl13, tbl14, tbl15, tbl16]

set1 = 14.93, 15.63, 9.35, 15.63, 9.8, 9.35, 6.25, 0.78, 1.56, 6.25, 2.34, 4.69, 1.56, 0.78, 0.78, 0.39 
set2 = 11.76, 11.76, 11.76, 11.76, 4.69, 7.81, 7.81, 3.13, 3.13, 6.25, 3.13, 9.35, 3.13, 1.56, 2.34, 0.78 
set3 = 14.49, 14.93, 9.35, 15.63, 9.8, 9.35, 6.25, 0.78, 1.56, 6.25, 2.34, 4.69, 1.56, 1.95, 0.78, 0.39 
set4 = 10.2, 10.2, 11.76, 11.76, 4.69, 7.81, 7.81, 3.13, 3.13, 6.25, 3.13, 9.35, 3.13, 3.91, 3.13, 0.78 
set5 = 12.5, 13.33, 9.35, 15.63, 9.8, 9.35, 6.25, 0.78, 1.56, 6.25, 2.34, 4.69, 1.56, 4.69, 1.56, 0.39 
set6 = 4.29, 4.29, 9.35, 9.35, 3.13, 15.63, 15.63, 3.13, 3.13, 6.25, 3.13, 9.35, 3.13, 6.25, 3.13, 0.78 
arr = np.array([set1, set2, set3, set4, set5, set6])
settings = [np.cumsum(a* 1/100) for a in arr]
for s in settings:
  s[-1] = 1.


blank = 17.6
c_bell = 83.0, 82.3, 84.2, 83.0, 82.3, 84.2
wcherry = 46.1, 44.6, 43.2, 41.8, 40.6, 39.4
scroll = 72.8
scherry = 131.6
chance = 202.3

blk = np.reciprocal([blank for _ in range(6)])
bell = np.reciprocal(c_bell)
wche = np.reciprocal(wcherry)
scl = np.reciprocal([scroll for _ in range(6)])
sche = np.reciprocal([scherry for _ in range(6)])
cha = np.reciprocal([chance for _ in range(6)])

small_roles = np.empty((0, 7), float)
for i in range(6):
  s = i - 1
  roles = [blk[s], bell[s], wche[s], scl[s], sche[s], cha[s]]
  roles.insert(0, 1-sum(roles))
  roles = np.cumsum(roles)
  small_roles = np.append(small_roles, np.array([roles]), axis=0)
  
# print(small_roles)
f = np.vectorize(lambda x: np.where((small_roles[5] < x)==False)[0][0])
rnd = np.random.rand(800)
print(f(rnd))
# scrolls = [i for i, role in enumerate(f(rnd)) if role == 5]
# print(scrolls)

# s = 6
trial = 5
for s in [1,2,3,4,5,6]:
  f = np.vectorize(lambda x: np.where((settings[s-1] < x)==False)[0][0])
  rnd = np.random.rand(trial)
  # print(s, f(rnd) + 1)









if __name__ == '__main__':
  pass