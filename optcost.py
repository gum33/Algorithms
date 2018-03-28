# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:02:49 2018

@author: Guðmundur Magnússon
"""
import numpy as np

#Skilgreinum tvíundartré til að nota
class Node:
    def __init__(self, val):
            self.left = None
            self.right = None
            self.val = val
            
    def __str__(self):
        return 'value: {0} ', str.format(self.val)

        
def insert(root, value):
    if not root:
        return Node(value)
    elif value < root.val:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root


def search(root, value, depth=1):
    if not root:
        return 0, 0
    elif root.val == value:
        return depth, root.val
    elif value < root.val:
        return search(root.left, value, depth+1)
    else:
        return search(root.right, value, depth+1)


def optBinaryTree(f):
    n = len(f)
    OptCost = np.zeros((n,n), dtype=float)
    FA = np.zeros((n,n), dtype=float)
    
    def OptimalSearchTree(f):
        initF(f)
        for j in range(0,n):
            for i in range(j,-1,-1):
                computeOptCost(i,j)
        return OptCost
    
    def OptimalSearchTree2(f):
        initF(f)
        for i in range(n,-1,-1):
            for j in range(i,n):
                computeOptCost(i,j)
        return OptCost
    
    def initF(f):
        for i in range(0,n):
            for j in range(i,n):
                FA[i,j] = FA[i,j-1]+f[j]

    def computeOptCost(i,j):
        OptCost[i,j] = 1000
        for r in range (i,j):
            tmp = OptCost[i,r-1] + OptCost[r+1,j]
            if OptCost[i,j] > tmp:
                OptCost[i,j] = tmp
        if OptCost[i,j] == 1000:
            OptCost[i,j] = 0
        
        OptCost[i,j] = OptCost[i,j] + FA[i,j]

    OptCost = OptimalSearchTree2(f)
    return OptCost

#Gráðug smíð á tré fyrir lykla A[1..n] með tíðnir f
def greedyTree(A, f):
    gt = None
    order = np.argsort(-f)
    for i in order:
        gt = insert(gt, A[i])
    return gt

    

if __name__ == '__main__':
    #Setjum inn tíðni fylkið sem við viljum reikna
    A = [1, 2, 3, 4, 5, 6]
    f = np.array([0.15, 0.1, 0.12, 0.03, 0.2, 0.4],dtype=float)
    a = Node(3)
    print(a)
    gt = greedyTree(A,f)
    print(search(gt,5))

