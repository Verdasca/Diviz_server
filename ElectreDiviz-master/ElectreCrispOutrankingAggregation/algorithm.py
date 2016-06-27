import copy, math

from copy import deepcopy
from common import Vividict

class algorithm(object):
    
    def __init__(self, alternatives, profiles, concordance, discordance):
        self.alternatives = alternatives
        self.profiles = profiles
        self.N = len(alternatives)
        self.concordance = concordance
        self.discordance = discordance
    
    def Run(self): 

        result = Vividict()

        for a1 in self.alternatives:
            #result[a1] = {}
            
            alt = self.alternatives
            if not self.profiles == None: 
                alt = self.profiles
            
            for a2 in alt:
                if not self.concordance.has_key(a1): continue
                if not self.concordance[a1].has_key(a2): continue
                if self.discordance.has_key(a1) and self.discordance[a1].has_key(a2): continue
                result[a1][a2] = True
                
        return result
                
