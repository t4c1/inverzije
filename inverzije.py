import random
from time import clock

def generiraj(n,tip):
    if tip =="inc":
        return range(n)
    elif tip=="dec":
        return range(n,0,-1)
    elif tip=="rnd":
        res=range(n)
        random.shuffle(res)
        return res
    else:
        return tip #raise NotImplementedError

def inverzije_bf_simple(l):
    n=len(l)
    res=0
    for i in range(n):
        for j in range(i,n):
            if l[i]>l[j]:
                res+=1
    return res

def inverzije_bf(l): # ~ n**2 / 2
    """
    brute force pristop
    """
    n=len(l)
    res=0
    for i in range(n):
        for j in range(i,n):
            res+=l[i]>l[j]
    return res

def inverzije_is(l):
    """
    insertion sort, linearno iskanje, swapi, lepa koda
    """
    listlen=len(l)
    res=0
    for i in range(1,listlen):
        for j in range(i):
            if l[i]<l[j]:
                res+=i-j
                for k in range(j,i):
                    l[k],l[i]=l[i],l[k]
                break
    return res

def inverzije_is2(l):
    """
    insertion sort, bisekcija, swapi, lepa koda
    """
    listlen=len(l)
    res=0
    for i in range(1,listlen):
        start=0
        stop=i
        while start<stop:
            center=(start+stop)//2
            if l[center]<l[i]:
                start=center+1
            else:
                stop=center
        if l[start]>l[i]:
            res+=i-start
            for k in range(start,i):
                l[k],l[i]=l[i],l[k]
    return res

def inverzije_is3(l):
    """
    insertion sort, bisekcija, zamiki, lepa koda
    """
    listlen=len(l)
    res=0
    for i in range(1,listlen):
        start=0
        stop=i
        while start<stop:
            center=(start+stop)//2
            if l[center]<l[i]:
                start=center+1
            else:
                stop=center
        if l[start]>l[i]:
            res+=i-start
            tmp=l[i]
            for k in range(i,start,-1):
                l[k]=l[k-1]
            l[start]=tmp
    return res

def inverzije_dc_rek(l, start=0, end=-1):
    """
    divide & conquer pristop - mergesort, rekurzivno, z veckratno alokacijo
    """
    if end==-1:
        end=len(l)
    if end-start<=1:
        return 0

    center= (start + end) // 2
    res=inverzije_dc_rek(l, start, center)+inverzije_dc_rek(l,center,end)

    l2=[0]*len(l)
    i1=start
    i2=(start+end)//2
    end1=i2
    for outidx in range(start, end):
        if i1< end1:
            if i2<end and l[i1]>l[i2]:
                l2[outidx]=l[i2]
                i2+=1
                res+=end1-i1
            else:
                l2[outidx]=l[i1]
                i1+=1
        else:  # i2<end2
            l2[outidx]=l[i2]
            i2+=1
    for i in range(start, end):
        l[i]=l2[i]
    return res

def inverzije_dc_rek2(l,l2=None, start=0, end=-1):
    """
    divide & conquer pristop - mergesort, rekurzivno
    """
    if l2 is None:
        l2=l[:]
        end=len(l)
    if end-start<=1:
        return 0

    center= (start + end) / 2
    res=inverzije_dc_rek2(l2,l, start, center)+inverzije_dc_rek2(l2,l,center,end)

    i1=start
    i2=(start+end)//2
    end1=i2
    for outidx in range(start, end):
        if i1< end1:
            if i2<end and l[i1]>l[i2]:
                l2[outidx]=l[i2]
                i2+=1
                res+=end1-i1
            else:
                l2[outidx]=l[i1]
                i1+=1
        else:  # i2<end2
            l2[outidx]=l[i2]
            i2+=1
    for i in range(start, end):
        l[i]=l2[i]
    return res

def inverzije_dc(l):
    """
    divide & conquer pristop - mergesort
    """
    listlen = len(l)
    l2= [0] * listlen
    runl=1
    res=0
    while runl<listlen:
        #runstart=0
        for runstart in range(0,listlen,2*runl):
        #while runstart<listlen:
            i1=runstart
            i2=runstart+runl
            end1 = runstart + runl
            end2 = min(runstart + 2*runl, listlen)
            for outidx in range(runstart, min(runstart + 2*runl, listlen)):
                if i1< end1:
                    if i2<end2 and l[i1]>l[i2]:
                        l2[outidx]=l[i2]
                        i2+=1
                        res+=end1-i1
                    else:
                        l2[outidx]=l[i1]
                        i1+=1
                else:  # i2<end2
                    l2[outidx]=l[i2]
                    i2+=1
            #runstart+=runl*2
        l,l2=l2,l
        runl*=2
    #print l
    return res

all_funcs = inverzije_bf,inverzije_bf_simple,inverzije_is,inverzije_is2,inverzije_is3,inverzije_dc,inverzije_dc_rek,inverzije_dc_rek2
fast_funcs = inverzije_dc,inverzije_dc_rek,inverzije_dc_rek2
def test(n,funcs=all_funcs,gen="rnd"):
    l=generiraj(n,gen)
    for func in funcs:
        lt=l[:]
        t=clock()
        res=func(lt)
        t=clock()-t
        print "%20s: %4f   (%d)"%(func.__name__,t,res)

def find_best_test(reps=10,funcs=all_funcs,gen="rnd", max_time=1):
    funcs=list(funcs)
    ns=[]
    results={i.__name__:[] for i in funcs}
    n=1
    while funcs:
        print n, len(funcs)
        ns.append(n)
        l=generiraj(n,gen)
        for func in funcs[::-1]:#ker iz seznama lahko brisemo gremo cez v obratnem vrstnem redu!
            #lt=[l[:] for i in range(reps)]
            tmp=0
            for i in range(reps):
                lt=l[:]
                t=clock()
                res=func(lt)
                t=clock()-t
                tmp+=t
            tmp/=reps
            results[func.__name__].append(tmp)
            if tmp>max_time:
                funcs.remove(func)
        n=int(n*1.1)+1
    return results,ns

def draw_graph(res,ns):
    from matplotlib import pyplot
    f=pyplot.figure()
    #odkomentiraj za logaritmicno skalo
    #pyplot.semilogx()
    #pyplot.semilogy()
    for fn in res:
        l=pyplot.plot(ns[:len(res[fn])],res[fn],label=fn)
    pyplot.legend()
    pyplot.show()
    #TODO: name map, axis


if __name__=="__main__":
    res,ns = find_best_test(reps=10,max_time=10)
    print "%20s"%("FUNC \\ N",), "  ".join(["%8d"%(j,) for j in ns])
    for i in res:
        print "%20s"%(i,), ", ".join(["%8f"%(j,) for j in res[i]])

    draw_graph(res,ns)
    #test(1000000,(inverzije_dc,inverzije_dc_rek2))
    #test(30000,fast_funcs)
    #test(10000)