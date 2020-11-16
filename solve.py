import gurobipy as gp
from gurobipy import GRB
import numpy as np
import sys
import time
from xlrd import open_workbook
from xlutils.copy import copy

def read_input(file_a, file_b):
    fp = open(file_a, 'r')
    input_a = fp.read().split()
    if file_b:
        fp = open(file_b, 'r')
        input_b = fp.read().split()

    N = int(input_a[0])  # number of flows
    M = int(input_a[1])  # number of links
    U = []  # utilization of flows
    P = []  # number of paths
    B = []  # used links

    for i in range(2, 2+N):
        U.append(float(input_a[i]))
        P.append(int(input_a[i+N]))

    index = 2 + N*2
    for i in range(N):
        mat = []
        for j in range(P[i]):
            row = []
            for k in range(M):
                row.append(int(input_a[index]))
                index += 1
            mat.append(row)
        B.append(mat)

    if file_b:
        for i in range(2, 2+N):
            U.append(float(input_b[i]))
            P.append(int(input_b[i+N]))
        
        index = 2 + N*2
        for i in range(N):
            mat = []
            for j in range(P[i]):
                row = []
                for k in range(M):
                    row.append(int(input_b[index]))
                    index += 1
                mat.append(row)
            B.append(mat)
    fp.close()
    # print(N)
    # print(M)
    # print(U)
    # print(P)
    # for i in range(len(B)):
    #     print(B[i])

    return N, M, U, P, B

def solve_MILP(N, M, U, P, B):
    C = []
    path = []
    try:
        t1 = time.time()
        # Create a new model
        m = gp.Model("extensibility")

        # Create variables
        x, y = {}, {}
        for i in range(N):
            for j in range(P[i]):
                x[i, j] = m.addVar(vtype=GRB.BINARY, name="x[%s,%s]" % (i, j))
        for k in range(M):
            y[k] = m.addVar(vtype=GRB.CONTINUOUS, name="y[%s]" % k)
        z = m.addVar(vtype=GRB.CONTINUOUS, name="z")

        # Set objective
        m.setObjective(z, GRB.MAXIMIZE)

        # Add constraint
        # for all i, sigma(x_{i,j}) = 1 (Every flow can choose only one path)
        for i in range(N):
            m.addConstr(gp.quicksum(x[i, j] for j in range(
                P[i])) == 1, name="onePath[%s]" % i)

        # for all k, y_k = remaining capacity
        for k in range(M):
            m.addConstr((1 - gp.quicksum(gp.quicksum(x[i, j] * B[i][j][k] * U[i] for j in range(
                P[i])) for i in range(N))) == y[k], name="remaining[%s]" % k)

        # for all k, y_k >= 0 (Check not overload)
        for k in range(M):
            m.addConstr(y[k] >= 0, name="in_capacity[%s]" % k)

        # for all k, y_k >= z (Find min)
        for k in range(M):
            m.addConstr(y[k] >= z, name="geq_min[%s]" % k)

        # Disables solver output
        m.setParam('OutputFlag',0)

        # Optimize model
        m.optimize()
        solveTime = time.time()-t1
        # Print the objective value
        if m.SolCount > 0:
            hasSol = True
            # print('Obj: %g' % m.objVal)
            # Remaining utilization of each link
            for k in range(M):
                C.append(m.getVarByName("y[%s]" % k).x)
            for i in range(N):
                for j in range(P[i]):
                    # print(m.getVarByName("x[%s,%s]" % (i, j)).x)
                    if (m.getVarByName("x[%s,%s]" % (i, j)).x) == 1:
                        path.append(j)
                        # print('path', j)
        else:
            hasSol = False
            print("No solution.")

        return hasSol, solveTime, C, path

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except Exception as e: 
        print(e)

    except AttributeError:
        print('Encountered an attribute error')

# Feed additional flows by a shortest-path heuristic
def feed_additional(N, M, U, P, B, C, path):
    # print('MILP+SP remaining:')
    # print(C)
    # sum_util = 0
    # for i in range(len(C)):
    #     sum_util += (1-C[i])
    # fail = False
    flow_cnt = N
    for i in range(N, 2*N):
        if sum(B[i][0]) < sum(B[i][1]):
            enough = True
            for link in [j for j, e in enumerate(B[i][0]) if e == 1]:
                if(C[link] < U[i]):
                    enough = False
                    break
            if enough:
                # sum_util += (U[i] * sum(B[i][0]))
                flow_cnt += 1
                for link in [j for j, e in enumerate(B[i][0]) if e == 1]:
                    C[link] -= U[i]
                path.append(0)
                # print(i, U[i])
                # print('path', 0)
                # print(C)
                continue

        enough = True
        for link in [j for j, e in enumerate(B[i][1]) if e == 1]:
            if(C[link] < U[i]):
                enough = False
                break
        if enough:
            # sum_util += (U[i] * sum(B[i][1]))
            flow_cnt += 1
            for link in [j for j, e in enumerate(B[i][1]) if e == 1]:
                C[link] -= U[i]
            path.append(1)
            # print(i, U[i])
            # print('path', 1)
            # print(C)
        else:
            path.append(-1)
    
    return flow_cnt, path


