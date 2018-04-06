<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:23:18 2018

@author: Guðmundur Magnússon
"""
import random 
import numpy as np
from time import sleep

class NodeT:
    def __init__(self, val):
            self.left = None
            self.right = None
            self.parent = None
            self.val = val
            self.freq = random.uniform(0,1)
            
    def __str__(self):
         return 'value: %s, Priority: %s' % (self.val, self.freq)

class Treap:
    
    def __init__(self):
        self.root = None
  
    def insert(self, val):
        if self.root is None:
            self.root = NodeT(val)
        else:
            self._insert(self.root, val)
       
    def _insert(self, node, val):
        
        if(node.val < val):
            if node.right is not None:
                self._insert(node.right, val)     
            else:
                
                node.right = NodeT(val)
                node.right.parent = node
                if node.right.freq > node.freq:
                    self.swapleft(node.right)
        else:
            if node.left is not None:
                self._insert(node.left, val)
            else:
                node.left = NodeT(val)
                node.left.parent = node
                if node.left.freq > node.freq:
                    self.swapright(node.left)
                                      
    def swapleft(self, node):
        grandparent = node.parent.parent
        parent = node.parent
        parent.right = node.left
        if node.left is not None:
            node.left.parent = parent
        node.parent = grandparent
        
        if grandparent is None:
            self.root = node
        elif parent is grandparent.left:
            grandparent.left = node
        else: 
            grandparent.right = node
        node.left = parent
        parent.parent = node
        if grandparent is not None:
            if(node.freq > grandparent.freq):
                if grandparent.left is node:
                    self.swapright(node)
                else:
                    self.swapleft(node)
            
        
    def swapright(self, node):
        grandparent = node.parent.parent
        parent = node.parent
        parent.left = node.right
        if node.right is not None:
            node.right.parent = parent
        node.parent = grandparent
        
        if grandparent is None:
            self.root = node
        elif parent is grandparent.left:
            grandparent.left = node
        else:
            grandparent.right = node
        node.right = parent
        parent.parent = node
        if(node.freq > grandparent.freq):
            if grandparent.left is node:
                self.swapright(node)
            else:
                self.swapleft(node)
                        
    #Treap search                   
    def search(self, val):
        if self.root is not None:
            return self._search(self.root, val)
        else: 
            return None
        
    #Regular search but new freq provided.
    def _search(self,  node, val, depth=1):
            #Found node, swap give new prio
            if val is node.val:
                freq = random.uniform(0,1)
                if freq > node.freq:
                    node.freq = freq
                    if node is self.root:
                        return node, depth
                    if (freq > node.parent.freq):
                        if(node is node.parent.right):
                            self.swapleft(node)
                        else: self.swapright(node)
                return node, depth
            
            #Keep searching
            elif val < node.val:
               return self._search(node.left, val, depth+1)
            else:
                return self._search(node.right, val, depth+1)

    #Simple print
    def printTree(self):
        if(self.root is not None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node is not None):
            print(node)
            self._printTree(node.left)
            self._printTree(node.right)
            
mytree = Treap()

for i in range(1,5):
   mytree.insert( i)

mytree.printTree()
print()
print('Found %s, Depth: %s' %(mytree.search(4)))
print()
mytree.printTree()
