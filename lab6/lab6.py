import numpy as np
import scipy.linalg

def solve_down(A,B):
    X = np.copy(B)
    size = B.shape[0]

    for i in range(size):
        for j in range(0, i):
            X[i] -= A[i][j] * X[j]
        X[i] /= A[i][i]

    return X

def solve_up(A,B):
    X = np.copy(B)
    size = B.shape[0]

    for i in range(size - 1, -1, -1):
        for j in range(i + 1, size):
            X[i] -= A[i][j] * X[j]
        X[i] /= A[i][i]

    return X

def solve_LU(A, B):
    P, L, U = scipy.linalg.lu(A)
    
    ONE = solve_down(L, B)
    FINAL = solve_up(U, ONE)

    return FINAL

def solve_QR(A, B):
    Q, R = scipy.linalg.qr(A)
    B1 = np.transpose(Q) @ B

    return solve_up(R,B1)

def main():
    A = np.array([ [7, 3, -1, 2], [3, 8, 1, -4], [-1, 1, 4, -1], [2, -4, -1, 6] ], dtype=np.float64)
    B = np.array([1,2,3,4], dtype=np.float64)

    print(scipy.linalg.solve(A, B), " - linalg.solve")
    print(solve_LU(A,B), " - LU")
    print(solve_QR(A,B), " - QR")

if __name__ == "__main__":
    main()