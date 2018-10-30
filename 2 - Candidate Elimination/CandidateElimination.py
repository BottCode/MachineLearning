from copy import deepcopy

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
            find = True
            for i in list(range(len(a))):
                if (len(a[i]) <= len(h[i]) and (not (set(a[i]) >= set(h[i])))):
                    # it means hypotesis a is not comparable to h
                    find = False
                    break
            if find:
                return True

    return False

# return True iff any hyp in A is more specific than h
def hasMoreSpecific(h,A):
    for a in A:
        if a != h:
            find = True
            for i in list(range(len(a))):
                if (len(a[i]) >= len(h[i])) and (not (set(a[i]) <= set(h[i]))):
                    # it means hypotesis a is not comparable to h
                    find = False
                    break
            if find:
                return True
    return False

# we need to generalize h such that it's constraints are satisfied by d
def computeMinimalGeneralization(h,d):
    new_h = h.copy()
    for i in list(range(len(h))):
        if d[i] not in h[i]:
            new_h[i].append(d[i])
    if hasMoreGeneral(new_h,G):
        return [new_h]
    return [[]]

# we need to specialize h such that it's constraints are satisfied by d
def computeMinimalSpecialization(h,d):
    h_aux, h1 = deepcopy(h), deepcopy(h),
    specializations = []
    for i in list(range(len(h))):
        if d[i] in h[i]:
            h[i].remove(d[i])
        h_aux[i] = h[i]
        if hasMoreSpecific(h_aux, S):
            specializations.append(h_aux)
        h_aux = h1.copy()

    return specializations

# are the h's constraints satisfied by d?
def isConsistentForS(h,d):
    for i in list(range(len(h))):
            if d[i] not in h[i]:
                return False
    return True

# watchout: d is a NEGATIVE example
def isConsistentForG(h,d):
    return not isConsistentForS(h,d)

def removeHypTooGeneral(S):
    for s1 in S:
        for s2 in S:
            if s1 != s2:
                find = True
                for i in list(range(len(s1))):
                    if (len(s1[i]) <= len(s2[i]) and (not (set(s1[i]) >= set(s2[i])))): 
                        # it means hypotesis s1 is not comparable to s2
                        find = False
                        break
                if find:
                    S.remove(s1)
    return S

def removeHypTooSpecific(G):
    for g1 in G:
        for g2 in G:
            if g1!= g2:
                find = True
                for i in list(range(len(g1))):
                    if (len(g1[i]) >= len(g2[i])) and (not (set(g1[i]) <= set(g2[i]))): 
                        # it means hypotesis g1 is not comparable to g2
                        find = False
                        break
                if find:
                    G.remove(g1)
    return G

# watchout: d is a POSITIVE example
def removeInconsistentFromG(d,G):
    for g in G:
        for i in list(range(len(d))): # compare each constraint in d with its corresponding constraint in s
            if d[i] not in g[i]:      # d is posivite (and also g), but d[i] it involves values not in g[i] => g is incosistent
                G.remove(g)
                break
    return G

# watchout: d is a NEGATIVE example
def removeInconsistentFromS(d,S):
    for s in S:
        for i in list(range(len(d))): # compare each constraint in d with its corresponding constraint in s
            if d[i] not in s[i]:      # d is negative and constraint d[i] involves different values than s[i] => s is consistent
                break                 # go to constraint d[i+1] and s[i+1]
            S.remove(s)               # each constraint in d[i] involves values in s[i]. But d is negative => s is inconsistent
    return S

# CANDIDATE ELIMINATION ALGORITHM

print("Starting G ",G,"\nStarting S ",S)
for d in DATA:
    if d[1] == Yes:
        print("\ntraining with positive example: ",d[0])
        G = removeInconsistentFromG(d[0],G)
        i = 0
        for s in S:
            if not isConsistentForS(s,d[0]):
                del S[i]
                min_gen = computeMinimalGeneralization(s,d[0])
                S.extend(min_gen)
                S = removeHypTooGeneral(S)
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
