# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:23:18 2018

@author: Lenovo
"""
import random 
import numpy as np

class NodeT:
    def __init__(self, val, freq=random.uniform(0,1)):
            self.left = None
            self.right = None
            self.parent = None
            self.val = val
            self.freq = freq
            
    def __str__(self):
        return 'value: ', self.val

class Treap:
    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, node, val):
        if self.root is None:
            self.root = NodeT(val)
        elif(node.val < val):
            if node.right is not None:
                self.insert(node.right, val)
            else:
                node.right = NodeT(val)
                node.right.parent = node
                if node.right.freq > node.freq:
                    self.swapright(node.right)
        else:
            if node.left is not None:
                self.insert(node.left, val)
            else:
                node.left = NodeT(val)
                node.left.parent = node
                if node.left.freq > node.freq:
                    self.swapleft(node.left)
        
    def swapleft(self, node):
        grandparent = node.parent.parent
        parent = node.parent
        parent.right, node.left = node.left, node.parent
        if(grandparent is None):
            self.root = node
        else:
            if(grandparent.right is parent):
                grandparent.right = node
                if grandparent.freq < node.freq:
                    self.swapleft(node)
            else:
                grandparent.left, node.parent = node, grandparent
                if grandparent.freq < node.freq:
                    self.swapright(node)
            
        
        
        
            
            