"""Exact, synthetic robot-inference admission experiment. Python standard library."""
from itertools import product, permutations
from pathlib import Path
import csv, json, random, platform, math

VERSION = 'ps2-robot-revision-2026-10-05'

def deadline(job, queue=True, freshness=True):
    """Milliseconds until queued actions expire or pose drift exceeds tolerance."""
    buffer_ms = job['buffer_steps'] * job['period_ms'] if queue else math.inf
    pose_ms = 1000 * job['tolerance_mm'] / job['speed_mm_s'] if freshness and job['speed_mm_s'] else math.inf
    return min(buffer_ms, pose_ms) - job['network_ms'] - job.get('guard_ms', 0)

def schedule(jobs, subset, horizon, physical=True):
    # Even the generic admission baseline gets EDF dispatch: isolate admission, not order.
    order = sorted(subset, key=lambda i: (deadline(jobs[i]), i))
    elapsed = 0
    for i in order:
        elapsed += jobs[i]['service_ms']
        if elapsed > horizon or (physical and elapsed > deadline(jobs[i]) + 1e-9):
            return None
    return order

def feasible_sets(jobs, horizon, physical=True):
    return [(tuple(i for i in range(len(jobs)) if mask >> i & 1), order)
            for mask in range(1 << len(jobs))
            if (order := schedule(jobs, [i for i in range(len(jobs)) if mask >> i & 1], horizon, physical)) is not None]

def allocate(jobs, bids=None, credit=0, reserve_ms=0, horizon=400, physical=True, edf=False):
    if not jobs or len(jobs)>12: raise ValueError('1..12 jobs required for exact enumeration')
    bids = [j['value'] for j in jobs] if bids is None else list(bids)
    if len(bids)!=len(jobs): raise ValueError('bid length')
    if any(not math.isfinite(x) or x<0 for x in [*bids,credit,reserve_ms,horizon]): raise ValueError('invalid number')
    if reserve_ms>horizon: raise ValueError('reserve exceeds capacity')
    for j in jobs:
        if j['eligible'] not in (0,1): raise ValueError('eligibility')
        for k in ['value','service_ms','buffer_steps','period_ms','tolerance_mm','speed_mm_s','network_ms']:
            if not math.isfinite(j[k]) or j[k]<0: raise ValueError(k)
        if j['service_ms']==0 or j['period_ms']==0: raise ValueError('positive duration required')
    capacity=horizon-reserve_ms
    options=feasible_sets(jobs,capacity,physical)
    scores=[b+credit*j['eligible'] for b,j in zip(bids,jobs)]
    # A fixed lexicographic allocation tie rule, independent of bids.
    options.sort(key=lambda z:tuple(-int(i in z[0]) for i in range(len(jobs))))
    chosen,order=max(options,key=lambda z:sum(scores[i] for i in z[0]))
    if edf:
        chosen=[]
        for i in sorted(range(len(jobs)),key=lambda i:(deadline(jobs[i]),i)):
            if schedule(jobs,chosen+[i],capacity) is not None: chosen.append(i)
        order=schedule(jobs,chosen,capacity)
    payments=[0.0]*len(jobs)
    if not edf:
        for i in chosen:
            without=max(sum(scores[j] for j in subset) for subset,_ in options if i not in subset)
            with_others=max(sum(scores[j] for j in subset if j!=i) for subset,_ in options if i in subset)
            payments[i]=max(0,without-with_others-credit*jobs[i]['eligible'])
    elapsed=0; completed=[]; details=[]; waste=0
    for i in order:
        elapsed+=jobs[i]['service_ms']
        timely=elapsed<=deadline(jobs[i])+1e-9
        if timely: completed.append(i)
        else: waste+=jobs[i]['service_ms']
        details.append(dict(id=jobs[i]['id'],finish_ms=elapsed,deadline_ms=deadline(jobs[i]),timely=timely))
    return dict(allocated=[jobs[i]['id'] for i in chosen],order=[jobs[i]['id'] for i in order],
                completed=[jobs[i]['id'] for i in completed],payments=payments,
                utilities=[j['value']*int(i in completed)-payments[i] for i,j in enumerate(jobs)],
                realized_value=sum(jobs[i]['value'] for i in completed),nominal_value=sum(jobs[i]['value'] for i in chosen),
                revenue=sum(payments),usable_entrant_access=sum(jobs[i]['eligible'] for i in completed),
                nominal_entrant_access=sum(jobs[i]['eligible'] for i in chosen),late_jobs=len(chosen)-len(completed),
                wasted_ms=waste,reserve_ms=reserve_ms,details=details)

def example():
    return [dict(id=name,value=value,eligible=int(name=='E'),service_ms=200,buffer_steps=buffer,
                 period_ms=100,tolerance_mm=tol,speed_mm_s=50,network_ms=0)
            for name,value,buffer,tol in [('A',10,2,20),('B',9,4,10),('D',8,4,20),('E',6,4,20)]]

