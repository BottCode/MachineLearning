from copy import deepcopy
Any = '?'
Yes = 'Y'
No = 'N'

DATA = [
        [['sunny','warm','normal','strong','warm','same'],Yes],
        [['sunny','warm','high','strong','warm','same'],Yes],
        [['rainy','cold','high','strong','warm','change'],No],
        [['sunny','warm','high','strong','cool','change'],Yes]
]

MAP_ATTRIBUTES_VALUES = {
    'Sky': ['sunny','rainy'],
    'Temp': ['cold','warm'],
    'Humidity': ['normal','high'],
    'Wind': ['weak', 'strong'],
    'Water': ['warm', 'cool'],
    'Forecast': ['same','change']
}

sky_value =      MAP_ATTRIBUTES_VALUES['Sky']
temp_value =     MAP_ATTRIBUTES_VALUES['Temp']
humidity_value = MAP_ATTRIBUTES_VALUES['Humidity']
wind_value =     MAP_ATTRIBUTES_VALUES['Wind']
water_value =    MAP_ATTRIBUTES_VALUES['Water']
forecast_value = MAP_ATTRIBUTES_VALUES['Forecast']

# the most general hypotesis
G = [ [sky_value, temp_value, humidity_value, wind_value, water_value, forecast_value] ]
#the most specific hypotesis
S = [ [[],[],[],[],[],[]] ]

# return True iff any hyp in A is more general than h
def hasMoreGeneral(h,A):
    for a in A:
        if a != h:
            # # print(len(a),len(h))
            # # print("Comparing ",a," with ",h,"\n")
            find = True
            for i in list(range(len(a))):
                if (len(a[i]) <= len(h[i]) and (not (set(a[i]) >= set(h[i])))):
                    find = False
                    break
            if find:
                # # print(a, " is more general than ",h)
                return True

    return False

# return True iff any hyp in A is more specific than h
def hasMoreSpecific(h,A):
    # print(A)
    for a in A:
        if a != h:
            # # print(len(a),len(h))
            ## print("Comparing ",a," with ",h)
            find = True
            for i in list(range(len(a))):
                if (len(a[i]) >= len(h[i])) and (not (set(a[i]) <= set(h[i]))):
                    find = False
                    break
            if find:
                # # print(a, " is more specific than ",h)
                ## print("\n")
                return True
    ## print(a, " is NOT more specific than ",h)
    ## print("\n")
    return False

# we need to generalize h such that it's constraints are satisfied by d
def computeMinimalGeneralization(h,d):
    # print("generalizing ",h," to ",d)
    new_h = h.copy()
    for i in list(range(len(h))):
        if d[i] not in h[i]:
            new_h[i].append(d[i])
    if hasMoreGeneral(new_h,G):
        return [new_h]
    return [[]]

# we need to specialize h such that it's constraints are satisfied by d
def computeMinimalSpecialization(h,d):
    # print("Min spec from ",h, " to ",d)
    h_copy, h_aux, h1 = deepcopy(h), deepcopy(h), deepcopy(h) 
    specializations = []
    for i in list(range(len(h_copy))):
        # # print("constr is ",h_copy[i], ". d[i]: ",d[i])
        if d[i] in h_copy[i]:
            h_copy[i].remove(d[i])
        h_aux[i] = h_copy[i]
        if hasMoreSpecific(h_aux, S):
            specializations.append(h_aux)
        h_aux = h1.copy()
        ## print("final constr is ",h_copy[i],"\n")
    
    # print("sPEC ARE ",specializations)
    return specializations

# are the h's constraints satisfied by d?
def isConsistentForS(h,d):
    ## print("Analyzing h: ",h," with d: ",d,". ")
    for i in list(range(len(h))):
           # # print("comparing ",h[i]," with ",d[i])
            if d[i] not in h[i]:
                return False
    return True

def isConsistentForG(h,d):
    return not isConsistentForS(h,d)

def removeHypTooGeneral(S):
    ## print("starting S: ",S)
    for s1 in S:
        for s2 in S:
            if s1 != s2:
                find = True
                for i in list(range(len(s1))):
                    # # print("Comparing ",s1[i]," with ",s2[i],"\n")
                    if (len(s1[i]) <= len(s2[i]) and (not (set(s1[i]) >= set(s2[i])))): 
                        find = False
                        break
                if find:
                    S.remove(s1)
    ## print("final S: ",S)
    return S

def removeHypTooSpecific(G):
    ## print("starting G: ",G)
    for g1 in G:
        for g2 in G:
            if g1!= g2:
                find = True
                for i in list(range(len(g1))):
                    if (len(g1[i]) >= len(g2[i])) and (not (set(g1[i]) <= set(g2[i]))):
                        find = False
                        break
                if find:
                    G.remove(g1)
    ## print("final G: ",G)
    return G

def removeInconsistentFromG(d,G):
    for g in G:
        ## print("is ", g, " consistent with ",d," ?")
        for i in list(range(len(d))):
            ## print("compare ",h[i]," and ",a[i])
            if d[i] not in g[i]:
                ## print("No")
                G.remove(g)
                break
    return G

def removeInconsistentFromS(d,S):
    for s in S:
        # # print("is ", s, " consistent with ",d," ?")
        for i in list(range(len(d))):
           # # print("comparing ",h[i]," with ",d[i])
            if d[i] not in s[i]:
                ## print("Yes")
                break
            S.remove(s)
    return S

print("Starting G ",G,"\nStarting S ",S)
for d in DATA:
    # # print("Iterating G:",G,"\nIterating S",S,"\n")
    if d[1] == Yes:
        print("\ntraining with positive example: ",d[0])
        G = removeInconsistentFromG(d[0],G)
        i = 0
        for s in S:
            if not isConsistentForS(s,d[0]):
                del S[i]
                min_gen = computeMinimalGeneralization(s,d[0])
                # # print("MinGen is: ",min_gen,"\n")
                S.extend(min_gen)
                S = removeHypTooGeneral(S)
                # # print("S is ",S)
            i = i + 1
    else:
        print("\ntraining with negative example: ",d[0])        
        S = removeInconsistentFromS(d[0],S)
        i = 0
        for g in G:
            if not isConsistentForG(g,d[0]):
                del G[i]
                min_spec = computeMinimalSpecialization(g,d[0])
                G.extend(min_spec)
                G = removeHypTooSpecific(G)
                break
            i = i + 1
    print("Iterating G:",G,"\nIterating S",S,"\n")


print("\nFinal G ",G,"\nFinal S ",S)     
