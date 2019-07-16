#This function is the key difference of class association rules with class sequential rules
def subset(A, B):
#a sequence A=a1a2...ar  is a subsequence of another sequence B=b1b2...bm
#if there exist integers 1<=j1<j2<....<jr-1<jr<=m
#such that a1 subset of bj1, a2 subset of bj2 ... ar subset of bjr

    #initialize indexes
    i = j = 0
    #loop through the sequences
    while (i < len(A) and j < len(B)):
        if not isinstance(A[i], (tuple, list)):
            if not isinstance(B[j], (tuple, list)):
                if A[i] == B[j]:
                    i += 1
                    j += 1
                else:
                    j += 1
            else:
                if A[i] in B[j]:
                    i += 1
                    j += 1
                else:
                    j += 1
        else:
            tmp = set(A[i])
            if isinstance(B[j], (tuple, list)) and tmp.issubset(B[j]):
                i += 1
                j += 1
            else:
                j += 1

    return i == len(A)
