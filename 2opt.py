import numpy as np
import random

def randpath(gr):
    nodes = list(range(gr.shape[0]))
    random.shuffle(nodes) #Walk a random path
    length = path_length(gr,nodes)
    return length, nodes

#2-opt swap
def mixpath(gra, number):
    best_path = []
    best_length = float('inf')
    #Testing k different starting routes
    for i in range(number):
        length, path = randpath(gra)
        
        changed = True
        while changed:

            changed = False
            #Testing all swap
            for a in range(-1, gra.shape[0]):
                for b in range(a+1,gra.shape[0]):
                    new_path= path[:a]+path[a:b][::-1]+path[b:]
                    new_length = path_length(gra,new_path)
                    
                    if new_length < length:
                        length = new_length
                        path = new_path
                        changed = True
        if length<best_length:
            best_length = length
            best_path = path
    return best_length, best_path


def path_length(vert, order):
    length = 0
    for i in range(len(order)-1):
        length += vert[order[i],order[i+1]]
    length += vert[order[i+1],order[0]] #return to start
    return length

if __name__ == "__main__":
    graph = np.loadtxt("dist1.txt", dtype='i')
    print(mixpath(graph,100))   #Put in higher number for better result 