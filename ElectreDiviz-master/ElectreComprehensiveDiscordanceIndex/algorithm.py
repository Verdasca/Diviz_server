import copy, math

from copy import deepcopy

class algorithm(object):
    
    def __init__(self, alternatives, profiles, criteria, weights, discordance):
        self.alternatives = alternatives
        self.N = len(alternatives)
        self.criteria = criteria
        self.weights = weights
        self.discordance = discordance
        self.profiles = profiles
        
    def Run(self):  

        denom = 0.0
        for c in self.criteria:
            denom += self.weights[c]
        
        second = self.alternatives
        if not self.profiles == None:
            second = self.profiles
        
        result = {}
        for a1 in self.alternatives:
            result[a1] = {}
            for a2 in second:
                result[a1][a2] = 0.0
                if a1 == a2: continue
                for c in self.criteria:
                    result[a1][a2] += self.weights[c] * self.discordance[a1][a2][c]
                result[a1][a2] /= denom
        return result