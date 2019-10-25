from multiprocessing import Process as P
from multiprocessing import current_process, Lock, Pool
from time import sleep

A = [[1, 2],
     [4, 5],
     [2, 3]]

B = [[2, 3, 4],
     [4, 5, 1]]

lock = Lock()


proc=[]


def f(x):
    return x * x

def ellmatr(i, j, k):

    with lock:

        sleep(1)
        result=A[i][0]*B[0][j]+A[i][1]*B[1][j]
        # proc_name=current_process().name
        # print(proc_name)
        if (k!=2):
            print (result,end=' ')
        else:
            print(result,"\n")


if __name__ == '__main__':
    for i in range(3):
        k = -1
        for j in range(3):
            k+=1
            pr = P(target=ellmatr, args=(i, j, k))
            proc.append(pr)
            pr.start()
    for p in proc:
        p.join()




