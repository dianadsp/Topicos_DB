import sys
import operator
import math
import numpy as np


def mag (x):
    return np.linalg.norm(x)

def process(vect1, vect2):
    numerator=np.dot(vect1, vect2)
    denom=float(mag(vect1))*float(mag(vect2))
    total=float(float(numerator)/denom)
    return total

def main():
    vect1=[2, 5, 0, 0, 0]
    vect2=[0, 1, 0, 2, 3]
    vect3=[2, 5, 0, 0, 0]
    total=process(vect1, vect3)
    print("comparacion: 2,5,0,0,0 con 2,5,0,0,0: ", total)
    total=process( vect1, vect2)
    print("comparacion: 2,5,0,0,0 con 0,1,0,2,3: ",total)

 
if __name__ == "__main__":
    main()
    

