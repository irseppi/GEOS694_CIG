from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    num = str(np.random.randint(1, 10))
    message = {"text": ["hello world!", num]}
    comm.send(message, dest=1)

elif rank == comm.Get_size() - 1:
    message = comm.recv(source=rank-1)
    num = int(message["text"][rank])
    message["text"].extend([str(rank * num), "goodbye world!"])
    mess = ""
    for s in message["text"]:
        mess += s + " "
    print(mess)
    
else:
    message = comm.recv(source=rank-1)
    num = int(message["text"][rank])
    message["text"].extend([str(rank * num)])
    comm.send(message, dest=rank+1)
