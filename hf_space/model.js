(function(root){
function auction(values,bids,eligible,capacity=2,reserve=0,credit=0){
 const n=values.length;
 if(!n||bids.length!==n||eligible.length!==n||![...values,...bids,credit].every(x=>Number.isFinite(x)&&x>=0)||!Number.isInteger(capacity)||!Number.isInteger(reserve)||reserve<0||reserve>capacity||!eligible.every(x=>x===0||x===1))throw Error('Invalid inputs');
 const q=Math.min(n,capacity-reserve),scores=bids.map((b,i)=>b+credit*eligible[i]);
 const order=Array.from({length:n},(_,i)=>i).sort((a,b)=>scores[b]-scores[a]||a-b),winners=order.slice(0,q);
 const cutoff=q<n?scores[order[q]]:0;
 const payments=values.map((_,i)=>winners.includes(i)?Math.max(0,cutoff-credit*eligible[i]):0);
 const utilities=values.map((v,i)=>winners.includes(i)?v-payments[i]:0);
 return {winners,payments,utilities,revenue:payments.reduce((a,b)=>a+b,0),firm_value:winners.reduce((s,i)=>s+values[i],0),entrant_slots:winners.reduce((s,i)=>s+eligible[i],0),worker_reserved:reserve,firm_slots:winners.length,cutoff,scores,opportunity_cost:[...values].sort((a,b)=>b-a).slice(0,q).reduce((a,b)=>a+b,0)-winners.reduce((s,i)=>s+values[i],0)};
}
 if(typeof module!=='undefined')module.exports={auction};else root.computeCommons={auction};
})(typeof window!=='undefined'?window:globalThis);
