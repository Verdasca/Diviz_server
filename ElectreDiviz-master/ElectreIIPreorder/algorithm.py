import copy, math

from copy import deepcopy

class algorithm(object):
    
    def __init__(self, alternatives, outranking, preorder, direction):
        self.alternatives = alternatives
        self.N = len(alternatives)
        self.outranking = outranking
        self.preorder = preorder
        self.direction = direction
        
    def Run(self):   
        result = {}
        
        
        # Parse outranking
        S = []
        for i in range(0, self.N):
            V = []
            for j in range(0, self.N):
                o = 0
                A1 = self.alternatives[i]
                if A1 in self.outranking:
                    A2 = self.alternatives[j]
                    if A2 in self.outranking.get(A1):
                        o = 1
                
                V.append(o)
            S.append(V)

        

        if (self.preorder is not None):
            max = -1
            for a in self.alternatives:
                v = self.preorder.get(a)
                if (v > max):
                    max = int(v)
            R = []
            for i in range(0, max):
                v = []
                R.append(v)
            for i in range(0, self.N):
                a = self.alternatives[i]
                r = int(self.preorder.get(a))
                R[r - 1].append(i)
            
            front= 1
            for f in R:
                mask = self.GetBinaryVector(1)
                for i in f:
                    mask[i] = 0
                sR = self.getRankFromOutranking(S, mask)
            
                for l in sR:
                    for a in l: 
                        result[self.alternatives[a]] = front
                    front = front + 1  
        else:

            R = self.getRankFromOutranking(S, None)
            front = 1
            for f in R:
                for l in f:
                    result[self.alternatives[l]] = front
                front = front + 1       

        return result   
        
    def getRankFromOutranking(self, O, mask):
        rank = []
        used = []
        left = self.N
    
        ignore = 0
        
        for i in range(0, self.N):
            used.append(0)
            if (mask is not None) and (mask[i] == 1):
                used[i] = 1
                ignore = ignore + 1
                
        left = left - ignore
    
                    
        while True:
            front = []
            for i in range(0, self.N):
                if (used[i] == 1):
                    continue
                # CHECK ID NON-PREFERRED (DOWNWARDS)
                # OR DO DONT PREFER (UPWARDS)  
                isOK = True
                     
                for j in range(0, self.N):
                    if (i == j) or (used[j] == 1):
                        continue   
                        
                    if (self.direction == 'downwards'):
                        if (O[j][i] == 1) and (O[i][j] == 0):
                            isOK = False
                            break
                        
                    elif (self.direction == 'upwards'):
                        if (O[j][i] == 0) and (O[i][j] == 1):
                            isOK = False
                            break
                
                if (isOK == True):
                    front.append(i)
                  
            for i in front:
                used[i] = 1
                left = left - 1  
            
            rank.append(front)
                
            if (left == 0):
                break        
            
        if (self.direction == 'upwards'):
            newRank = []
            l = len(rank)
            for v in range(0, l):
                newRank.append(rank[l - v - 1])
            rank = newRank
                
        return rank
        
        
    def GetBinaryMatrix(self):
        result = []
        for a in self.alternatives:
            row = []
            for b in self.alternatives:
                row.append(0)
            result.append(row)
        return result
        
    def GetBinaryVector(self, i):
        result = []
        for a in self.alternatives:
            result.append(i)
        return result
     
    def GetRealMatrix(self):
        result = []
        for a in self.alternatives:
            row = []
            for b in self.alternatives:
                row.append(0.0)
            result.append(row)
        return result 
      
      