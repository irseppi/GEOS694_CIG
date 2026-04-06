from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

for N in [10, 1000, 10000]:
    num_array = None
    if rank == 0:
        num_array = np.linspace(0, N-1, N)
        check = sum(num_array)

    partial = np.empty(int(N/size), dtype='d')
    comm.Scatter(num_array, partial, root=0)
    reduced = None
    if rank == 0:
        reduced = np.empty(size, dtype='d')
    comm.Gather(sum(partial), reduced, root=0)

    if rank == 0:
        print("The sum of 1-N is " + str(sum(reduced)) + " == " + str(check))