import sys
import numpy as np

M = int(sys.argv[1]) if len(sys.argv) > 1 else 7
lim = M+5
mat = np.zeros((lim, lim), dtype=np.int)

for b in range(lim):
    for p in range(lim):
        mat[b][p] = pow(b, p, M)

print(mat)
np.savetxt('powmod.txt', mat, fmt='%d')

