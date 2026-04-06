from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

num = np.array(np.random.randint(1, 1000), dtype='d')

max_num = comm.reduce(num, op=MPI.MAX, root=0)
if rank == 0:
    print("max_num: ", max_num)

if rank == 0:
    comm.bcast(max_num, root=0)
else:
    max_num = comm.bcast(max_num, root=0)

if num < max_num:
    print("Rank " + str(rank) + " has value " + str(num) + " which is less than global max " + str(max_num))
else:
    print("Rank " + str(rank) + " has value " + str(num) + " which is the global max " + str(max_num))