def compare(jobs,horizon=400):
    return {name:allocate(jobs,horizon=horizon,**kw) for name,kw in [
        ('generic',dict(physical=False)),('edf',dict(edf=True)),('feasible',{}),
        ('credit',dict(credit=3)),('reserve',dict(reserve_ms=100)),('combined',dict(credit=5,reserve_ms=100))]}

def verify():
    checks=0
    # Verify EDF feasibility independently against every permutation, including non-unit times.
    for p in product([1,2],repeat=3):
      for d in product([1,2,3],repeat=3):
        js=[dict(id=str(i),value=1,eligible=i==2,service_ms=p[i],buffer_steps=d[i],period_ms=1,
                 tolerance_mm=100,speed_mm_s=0,network_ms=0) for i in range(3)]
        for mask in range(8):
          subset=[i for i in range(3) if mask>>i&1]
          brute=any(all(sum(p[j] for j in order[:k+1])<=min(4,d[i]) for k,i in enumerate(order)) for order in permutations(subset))
          assert (schedule(js,subset,4) is not None)==brute; checks+=1
    js=example()[:2]+example()[3:]
    for rivals in product(range(4),repeat=3):
      for credit in [0,1,3]:
       for reserve in [0,100,400]:
        for i in range(3):
         for v in range(4):
          case=[dict(j) for j in js];case[i]['value']=v
          honest=list(rivals);honest[i]=v
          base=allocate(case,honest,credit,reserve)['utilities'][i]
          assert base>=-1e-9;checks+=1
          for b in range(4):
           reports=list(rivals);reports[i]=b
           assert allocate(case,reports,credit,reserve)['utilities'][i]<=base+1e-9;checks+=1
    out=compare(example())
    assert [out[k]['realized_value'] for k in ['generic','edf','feasible','credit','reserve','combined']]==[10,18,18,16,10,6]; checks+=1
    return dict(assertions=checks,maximum_positive_gain=0,scope='Finite report grid; analytical proof required for all real bids.')

def run():
    rng=random.Random(206)
    samples=[]
    for seed in range(300):
        js=[dict(id=str(i),value=rng.randint(1,20),eligible=int(i>=4),service_ms=rng.choice([50,100,150,200]),
                 buffer_steps=rng.randint(1,8),period_ms=100,tolerance_mm=rng.choice([10,20,40]),
                 speed_mm_s=rng.choice([25,50,100]),network_ms=rng.choice([0,25,50])) for i in range(6)]
        for mechanism in ['generic','edf','feasible','credit']:
            kw={'physical':False} if mechanism=='generic' else {'edf':True} if mechanism=='edf' else {'credit':3} if mechanism=='credit' else {}
            row=allocate(js,horizon=600,**kw)
            samples.append(dict(instance=seed,mechanism=mechanism,**{k:row[k] for k in ['realized_value','revenue','usable_entrant_access','late_jobs','wasted_ms']}))
    summary={m:{k:sum(r[k] for r in samples if r['mechanism']==m)/300 for k in ['realized_value','revenue','usable_entrant_access','late_jobs','wasted_ms']} for m in ['generic','edf','feasible','credit']}
    paired={}
    for m in ['generic','edf']:
        a=[r['realized_value'] for r in samples if r['mechanism']=='feasible'];b=[r['realized_value'] for r in samples if r['mechanism']==m]
        diff=[x-y for x,y in zip(a,b)];mean=sum(diff)/len(diff)
        se=(sum((x-mean)**2 for x in diff)/(len(diff)-1)/len(diff))**.5
        paired[m]=dict(mean_difference=mean,mc_interval_95=[mean-1.96*se,mean+1.96*se])
    base=example(); ablations={}
    for name in ['full','no_queue','no_freshness','neither']:
        js=[dict(j) for j in base]
        if name in ['no_queue','neither']:
            for j in js:j['buffer_steps']=100
        if name in ['no_freshness','neither']:
            for j in js:j['speed_mm_s']=0
        ablations[name]=compare(js)
    stress={str(delay):allocate([dict(j,network_ms=delay) for j in base]) for delay in [0,25,50,100,150,200]}
    result=dict(version=VERSION,python=platform.python_version(),evidence='Synthetic snapshot scheduling; no trained policy, robot trials, or human observations.',
                inputs=base,worked=compare(base),verification=verify(),random_design=dict(seed=206,n_instances=300,n_robots=6,horizon_ms=600),summary=summary,paired=paired,ablations=ablations,network_stress=stress)
    output=Path(__file__).resolve().parent
    (output/'robot_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    with (output/'robot_sweep.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(samples[0]));w.writeheader();w.writerows(samples)
    print(json.dumps({k:result[k] for k in ['worked','verification','summary','paired']},indent=2))
    return result

if __name__=='__main__':run()
