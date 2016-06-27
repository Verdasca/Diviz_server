import copy, math

from copy import deepcopy

class algorithm(object):
    
    def __init__(self, alternatives, relation, direction, alpha, beta):
        self.alternatives = alternatives
        self.N = len(alternatives)
        self.relation = relation
        self.direction = direction
        self.alpha = alpha
        self.beta = beta
        self.map = [1 for i in range(self.N)]
        
    def Run(self):   
        result = {}
        for rank in range(self.N):
            A = self.GetAlternatives()
            c = self.GetCredibility(A, 2.0)
            if c > 0:
                while True:
                    T = deepcopy(self.relation)
                    c = self.DecreaseCredibility(A, c)
                    self.UpdateMatrix(A, T, c)
                    A = self.GetBestAlternatives(T, A)
                    if (len(A) == 1) or (c == 0.0): 
                        break;   

            for a in A:
                result[self.alternatives[a]] = rank + 1
                self.map[a] = 0
            if len(result) == self.N:
                break

        if self.direction == 'upwards':
            rank += 2
            for s in self.alternatives:
                result[s] = rank - result[s];   
            
        return result        
        
    def GetBestAlternatives(self, T, A):
        v = []
        for i in range(len(self.alternatives)):
            v.append(0)
        for x in A:
            for y in A:
                a = T[self.alternatives[x]][self.alternatives[y]]
                if a > 0:
                    v[x] += 1
                    v[y] -= 1
        best = 0
        max = 0
        if self.direction == 'upwards':
            max = self.N
        for a in A:
            if ((self.direction == 'downwards') and (v[a] > max)) or ((self.direction == 'upwards') and (v[a] < max)):
                max = v[a]
                best = i
        result = []
        for a in A:
            if v[a] == max:
                result.append(a)   
        return result
                
        
    def UpdateMatrix(self, A, T, c):
        result = []
        for x in A:
            for y in A:
                if y < x: 
                    continue
                a = T[self.alternatives[x]][self.alternatives[y]]
                b = T[self.alternatives[y]][self.alternatives[x]]                  
                con1 = 0
                con2 = 0 
                if (a <= c) or (a < b + (self.alpha * a + self.beta)):
                    con1 = 1;
                if (b <= c) or (b < a + (self.alpha * b + self.beta)):
                    con2 = 1;
                if con1 == 1:
                    T[self.alternatives[x]][self.alternatives[y]] = 0.0
                if con2 == 1:
                    T[self.alternatives[y]][self.alternatives[x]] = 0.0
                
    def DecreaseCredibility(self, A, c):
        c = c - self.GetLowerCredibility(c)
        c = self.GetCredibility(A, c)
        return c
                   
    def GetAlternatives(self):
        result = []
        for a in range(self.N):
            if self.map[a] == 1: 
                result.append(a)
        return result
        
    def GetCredibility(self, A, m):
        result = 0
        for x in A:
            for y in A:
                t = self.relation[self.alternatives[x]][self.alternatives[y]]
                if (x != y) and (t > result) and (t < m):
                    result = t
        return result
    
    def GetLowerCredibility(self, c):
         return (self.alpha * c + self.beta) 