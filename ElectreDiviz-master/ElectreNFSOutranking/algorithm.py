import copy, math

from copy import deepcopy

class algorithm(object):
    
    def __init__(self, alternatives, outranking, nonoutranking, crisp):
        self.alternatives = alternatives
        self.N = len(alternatives)
        self.outranking = outranking
        self.nonoutranking = nonoutranking
        self.crisp = crisp
        
        if self.crisp == "true":
            p = [outranking, nonoutranking]
            for r in p:
                if r == None: break
                for a1 in self.alternatives:
                    if r.has_key(a1):
                        for a2 in self.alternatives:
                            if r[a1].has_key(a2):
                                r[a1][a2] = 1

    def Run(self):  
        str = {}
        wea = {}
        nfs = {}
    
        for a1 in self.alternatives:
            wea[a1] = 0
            str[a1] = 0
            for a2 in self.alternatives:
                
                if self.outranking.has_key(a1):
                    if self.outranking[a1].has_key(a2):
                        str[a1] += self.outranking[a1][a2]
                if self.outranking.has_key(a2):
                    if self.outranking[a2].has_key(a1):
                        wea[a1] += self.outranking[a2][a1]
        
        if not self.nonoutranking == None:
            for a1 in self.alternatives:
                for a2 in self.alternatives:

                    if self.nonoutranking.has_key(a2):
                        if self.nonoutranking[a2].has_key(a1):
                            str[a1] += self.nonoutranking[a2][a1]
                    if self.nonoutranking.has_key(a1):
                        if self.nonoutranking[a1].has_key(a2):
                            wea[a1] += self.nonoutranking[a1][a2]
        
        if self.crisp == "true":
            for a1 in self.alternatives:
                wea[a1] = int(wea[a1])
                str[a1] = int(str[a1])
                nfs[a1] = int(str[a1] - wea[a1])
        else:
            for a1 in self.alternatives:
                nfs[a1] = str[a1] - wea[a1]
                           
        result = [nfs, str, wea]
        return result