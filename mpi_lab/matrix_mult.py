from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
N = comm.Get_size()

A_matrix = None
if rank == 0:
    A_matrix = np.random.rand(N, N)

A_array = np.empty(N, dtype='d')
comm.Scatter(A_matrix, A_array, root=0)

x = None
if rank == 0:
    x = np.random.rand(N)
x_array = comm.bcast(x, root=0)

y = np.dot(A_array, x_array)
comm.Barrier()

y_array= None
if rank == 0:
    y_array = np.empty(N, dtype='d')

comm.Igather(y, y_array, root=0)
if rank == 0:
    print(str(A_matrix) + "*" + str(x_array.reshape(-1, 1)) + " = " + str(y_array.reshape(-1, 1)))