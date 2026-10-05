(function(root){
'use strict';
function example(){return [['A',10,2,20],['B',9,4,10],['D',8,4,20],['E',6,4,20]].map(([id,value,buffer_steps,tolerance_mm])=>({id,value,buffer_steps,tolerance_mm,eligible:+(id==='E'),service_ms:200,period_ms:100,speed_mm_s:50,network_ms:0}));}
function deadline(j){return Math.min(j.buffer_steps*j.period_ms,j.speed_mm_s?1000*j.tolerance_mm/j.speed_mm_s:Infinity)-j.network_ms-(j.guard_ms||0);}
function allocate(jobs,bids=jobs.map(j=>j.value),credit=0,reserve=0,horizon=400,physical=true,edf=false){
 if(jobs.length<1||jobs.length>12||bids.length!==jobs.length||[...bids,credit,reserve,horizon].some(x=>!Number.isFinite(x)||x<0)||reserve>horizon)throw Error('Invalid inputs');
 const orderOf=s=>[...s].sort((a,b)=>deadline(jobs[a])-deadline(jobs[b])||a-b);
 const valid=s=>{let t=0;return orderOf(s).every(i=>{t+=jobs[i].service_ms;return t<=horizon-reserve&&(!physical||t<=deadline(jobs[i])+1e-9);});};
 const options=[];for(let mask=0;mask<2**jobs.length;mask++){const s=jobs.map((_,i)=>i).filter(i=>mask>>i&1);if(valid(s))options.push(s);}
 options.sort((a,b)=>{for(let i=0;i<jobs.length;i++){const d=+b.includes(i)-+a.includes(i);if(d)return d;}return 0;});
 const scores=bids.map((b,i)=>b+credit*jobs[i].eligible);const sum=s=>s.reduce((a,i)=>a+scores[i],0);
 let chosen=options.reduce((best,s)=>sum(s)>sum(best)?s:best,options[0]);
 if(edf){chosen=[];for(const i of orderOf(jobs.map((_,i)=>i)))if(valid([...chosen,i]))chosen.push(i);}
 const payments=jobs.map((_,i)=>!chosen.includes(i)||edf?0:Math.max(0,Math.max(...options.filter(s=>!s.includes(i)).map(sum))-Math.max(...options.filter(s=>s.includes(i)).map(s=>sum(s)-scores[i]))-credit*jobs[i].eligible));
 let t=0;const completed=[];const details=orderOf(chosen).map(i=>{t+=jobs[i].service_ms;const timely=t<=deadline(jobs[i])+1e-9;if(timely)completed.push(i);return {id:jobs[i].id,finish_ms:t,deadline_ms:deadline(jobs[i]),timely};});
 return {allocated:chosen.map(i=>jobs[i].id),order:orderOf(chosen).map(i=>jobs[i].id),completed:completed.map(i=>jobs[i].id),payments,utilities:jobs.map((j,i)=>j.value*+completed.includes(i)-payments[i]),realized_value:completed.reduce((s,i)=>s+jobs[i].value,0),revenue:payments.reduce((a,b)=>a+b,0),usable_entrant_access:completed.reduce((s,i)=>s+jobs[i].eligible,0),late_jobs:chosen.length-completed.length,details};
}
root.RobotModel={example,deadline,allocate};if(typeof module!=='undefined')module.exports=root.RobotModel;
})(typeof globalThis!=='undefined'?globalThis:this);
