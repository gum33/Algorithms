
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
        else:
            if node.left is not None:
                self._insert(node.left, val)
            else:
                node.left = Node(val)
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
            
    def printTree(self):
        if(self.root is not None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node is not None):
            print(node)
            self._printTree(node.left)
            self._printTree(node.right)
        


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
    

    optTree = bTree()
    print(R)
    r = R[0,n-1]
    optTree.insert(r)
    
    #Insert left subtree
    def insertLower(i,j,r):
        x = r
        while x==r:
            if r not in R[:,j]:
                x = R[i,j]
                optTree.insert(x)
            else: j-=1
        if i+1<n:    
            if R[i+1,j] != 0:
                insertHigher(i,j,x)
        if j>0:
            print(j)
            if R[i,j-1] != 0:
                insertLower(i,j,x)
    #Insert right subtree   
    def insertHigher(i,j,r):
        x = r
        while x == r:
            if r not in R[i,:]:
                x = R[i,j]
                optTree.insert(x)
            else: i+=1
        if i+1<n:
            if R[i+1,j] != 0:
                print(R[i+1,j])
                insertHigher(i,j,x)
        if j-1<0:        
            if R[i,j-1] != 0:
                insertLower(i,j,x)
    insertLower(0,n-1,r)
    insertHigher(0,n-1,r)
    
    return OptCost, R,optTree

#Gráðug smíð á tré fyrir lykla A[1..n] með tíðnir f
def greedyTree(A, f):
    gt = bTree()
    order = np.argsort(-f)
    for i in order:
        gt.insert(A[i])
    return gt

    

if __name__ == '__main__':
    #Setjum inn tíðni fylkið sem við viljum reikna
    A = [1, 2, 3, 4, 5, 6]
    f = np.array([0.15, 0.1, 0.12, 0.03, 0.2, 0.4],dtype=float)
    gt = greedyTree(A,f)
    tree = bTree()
    tree.insert(5)
    tree.insert(2)
    
    
    
    a = Node(3)
    xd = optBinaryTree(f)
    f2 = np.array([0.5, 0.2, 0.3])
    B = [1, 2, 3]
    xd2 = optBinaryTree(f2)
    xd2[2].printTree()
    xd[2].printTree()
  
    mytree.printTree()
    print()
    print('Found %s, Depth: %s' %(mytree.search(4)))
    print()
    mytree.printTree()

    