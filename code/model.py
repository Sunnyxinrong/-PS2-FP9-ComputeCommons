"""Compute Commons: unit-demand inference-slot auctions. Standard library only."""
from itertools import product
import json, platform, csv
from pathlib import Path
VERSION = 'ps2-review-2026-09-27'

def auction(values, bids=None, eligible=None, capacity=2, reserve=0, credit=0):
    """Public verified eligibility; bid-independent index tie-break; zero loser payments."""
    n=len(values)
    if bids is None: bids=values
    if eligible is None: eligible=[0]*n
    if not (len(bids)==len(eligible)==n and n>0): raise ValueError('length mismatch')
    if any(type(z) not in (int,float) or not 0<=z<float('inf') for z in [*values,*bids,credit]): raise ValueError('finite nonnegative numbers required')
    if type(capacity) is not int or type(reserve) is not int or not 0<=reserve<=capacity: raise ValueError('invalid capacity or reserve')
    if any(type(e) is not int or e not in (0,1) for e in eligible): raise ValueError('public binary eligibility required')
    q=min(n,capacity-reserve)
    scores=[b+credit*e for b,e in zip(bids,eligible)]
    order=sorted(range(n),key=lambda i:(-scores[i],i))
    winners=order[:q]
    cutoff=scores[order[q]] if q<n else 0
    payments=[max(0,cutoff-credit*eligible[i]) if i in winners else 0 for i in range(n)]
    utilities=[values[i]-payments[i] if i in winners else 0 for i in range(n)]
    value=sum(values[i] for i in winners)
    benchmark=sum(sorted(values,reverse=True)[:q])
    return dict(winners=winners,payments=payments,utilities=utilities,revenue=sum(payments),firm_value=value,entrant_slots=sum(eligible[i] for i in winners),worker_reserved=reserve,firm_slots=len(winners),cutoff=cutoff,scores=scores,opportunity_cost=benchmark-value)

def verify():
    checks=0;max_gain=0;grid=range(5)
    for bids in product(grid,repeat=3):
      for reserve,credit in product(range(3),range(5)):
       elig=[0,0,1]
       a=auction(bids,eligible=elig,reserve=reserve,credit=credit)
       feasible=[x for x in product([0,1],repeat=3) if sum(x)<=2-reserve]
       assert sum(a['scores'][i] for i in a['winners'])==max(sum(s*y for s,y in zip(a['scores'],x)) for x in feasible)
       checks+=1
       assert a['revenue']>=0 and all(u>=0 for u in a['utilities']);checks+=1
       for i in range(3):
        for true_value in grid:
         vals=list(bids);vals[i]=true_value
         truthful=list(bids);truthful[i]=true_value
         baseline=auction(vals,truthful,elig,reserve=reserve,credit=credit)['utilities'][i]
         for report in grid:
          dev=list(bids);dev[i]=report
          gain=auction(vals,dev,elig,reserve=reserve,credit=credit)['utilities'][i]-baseline
          max_gain=max(max_gain,gain)
          assert gain<=0;checks+=1
    for capacity in [0,1,2,3,5]:
      for reserve in range(capacity+1):
       for credit in [0,0.1,4.5,100]:
        a=auction([0,0.5,7.25],eligible=[0,0,1],capacity=capacity,reserve=reserve,credit=credit)
        assert all(p>=0 for p in a['payments']) and all(u>=0 for u in a['utilities']);checks+=1
    return {'checks_passed':checks,'maximum_profitable_deviation_on_grid':max_gain,'grid':'3 bidders; rivals reports, own value and own report in {0,1,2,3,4}; r in {0,1,2}; credit in {0,1,2,3,4}. Independent exhaustive allocation check.'}

def main():
    v=[10,9,6];e=[0,0,1]
    treatments={name:dict(reserve=r,credit=c,**auction(v,eligible=e,reserve=r,credit=c)) for name,r,c in [('standard',0,0),('credit_only',0,4),('reserve_only',1,0),('combined',1,5)]}
    sweep=[dict(reserve=r,credit=c,**auction(v,eligible=e,reserve=r,credit=c)) for r,c in product(range(3),range(13))]
    honest=auction(v,eligible=e,reserve=1,credit=5)
    false_label=auction(v,eligible=[1,0,1],reserve=1,credit=5)
    fraud_gain=false_label['utilities'][0]-honest['utilities'][0]
    output=dict(version=VERSION,python=platform.python_version(),values=v,eligibility=e,capacity=2,treatments=treatments,sweep=sweep,verification=verify(),eligibility_stress=dict(honest=honest,false_label=false_label,gross_gain=fraud_gain,audit_threshold_if_fine_10=fraud_gain/10),evidence='Synthetic exact calculations; no human observations; no robot experiments.')
    Path('results.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    with Path('sweep.csv').open('w',newline='',encoding='utf-8') as f:
     keys=['reserve','credit','firm_value','revenue','entrant_slots','worker_reserved','opportunity_cost']
     w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:x[k] for k in keys} for x in sweep)
    print(json.dumps({k:output[k] for k in ['treatments','verification','eligibility_stress']},indent=2))

if __name__=='__main__': main()