def feed_all(N, M, U, P, B):
    C = [1]*M
    path = []
    flow_cnt = 0
    fail = False
    for i in range(N):
        if sum(B[i][0]) < sum(B[i][1]):
            enough = True
            for link in [j for j, e in enumerate(B[i][0]) if e == 1]:
                if(C[link] < U[i]):
                    enough = False
                    break
            if enough:
                # sum_util += (U[i] * sum(B[i][0]))
                flow_cnt += 1
                for link in [j for j, e in enumerate(B[i][0]) if e == 1]:
                    C[link] -= U[i]
                path.append(0)
                # print(i, U[i])
                # print(C)
                # if i==(N-1):
                #     print('All SP remaining:')
                #     print(C)
                continue

        enough = True
        for link in [j for j, e in enumerate(B[i][1]) if e == 1]:
            if(C[link] < U[i]):
                enough = False
                break
        if enough:
            # sum_util += (U[i] * sum(B[i][1]))
            flow_cnt += 1
            for link in [j for j, e in enumerate(B[i][1]) if e == 1]:
                C[link] -= U[i]
            path.append(1)
            # print(i, U[i])
            # print(C)
            # if i==(N-1):
            #     print('All SP remaining:')
            #     print(C)
        else:
            fail = True
            path.append(-1)
            # print('All SP Accommodate ' + str(i) + ' flows')
            # print(C)
            # return i
            # break
    # print('All SP remaining:')
    # print(C)
    if not fail:
        for i in range(N, 2*N):
            if sum(B[i][0]) < sum(B[i][1]):
                enough = True
                for link in [j for j, e in enumerate(B[i][0]) if e == 1]:
                    if(C[link] < U[i]):
                        enough = False
                        break
                if enough:
                    # sum_util += (U[i] * sum(B[i][0]))
                    flow_cnt += 1
                    for link in [j for j, e in enumerate(B[i][0]) if e == 1]:
                        C[link] -= U[i]
                    path.append(0)
                    # print(i, U[i])
                    # print('path', 0)
                    # print(C)
                    # if i==(N-1):
                    #     print('All SP remaining:')
                    #     print(C)
                    continue

            enough = True
            for link in [j for j, e in enumerate(B[i][1]) if e == 1]:
                if(C[link] < U[i]):
                    enough = False
                    break
            if enough:
                # sum_util += (U[i] * sum(B[i][1]))
                flow_cnt += 1
                for link in [j for j, e in enumerate(B[i][1]) if e == 1]:
                    C[link] -= U[i]
                path.append(1)
                # print(i, U[i])
                # print('path', 1)
                # print(C)
                # if i==(N-1):
                #     print('All SP remaining:')
                #     print(C)
            else:
                path.append(-1)
            # else:
            #     fail = True
                # print('All SP Accommodate ' + str(i) + ' flows')
                # print(C)
                # return i
                # break
    else:
        for i in range(N):
            path.append(-1)

    return flow_cnt, path


def write_excel(fileName, a, b, solveTime):
    rb = open_workbook(fileName)
    ws = rb.sheet_by_index(3) 
    r = ws.nrows
    wb = copy(rb) 
    sheet = wb.get_sheet(3)
    fileNo = sys.argv[1].split('/input_')[1].split('.dat')[0] + ', ' + sys.argv[2].split('/input_')[1].split('.dat')[0]
    sheet.write(r, 0, fileNo)
    sheet.write(r, 1, a)
    sheet.write(r, 2, b)
    sheet.write(r, 3, solveTime)
    wb.save(fileName)
    # print(a, b)

def output_path(path_MILP, path_SP, B, fileName):
    f = open(fileName, 'w')
    last = len(B[0][0])-1
    for i in range(len(path_MILP)):
        if path_MILP[i] >= 0:
            if B[i][path_MILP[i]][0] == 1 and B[i][path_MILP[i]][last] == 1:
                # print(path_MILP[i], 1)
                f.write(str(1))
            else:
                # print(path_MILP[i], 0)
                f.write(str(0))
        else:
            # print(-1)
            f.write(str(-1))
        f.write('\n')

    if path_SP:
        for i in range(len(path_SP)):
            if path_SP[i] >= 0:
                if B[i][path_SP[i]][0] == 1 and B[i][path_SP[i]][last] == 1:
                    # print(path_SP[i], 1)
                    f.write(str(1))
                else:
                    # print(path_SP[i], 0)
                    f.write(str(0))
            else:
                # print(-1)
                f.write(str(-1))
            f.write('\n')

def main():
    if len(sys.argv) == 4:
        N, M, U, P, B = read_input(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 3:
        N, M, U, P, B = read_input(sys.argv[1], None)
    else:
        print('Check arguments')
        return 

    hasSol, solveTime, C, path = solve_MILP(N,M,U,P,B)
    if not hasSol:
        write_excel('result.xls', -1, -1, -1)
    elif len(sys.argv) == 4:
        result_MILP, path_MILP = feed_additional(N,M,U,P,B,C,path)
        result_SP, path_SP = feed_all(N,M,U,P,B)
        write_excel('result.xls', result_MILP, result_SP, solveTime)
        output_path(path_MILP, path_SP, B, sys.argv[3])
    elif len(sys.argv) == 3:
        output_path(path, None, B, sys.argv[2])
    else:
        print('Check arguments')

if __name__ == '__main__':
    main()