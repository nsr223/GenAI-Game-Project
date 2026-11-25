import json,itertools,re,math,statistics as st,glob,random,collections
ax=json.load(open('axes.json')); STOP=set("a an the of and in on at to with from by his her their its as is it for into over under that this one two or while but out up".split())
def toks(t): return [w for w in re.findall(r"[a-z]+",t.lower()) if w not in STOP and len(w)>2]
def sim(items):
    docs=[collections.Counter(toks(i['description'])) for i in items]; N=len(docs); df=collections.Counter(w for d in docs for w in d)
    v=[{w:c*math.log((1+N)/(1+df[w])+1) for w,c in d.items()} for d in docs]
    def cos(a,b): return sum(a[w]*b.get(w,0) for w in a)/(math.sqrt(sum(x*x for x in a.values()))*math.sqrt(sum(x*x for x in b.values())))
    return st.mean(cos(a,b) for a,b in itertools.combinations(v,2))
def m(items,axes):
    d=[sum(a[k]!=b[k] for k in axes) for a,b in itertools.combinations(items,2)]
    cap=2; over=sum(max(0,c-cap) for k in axes for c in collections.Counter(i[k] for i in items).values())
    return dict(pairs=len(d),ge4=sum(x>=4 for x in d),ge6=sum(x>=6 for x in d),mean=round(st.mean(d),2),min=min(d),repeats=over,lex=round(sim(items),3))
rows=[]
for f in sorted(glob.glob('out/*.json')):
    d=json.load(open(f)); r=m(d['rooms'],ax['room']); p=m(d['people'],ax['person']); ids=len({i['id'] for i in d['rooms']})==8 and len({i['id'] for i in d['people']})==6
    wl=[len(i['description'].split()) for i in d['rooms']+d['people']]; rows.append((f[4:6],r,p,ids,sum(25<=w<=40 for w in wl)))
for n,r,p,ids,wl in rows: print(n,'rooms',r,'people',p,'ids',ids,'len ok',wl)
for t in 'ABC':
    g=[x for x in rows if x[0][0]==t]; s=lambda k,i:[x[i][k] for x in g]
    print(t,'ge4 rooms',s('ge4',1),'people',s('ge4',2),'| ge6 rooms',s('ge6',1),'people',s('ge6',2),'| mean',s('mean',1),s('mean',2),'| repeats',s('repeats',1),s('repeats',2),'| lex',s('lex',1),s('lex',2))
random.seed(20261124); fs=sorted(glob.glob('out/*.json')); random.shuffle(fs); key={}
with open('blind.txt','w') as o:
    for n,f in enumerate(fs,1):
        key[f'S{n}']=f; d=json.load(open(f)); o.write(f'##### S{n}\n')
        for i in d['rooms']+d['people']: o.write(f"{i['id']}: {i['description']} [{i['feeling']}]\n")
json.dump(key,open('key.json','w'))
