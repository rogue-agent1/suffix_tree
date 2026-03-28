#!/usr/bin/env python3
"""Suffix array + LCP — substring search, longest repeated substring."""
import sys
def build_suffix_array(s):
    return sorted(range(len(s)), key=lambda i: s[i:])
def build_lcp(s, sa):
    n=len(s); rank=[0]*n; lcp=[0]*n
    for i,idx in enumerate(sa): rank[idx]=i
    h=0
    for i in range(n):
        if rank[i]>0:
            j=sa[rank[i]-1]
            while i+h<n and j+h<n and s[i+h]==s[j+h]: h+=1
            lcp[rank[i]]=h
            if h>0: h-=1
    return lcp
def search(s, sa, pattern):
    lo,hi=0,len(sa)-1
    while lo<=hi:
        mid=(lo+hi)//2; suffix=s[sa[mid]:]
        if suffix[:len(pattern)]==pattern: return sa[mid]
        elif suffix<pattern: lo=mid+1
        else: hi=mid-1
    return -1
def longest_repeat(s, sa, lcp):
    mx=max(range(len(lcp)), key=lambda i:lcp[i])
    return s[sa[mx]:sa[mx]+lcp[mx]]
def cli():
    s=sys.argv[1] if len(sys.argv)>1 else "banana$"
    sa=build_suffix_array(s); lcp=build_lcp(s,sa)
    print(f"  String: {s}")
    print(f"  Suffix array: {sa}")
    print(f"  LCP: {lcp}")
    if len(s)>1: print(f"  Longest repeat: '{longest_repeat(s,sa,lcp)}'")
    pat=sys.argv[2] if len(sys.argv)>2 else "ana"
    idx=search(s,sa,pat); print(f"  Search '{pat}': {'found at '+str(idx) if idx>=0 else 'not found'}")
if __name__=="__main__": cli()
