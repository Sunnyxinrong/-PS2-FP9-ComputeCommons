const assert=require('node:assert/strict');
const fs=require('node:fs');
const {example,allocate}=require('./hf_space/robot.js');
const expected=JSON.parse(fs.readFileSync('code/robot_results.json','utf8')).worked;
const ps={generic:[0,0,400,false,false],edf:[0,0,400,true,true],feasible:[0,0,400,true,false],credit:[3,0,400,true,false],reserve:[0,100,400,true,false],combined:[5,100,400,true,false]};
let count=0;for(const [name,args] of Object.entries(ps)){const got=allocate(example(),undefined,...args);for(const key of ['allocated','order','completed','payments','utilities','realized_value','revenue','usable_entrant_access','late_jobs','details']){assert.deepEqual(got[key],expected[name][key],name+' '+key);count++;}}
console.log(`${count} Python/JavaScript field comparisons passed across six treatments.`);
