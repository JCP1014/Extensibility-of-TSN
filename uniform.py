import random
import sys
import numpy as np
import math

def gen_input(fileName, N, M):
    f = open(fileName, "w")

    # number of flows
    f.write(str(N)+'\n')

    # number of links
    f.write(str(M)+'\n')

    # range_max = 5e-2 / (N/100)
    # utilization of flows
    for i in range(N):
        # f.write(str(round(random.random(), 1))+'\n')
        f.write(str(round(random.uniform(1e-6, 1.5e-1), 6))+'\n')

    # number of possible paths
    for i in range(N):
        f.write('2\n')

    # used links of possible paths
    for i in range(N):
        row1 = np.zeros(M)
        start = random.randint(0,M-1)   # start link
        num = random.randint(1,M-1)   # steps
        # print(start, num)
        for j in range(start, start+num):
            if j >= M:
                row1[j-M] = 1
            else:
                row1[j] = 1
        row2 = np.zeros(M)
        for j in range(M):
            if row1[j] == 0:
                row2[j] = 1
        for j in range(M):
            f.write(str(int(row1[j]))+' ')
        f.write('\n')
        for j in range(M):
            f.write(str(int(row2[j]))+' ')
        f.write('\n')

    f.close()

def main():
    N = 30
    M = 19

    gen_input(sys.argv[1], N, M)
    gen_input(sys.argv[2], N, M)

if __name__ == '__main__':
    main()