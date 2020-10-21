#!/usr/bin/env python3

import numpy as np
import sys

def levenshtein_distance(w1, w2):
    l1, l2 = len(w1), len(w2)
    d = np.zeros((l1 + 1, l2 + 1))
    subCost = 0

    for i in range(l1 + 1):
        d[i, 0] = i
    for j in range(l2 + 1):
        d[0, j] = j

    for i in range(1, l1 + 1):
        for j in range(1, l2 + 1):
            if w1[i-1] == w2[j-1]:
                subCost = 0
            else:
                subCost = 1
            d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + subCost)
    
    return int(d[l1, l2])

def main(argv):
    if len(argv) != 3:
        print("usage : ./levenshtein_distance.py word1 word2")
    else:
        print(levenshtein_distance(argv[1], argv[2]))

if __name__ == "__main__":
    main(sys.argv)