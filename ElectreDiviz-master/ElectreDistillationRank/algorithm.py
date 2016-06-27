import copy, math


from copy import deepcopy

from common import Vividict

class algorithm(object):
    
    def __init__(self, alternatives, downwards, upwards):
        self.alternatives = alternatives
        self.N = len(alternatives)
        self.downwards = downwards
        self.upwards = upwards
        
    def Run(self):   
        # S relation
        s = {}
        rank = (self.downwards, self.upwards)
        
        for a1 in self.alternatives:
            s[a1] = {}
            for a2 in self.alternatives:
                s[a1][a2] = 0
                
        for a1 in self.alternatives:
            for a2 in self.alternatives:
                if a1 == a2:
                    s[a1][a2] = 0
                    continue
                for i in range(2):
                    a = self.isBetter(a1, a2, rank[i])
                    b = self.isBetter(a2, a1, rank[1 - i])
                    if (a == b == 0):
                        s[a1][a2] = 1
                        break
                    if (a == b == 1):
                        s[a1][a2] = 0
                        break
                    if (a == 1) and (b <= 0):
                        s[a1][a2] = 1                   
                        break
        
   
	# Construct Rank

	r = {} 
	used = []
	for i in range(self.N):
		used.append(0)

	left = self.N
	front = 0
	while (left > 0):
		toRemove = []
		for i in range(self.N):
			if used[i] == 1: 
				continue
			passed = True
			for j in range(self.N):
				if i == j: 
					continue
				if used[j] == 1: 
					continue
				if s[self.alternatives[j]][self.alternatives[i]] == 1 and s[self.alternatives[i]][self.alternatives[j]] == 0:
					passed = False
					break
			if passed == True:
				toRemove.append(i)			
		for i in toRemove:
			r[self.alternatives[i]] = front + 1
			used[i] = 1
			left -= 1
		front += 1
        
        #Median ranking
        mo = []
        for i in range(self.N):
            mo.append(i)
            for j in xrange(i, 0, -1):
                a1 = self.alternatives[mo[j]]
                a2 = self.alternatives[mo[j - 1]]
                if r[a2] < r[a1]:
                    break
                if r[a2] > r[a1]:
                    mo[j - 1], mo[j] = mo[j], mo[j - 1]
                elif r[a2] == r[a1]:
                    d1 = self.downwards[a1] - self.downwards[a2]
                    d2 = self.upwards[a1] - self.upwards[a2]
                    if d1 + d2 < 0:
                        mo[j - 1], mo[j] = mo[j], mo[j - 1]
        
        m = {}
        p = 1
        for i in range(len(mo)):
            if i > 0:
                a1 = self.alternatives[mo[i]]
                a2 = self.alternatives[mo[i - 1]]
                if (r[a2] < r[a1]):
                    p += 1
                elif (r[a2] == r[a1]):
                    d1 = self.downwards[a1] - self.downwards[a2]
                    d2 = self.upwards[a1] - self.upwards[a2]
                    if d1 + d2 > 0:
                        p += 1 
            m[self.alternatives[mo[i]]] = p   
               
	##########################################
	intersection = Vividict()
	for a in self.alternatives:
		for b in self.alternatives:
			if s[a][b] == 1:
				intersection[a][b] = True;                       

        result = (intersection, r, m)
        return result
     
        
    def isBetter(self, A, B, ranking):
        if ranking[A] < ranking[B]:
            return 1
        elif ranking[A] == ranking[B]:
            return 0
        else:
            return -1
