import json,re,glob,itertools,statistics as st
D=json.load(open('defaults.json')); ax=json.load(open('axes.json')); tot=sum(len(v) for v in D.values())
S={f[4:6]:json.load(open(f)) for f in sorted(glob.glob('out/*.json'))}
def get(s,i): return next(x for x in S[s]['rooms']+S[s]['people'] if x['id']==i)
for s in S:
    hits=[(i,n) for i,p in D.items() for n,r in p.items() if re.search(r,get(s,i)['description'],re.I)]
    print(s,f'{len(hits)}/{tot}', hits if s[0]=='D' else '')
for t in 'ABCD':
    g=[s for s in S if s[0]==t]
    for kind,axes in (('rooms',ax['room']),('people',ax['person'])):
        ids=[x['id'] for x in S[g[0]][kind]]
        same=st.mean(sum(get(a,i)[k]==get(b,i)[k] for k in axes)/len(axes) for i in ids for a,b in itertools.combinations(g,2))
        ge6=[sum(sum(x[k]!=y[k] for k in axes)>=6 for x,y in itertools.combinations(S[s][kind],2)) for s in g]
        print(t,kind,'same axes across the 3 runs',round(same,2),'| pairs >=6 axes',ge6)
