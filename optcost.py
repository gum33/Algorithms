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
        return 'value: %s' %self.val

#Classic simple binary tree
class bTree:
    def __init__(self):
        self.root = None
    
    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._insert(self.root, val)
       
    def _insert(self, node, val): 
        if(node.val < val):
            if node.right is not None:
                self._insert(node.right, val)     
            else:
                node.right = Node(val)
                node.right.parent = node
        else:
            if node.left is not None:
                self._insert(node.left, val)
            else:
                node.left = Node(val)
                node.left.parent = node
    #Search bTree                  
    def search(self, val):
        if self.root is not None:
            return self._search(self.root, val)
        else: 
            return None
        
    #Regular search
    def _search(self,  node, val, depth=1):
            #Found node, swap give new prio
            if val is node.val:
                return node, depth
            #Keep searching
            elif val < node.val:
               return self._search(node.left, val, depth+1)
            else:
                return self._search(node.right, val, depth+1)
        


def optBinaryTree(f):
    n = len(f)
    OptCost = np.zeros((n,n), dtype=float)
    R =  np.diag(range(1,n+1))
    FA = np.zeros((n,n), dtype=float)
    
    def OptimalSearchTree(f):
        initF(f)
        for j in range(0,n):
            for i in range(j,-1,-1):
                computeOptCost(i,j)
        
    
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
                R[i,j] = r+1
        if OptCost[i,j] == 1000:
            OptCost[i,j] = 0
        
        OptCost[i,j] = OptCost[i,j] + FA[i,j]
        
    OptimalSearchTree(f)
    
    def constructTree(R):
        optTree = bTree()
        
    return OptCost, R

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
    xd = optBinaryTree(f)
    f2 = np.array([0.5, 0.2, 0.3])
    B = [1, 2, 3]
    xd2 = optBinaryTree(f2)
    print(xd2[1])
    print(xd[0])
    gt = greedyTree(A,f)
    print(search(gt,5))
    mytree = Treap()

    for i in range(1,5):
       mytree.insert( i)
    
    mytree.printTree()
    print()
    print('Found %s, Depth: %s' %(mytree.search(4)))
    print()
    mytree.printTree()