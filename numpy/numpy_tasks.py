import numpy as np

def uniform_intervals(a, b, n):
    return np.linspace(a, b, n)


def cyclic123_array(n): 
    array_1 = np.array([1, 2, 3])
    return np.tile(array_1, n)

def first_n_odd_number(n):
    return 2 * np.arange(n) + 1
    
def zeros_array_with_border(n):
    a = np.zeros((n, n))
    a[0, :] = 1
    a[-1, :] = 1
    a[:, 0] = 1
    a[:, -1] = 1
    return a

def chess_board(n):
    board = np.zeros((n, n))
    board[::2, ::2] = 1
    board[1::2, 1::2] = 1
    return board

def matrix_with_sum_index(n):
    i, j = np.indices((n, n))
    return i + j
    i, j = np.indices((n, n))
    return i + j

def cos_sin_as_two_rows(a, b, dx):
    x = np.arange(a, b, dx)
    cos_x = np.cos(x)
    sin_x = np.sin(x)
    return np.vstack((cos_x, sin_x))

def compute_mean_rowssum_columnssum(A):
    mean, rows_sum, columns_sum = compute_mean_rowssum_columnssum(A)
    return np.mean(A), np.sum(A, axis=0), np.sum(A, axis=1)



def compute_integral(a, b, f, dx, method):
    match method:
        case 'rectangular':
            return np.sum(f(np.arange(a, b, dx))) * dx
        case 'trapezoidal':
            return np.sum((f(np.arange(a, b, dx)) + f(np.arange(a + dx, b + dx/2, dx))) * dx / 2)
        case 'simpson':
            return np.sum((f(np.arange(a, b, dx))
                           + 4*f(np.arange(a + dx/2, b + dx/2, dx)) + f(np.arange(a + dx, b + dx/2, dx))) * dx / 6)

def sort_array_by_column(A, j):
    return A[A[:, j].argsort()]

