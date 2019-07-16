#GSP algorithm for mining sequential patterns
#as described in https://books.google.gr/books?id=gfKjYuPZNUMC&pg=PA13&dq=Liu,+B.+2007.+Web+data+mining:+exploring+hyperlinks,contents,+and+usage+data.+Springer.&lr=&source=gbs_toc_r&cad=4#v=onepage&q&f=false
#Chapter 2.5

import collections as cl
import subset as ss


condsupVal = cl.defaultdict(int)    #helping dictionary to hold the actual value instead of string
def CSR_apriori(S, minsup, minconf):
    print ("Running CSR-apriori on",len(S),"data with minsup "+str(100*minsup)+"% and minconf "+str(100*minconf)+"%...")

    if not ((0 <= minsup <= 1) or (0 <= minconf <= 1)):
        raise ValueError('minsup and minconf must be a number between 0 and 1.')
    if not S:
        raise ValueError('data is empty')

    #Initialize some variables
    rulesupCount = cl.defaultdict(int)  #the support count of ruleitems
    condsupCount = cl.defaultdict(int)  #the support count of condsets
    n = 0;                              #number of sequences in S
    cands = list()                      #candidates
    F = list()                          #list of frequent items
    CSR = list()                        #list of class sequential rules
    #helpers
    lst = set()
    lst2 = list()

    #the first pass over the Data
    for sec in S:
        n += 1
        condset = sec[0]
        y = sec[1]
        for item in condset:
            i = str(item)
            condsupCount[i] += 1
            condsupVal[i] = item
            rule = concat(i, ',', y)
            lst.add((i,y))
            rulesupCount[rule] += 1

    cands.append(list(lst))
    
    #Get the frequent ruleitems and the 1-rules
    lst.clear()
    for condset,y in cands[0]:
        rule = concat(condset, ',', y)
        if (100*rulesupCount[rule]/n) >= (100*minsup):
            lst.add((condset,y))
            if (100*rulesupCount[rule]/condsupCount[condset]) >= (100*minconf):
                lst2.append(condsupVal[condset])

    F.append(list(lst))
    CSR.append(list(lst2))
    lst.clear()
    lst2 = []



    #level-wise search
    k = 1
    while(F[k-1]):
        #Get k-candidates
        cands.append(CARcandidate_gen(F[k-1],k))
        #if no candidates were found break
        if not cands[k]:
            break

        #Find new support counts
        for sec in S:
            for c in cands[k]:
                #if canditade condset is in the sequence
                if ss.subset(condsupVal[c[0]], sec[0]):
                    condsupCount[c[0]] += 1
                    #if they have the same class then count the ruleitem
                    if c[1] == sec[1]:
                        rulesupCount[concat(c[0], ',', c[1])] += 1;

        #Get the frequent ruleitems and the k-rules
        for condset,y in cands[k]:
            rule = concat(str(condset), ',', y)
            if (100*rulesupCount[rule]/n) >= (100*minsup):
                #we check for redundance
                if rulesupCount[rule]/condsupCount[condset] < 1:
                    lst.add((condset,y))
                if (100*rulesupCount[rule]/condsupCount[condset]) >= (100*minconf):
                    lst2.append(condsupVal[condset])

        F.append(list(lst))
        CSR.append(list(lst2))
        lst.clear()
        lst2 = []
        k += 1

    #return the rules
    tmp = []
    for v in CSR:
        if v != []:
            tmp += v;
    return tmp

def CARcandidate_gen(F, k):
    #cadidate generation function 
    c = list()

    #ruleitems must be in lexicografic order
    F.sort()
    #find all pairs that differ only in the last item
    i = 0
    while i < len(F):
        #The number of ruleitems to skip in the while-loop, intially set to 1
        step = 1

        #if we join (2+)-rules seperate the last item from the rest
        if k>1:
            first = F[i][0][:-1]
            last = F[i][0][-1]

        for j in range(i + 1, len(F)):
            #if we join (2+)-rules seperate the last item from the rest
            if k>1:
                first2 = F[j][0][:-1]
                last2 = F[j][0][-1]
                #We join condsets with the same class
                if F[j][1] == F[i][1] and first == first2:
                    tmp = F[i][0] + (last2,)
                    c.append((tmp,F[i][1]))
                    condsupVal[tmp] = condsupVal[F[i][0]]+(condsupVal[last2],)
                    step += 1
            else:
                if F[j][1] == F[i][1]:
                    c.append(((F[i][0],F[j][0]),F[i][1]))
                    condsupVal[(F[i][0],F[j][0])] = (condsupVal[F[i][0]],condsupVal[F[j][0]])
        i += step

    return c

def concat(a, sep, b):
    #string concatination function
    return str(a) + str(sep) + str(b)
'''
#Example run
X = [ (["sad","none"], "sad"), (["sad","sad", ["none", "sad"]], "sad"), ([["none","sad"], "but", "happy"],"happy") ]
print(CSR_apriori(X,0.1, 0.4))
'''
