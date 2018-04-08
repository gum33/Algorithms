
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:02:49 2018

@author: Guðmundur Magnússon
"""
import numpy as np
import matplotlib.pyplot as plt
import time
from IPython.display import display
import pandas as pd



#Skilgreinum tvíundartré til að nota fyrir opt og greedy tré
class Node:
    def __init__(self, val):
            self.left = None
            self.right = None
            self.val = val
            
            
    def __str__(self):
        return 'value: %s' %self.val


class bTree:
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, val):
        self.size += 1
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
                
    #Venjuleg binary tree leit                 
    def search(self, val):
        if self.root is not None:
            return self._search(self.root, val)
        else: 
            return None
        

    def _search(self,  node, val, depth=1):
            if val == node.val:
                return node, depth

            elif val < node.val:
               return self._search(node.left, val, depth+1)
            else:
                return self._search(node.right, val, depth+1)
    
    #Einfalt print til að finna villur     
    def printTree(self):
        if(self.root is not None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node is not None):
            print(node)
            self._printTree(node.left)
            self._printTree(node.right)
        

#Fyllum inn optimal binary tré
def optBinaryTree(f):
    n = len(f)
    OptCost = np.zeros((n,n), dtype=float)
    R =  np.diag(range(1,n+1))
    FA = np.zeros((n,n), dtype=float)
    optTree = bTree()
    
    #Reiknum OptCost og R fylki
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
    
    r = R[0,n-1]
    optTree.insert(r)

    #Notum R fylkið til að raða í binary tré
    def insertLower(i,j,r):
        x = r
        while x==r and j>i-1:
            if all(k< r for k in R[0:j+1,j]):
                x = R[i,j]
                optTree.insert(x)
            else: j-=1
        if i+1<n:    
            if R[i+1,j] != 0:
                insertHigher(i,j,x)
        if j>0:
            if R[i,j-1] != 0:
                insertLower(i,j,x)
    
    def insertHigher(i,j,r):
        x = r
        while x == r and i<n:
            if all(k>r for k in R[i,i:n]):
                x = R[i,j]
                optTree.insert(x)
            else: i+=1
        if i+1<n:
            if R[i+1,j] != 0:
                insertHigher(i,j,x)
        if j>0:        
            if R[i,j-1] != 0:
                insertLower(i,j,x)
    
    insertLower(0,n-1,r)
    insertHigher(0,n-1,r)
    return optTree

#Gráðug smíð á tré fyrir lykla A[1..n] með tíðnir f
def greedyTree(f):
    A = range(1,len(f)+1)
    gt = bTree()
    order = np.argsort(-f)
    for i in order:
        gt.insert(A[i])
    return gt

    
def testSearches(n, m):
    
    p = np.transpose(np.ones(n))
    p = np.divide(p,range(1,n+1))
    np.random.shuffle(p)
    
    t0 = time.perf_counter()
    opt = optBinaryTree(p)
    t1 = time.perf_counter()
    createOpt = t1-t0
    
    gt = greedyTree(p)
    t2 = time.perf_counter()
    createGT = t2-t1
    
    Treaptree = Treap()
    for i in range (1,n+1):
        Treaptree.insert(i)
    t3 = time.perf_counter()
    createTreap = t3-t2
    
    #Smíðum lista sem við notum í leitir
    fjoldiLeita = np.multiply(m,p)
    fjoldiLeita =[int(round(x)) for x in fjoldiLeita] 
    leit = []
    for i in range(0,len(fjoldiLeita)):
        for j in range(0,fjoldiLeita[i]):
           leit.append(i+1)
        
    np.random.shuffle(leit)

    t0 = time.perf_counter()
    for i in leit:
        opt.search(i)
    t1 = time.perf_counter()
    opttime = t1-t0

    for i in leit:
        gt.search(i)
    t2 = time.perf_counter()
    gttime = t2 - t1
    
    for i in leit:
        Treaptree.search(i)
    t3 = time.perf_counter()
    Treaptime = t3-t2
    
    return createOpt, opttime,  createGT, gttime, createTreap, Treaptime    
    
if __name__ == '__main__':

    Leit100 = testSearches(100, 200000)
    Leit400 = testSearches(400, 200000)
    Leit700 = testSearches(700, 200000)
    Leit1000 = testSearches(1000, 200000)
    
    oMake = [Leit100[0] , Leit400[0], Leit700[0], Leit1000[0]]
    oLeit = [Leit100[1] , Leit400[1], Leit700[1], Leit1000[1]]
    gMake = [Leit100[2] , Leit400[2], Leit700[2], Leit1000[2]]
    gLeit = [Leit100[3] , Leit400[3], Leit700[3], Leit1000[3]]
    tMake = [Leit100[4] , Leit400[4], Leit700[4], Leit1000[4]]
    tLeit = [Leit100[5] , Leit400[5], Leit700[5], Leit1000[5]]
    
    #Teiknum
    plt.figure(0)
    ns = [100, 400, 700, 1000]
    plt.plot(ns, oMake, label = "Opt Tree")
    plt.plot(ns, gMake,label = "Greedy Tree")
    plt.plot(ns, tMake, label = "Treap")
    plt.legend(["Opt tré", "Greedy tré", "Treap"], loc="best")

    plt.title('Uppsetning gagnagrinda')
    plt.xlabel("fjöldi lykla")
    plt.ylabel("Tími (s)")
    plt.savefig("Create.png",dpi =1000)
    plt.show()
    
    plt.figure(1)
    plt.plot(ns, oLeit, label = "Opt Tree")
    plt.plot(ns, gLeit,label = "Greedy Tree")
    plt.plot(ns, tLeit, label = "Treap")
    plt.legend(["Opt tré", "Greedy tré", "Treap"], loc="best")
    
    plt.title('Leit í gagnagrind')
    plt.xlabel("fjöldi lykla")
    plt.ylabel("Tími (s)")
    plt.savefig("Leit.png",dpi =1000)
    plt.show()
    
    #Töflum
    MakeTable = np.column_stack((ns,oLeit,gLeit,tLeit))
    LeitTable = np.column_stack((ns,oMake,gMake,tMake))
    
    LT = pd.DataFrame(MakeTable, 
                      columns = ["Fjöldi lykla", "Opt tré", 
                                 "Greedy tré", "Treap"])
    MT = pd.DataFrame(LeitTable, 
                      columns = ["Fjöldi lykla", "Opt tré", 
                                 "Greedy tré", "Treap"])
    display(LT)
    display(MT)

    


    