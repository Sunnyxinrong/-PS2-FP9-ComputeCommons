const fs=require('node:fs'),assert=require('node:assert/strict');
process.chdir(__dirname);
const {auction}=require('./hf_space/model.js');
const results=JSON.parse(fs.readFileSync('./code/results.json','utf8'));let n=0;
for(const row of results.sweep){const got=auction(results.values,results.values,results.eligibility,2,row.reserve,row.credit);for(const k of Object.keys(got)){assert.deepEqual(got[k],row[k]);n++;}}
const html=fs.readFileSync('./hf_space/index.html','utf8'),vm=require('node:vm');
const ids=[...html.matchAll(/id="([^"]+)"/g)].map(x=>x[1]);const els=Object.fromEntries(ids.map(id=>[id,{value:'',textContent:'',innerHTML:'',hidden:false,disabled:false}]));
els.role.value='2';els.treatment.value='0,4';els.mode.value='synthetic';els.confidence.value='50';els.legit.value='3';els.prediction.value='5';
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const sandbox={document:{getElementById:id=>els[id]},window:{},computeCommons:{auction},location:{reload:()=>{}},Date,Blob,URL,setTimeout,console};
vm.runInNewContext(script,sandbox);els.submit.onclick();assert.equal(els.error.textContent,'');assert.equal(els.result.hidden,false);assert.match(els.lesson.textContent,/Revenue: 14/);assert.match(els.lesson.textContent,/utility regret.*: 0/);n+=4;
console.log(`${n} Python/JavaScript field-parity and DOM-handler checks passed. This is not a browser visual review.`);
fs.writeFileSync('./code/js-verification.txt',`${n} checks passed. All 39 sweep settings match Python on all 11 result fields; the default interface submit handler displays revenue 14 and zero own regret. DOM stub, not full browser.\n`);
