# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:16:42 2019

@author: admin
"""
import os
from multiprocessing import Process
def matrixmult (stroka,rows_A, B):
    cols_A = len(stroka)
    rows_B = len(B)
    cols_B = len(B[0])
    if cols_A != rows_B:
      print ("Cannot multiply the two matrices. Incorrect dimensions.")
      return
    # Create the result matrix
    # Dimensions would be rows_A x cols_B
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += stroka[k] * B[k][j]
    proc=os.getpid()
    print('{0} made by process id: {1} string'.format(C[0],proc))

if __name__=='__main__':
    matr1=[[1,2],[2,3],[3,4]]
    matr2=[[1,2,3],[4,5,6]]
    matr3=[]
    procs=[]
    for i in matr1:
        proc=Process(target=matrixmult, args=(i,3,matr2)) 
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
        