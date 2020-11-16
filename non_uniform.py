import random
import sys
import numpy as np
from xlrd import open_workbook
from xlutils.copy import copy

def gen_input(fileName, N, M, p_start, p_end):
    f = open(fileName, "w")

    # number of flows
    f.write(str(N)+'\n')

    # number of links
    f.write(str(M)+'\n')

    # utilization of flows
    for i in range(N):
        # f.write(str(round(random.random(), 1))+'\n')
        f.write(str(random.uniform(1e-16, 3e-2))+'\n')

    # number of possible paths
    for i in range(N):
        f.write('2\n')

    # used links of possible paths
    for i in range(N):
        start = np.random.choice(M, p=p_start)  # start link
        end = np.random.choice(M, p=p_end)    # end link
        while (start == end) or (abs(start-end)+1 == M):
            end = np.random.choice(M, p=p_end)
        if end < start:
            tmp = start
            start = end
            end = tmp
        # print(start, end)
        row1 = np.zeros(M)
        for j in range(start, end+1):
                row1[j] = 1
        row2 = np.full(M, 1)
        for j in range(start, end+1):
                row2[j] = 0
        for j in range(M):
            f.write(str(int(row1[j]))+' ')
        f.write('\n')
        for j in range(M):
            f.write(str(int(row2[j]))+' ')
        f.write('\n')

    f.close()

def write_excel(fileName, a, b):
    rb = open_workbook(fileName)
    ws = rb.sheet_by_index(2) 
    r = ws.nrows
    wb = copy(rb) 
    sheet = wb.get_sheet(2) 
    sheet.write(r, 3, a)
    sheet.write(r, 4, b)
    wb.save(fileName)


def main():
    N = 100
    M = 19

    # non-uniform probability
    start = random.randint(0,M-1)   # start link
    end = random.randint(0,M-1)   # end link
    while (start == end) or (abs(start-end)+1 == M):
        end = random.randint(0,M-1)
    if end < start:
        tmp = start
        start = end
        end = tmp

    # Record start and end
    write_excel('result.xls', start, end)

    p_start = np.full(M, 0.01)
    p_start[start] = 1 - (0.01)*(M-1)
    p_end = np.full(M, 0.01)
    p_end[end] = 1 - (0.01)*(M-1)
    # p_start = np.zeros(M)
    # p_start[start] = 1
    # p_end = np.zeros(M)
    # p_end[end] = 1
    # print(p_start, p_end)
    gen_input(sys.argv[1], N, M, p_start, p_end)
    gen_input(sys.argv[2], N, M, p_start, p_end)

if __name__ == '__main__':
    main()