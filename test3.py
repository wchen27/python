def r(n):
    return (pow(5,n,10**9+7)%101)+50

def ok(h,l,D,I):
    " check that the escaping trolls are exactly those in I "
    H = sum(h[i] for i in I)
    for i in I:
        if H+l[i]>D: return False
    for j in range(len(h)-1,-1,-1):
        if j not in I:
            if H+h[j]+l[j]<D: return False
            H += h[j]
    return True
 
def Q(N):
    # compute problem data
    h,l,q = [],[],[]
    for n in range(N):
        h.append(r(3*n))
        l.append(r(3*n+1))
        q.append(r(3*n+2))
    D = float(sum(h))/2**0.5

    # sort by increasing h+l
    I = sorted(range(N),key=lambda k:h[k]+l[k])
    h = [h[i] for i in I]
    l = [l[i] for i in I]
    q = [q[i] for i in I]

    H = int(D)-50 # maximum height of non-escaping trolls
    v = [0]*(H+1) # v[d] = best score for a non-escaping height equal to d
    I = [[] for d in range(H+1)]
    v[h[0]] = sum(q)-q[0]
    I[h[0]] = [0]
    # loop on number of trolls 
    for i in range(1,N): # consider trolls 0 to i included
        v0,I0 = v[:],I[:]
        for d in range(h[i],H+1):
            if v0[d-h[i]]-q[i]>v0[d]:
                v[d] = v0[d-h[i]]-q[i]
                I[d] = I0[d-h[i]]+[i]
        if sum(q)-q[i]>=v[h[i]]:
            v[h[i]] = sum(q)-q[i]
            I[h[i]] = [i]
    return max(v[d] for d in range(H+1) if ok(h,l,D,I[d]))

print(Q(1000))