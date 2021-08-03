#binary search
#searches for an s in i that satisfies x == f(i[s])
#i = iterable
#f = function to call on each element of i
#x = value to search for
#start = offset into iterable to start
#end = offset into iterable to end
#if it finds a match, it returns a tuple of (s,i[s],f(i[s]))
#if it does not find a match, it returns (-1,None,None)
def bsearch(i,f,x,start=0,end=-1):
    if end == -1:
        end = len(i)-1
    #s = _bsearch(i,f,start,end,x)
    s = _bsearch2(i,f,start,end,x)
    return (s,i[s],f(i[s])) if s != -1 else (s,None,None)

#recursive
def _bsearch(i,f,lo,hi,x):
    if hi >= lo:
        md = (hi+lo)//2
        a = f(i[md])
        if a == x:
            return md
        elif a > x:
            return _bsearch(i,f,lo,md-1,x)
        else:
            return _bsearch(i,f,md+1,hi,x)
    else:
        return -1

#loop
def _bsearch2(i,f,lo,hi,x):
    while True:
        if hi >= lo:
            md = (hi+lo)//2
            a = f(i[md])
            if a == x:
                return md
            elif a > x:
                hi = md-1
            else:
                lo = md+1
        else:
            return -1
