const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
let src=fs.existsSync('app.js')?fs.readFileSync('app.js','utf8'):[...fs.readFileSync('index.html','utf8').matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]).filter(Boolean).join('\n');
src=src.replace(/render\(\);applyLanguage\(\);initAuth\(\);if\('serviceWorker'[\s\S]*$/,'');
const elements={},memory={};const ctx={console,structuredClone,setTimeout,clearTimeout,Date,URL,Blob,window:{},navigator:{},location:{origin:'http://localhost'},MutationObserver:class{observe(){}},localStorage:{getItem:k=>memory[k]||null,setItem:(k,v)=>memory[k]=v},document:{getElementById:id=>elements[id]||(elements[id]={innerHTML:'',value:''}),querySelector:()=>null,documentElement:{}},alert:()=>{},confirm:()=>true,scrollTo:()=>{}};
vm.createContext(ctx);
for(const file of ['data/editorial.js','data/products.js'])if(fs.existsSync(file))vm.runInContext(fs.readFileSync(file,'utf8'),ctx);
vm.runInContext(src,ctx);if(fs.existsSync('ui.js'))vm.runInContext(fs.readFileSync('ui.js','utf8'),ctx);
const run=s=>vm.runInContext(s,ctx);
let failures=0;function test(name,fn){try{fn();console.log('PASS '+name)}catch(e){failures++;console.error('FAIL '+name+' — '+e.message)}}
test('long-face response adds evidence for long face',()=>{run('faceAnswers={0:0,1:4,2:2,3:1,4:3,5:0,6:1}');const first=run('faceResult().title');assert.equal(first,'긴형')});
test('all unknown face answers remain undecided',()=>{run('faceAnswers={0:3,1:5,2:3,3:4,4:4,5:3,6:5}');assert.equal(run('faceResult().title'),'판정 보류')});
test('balanced oval responses give oval',()=>{run('faceAnswers={0:2,1:0,2:0,3:0,4:0,5:0,6:0}');assert.equal(run('faceResult().title'),'계란형')});
test('saved skin report appears in analysis list',()=>{run("state.skinAnalysis={title:'건성 경향'};sub='';renderAnalyze()");assert.match(elements.main.innerHTML,/건성 경향/)});
test('products and routine preserve across save',()=>{run("state.products=[{name:'검증용 크림',cat:'Moisturizer'}];tab='today';addRoutine(0,'am');save()");assert.equal(JSON.parse(memory.glowme_mvp_v1).am[0],'검증용 크림')});

test('backup schema includes saved skin, ratios and comments',()=>{assert.equal(run("['skinAnalysis','faceThirds','comments'].every(k=>Object.hasOwn(init,k))"),true)});
test('saved report stays visible on rerender',()=>{run("state.skinAnalysis={title:'건성 경향',answers:{0:0,1:0,2:0,3:0}};sub='saved-skin';tab='analyze';render()");assert.match(elements.main.innerHTML,/SAVED BEAUTY REPORT/)});
test('saved face ratio does not use later preferences',()=>{run('state.faceThirds=[33,34,33]');const html=run("faceStyleCards({title:'긴형',faceThirds:[45,30,25]})");assert.match(html,/45 : 30 : 25/);assert.match(html,/시스루뱅/)});
test('every face type has distinct asset and correct scoring',()=>{const cases=[['계란형',[2,0,0,0,0,0,0]],['둥근형',[1,4,0,1,3,0,2]],['긴형',[0,4,2,1,3,0,1]],['각진형',[2,3,2,3,3,1,5]],['하트형',[2,1,1,2,1,2,3]],['다이아몬드형',[2,2,1,2,2,2,4]]];for(const [expected,answers] of cases){run('faceAnswers='+JSON.stringify(Object.fromEntries(answers.map((a,i)=>[i,a]))));assert.equal(run('faceResult().title'),expected);assert.match(run('faceIllustration(faceResult())'),/image-cell/)}assert.equal(run('new Set(Object.values(faceEditorial).map(x=>x.id)).size'),6)});
test('all four skin types and unknown are distinct',()=>{for(let i=0;i<5;i++){run('skinAnswers={0:'+i+',1:'+i+',2:'+i+',3:'+i+'}');assert.equal(run('skinResult().title'),['건성 경향','지성 경향','복합성 경향','중성 경향','추가 관찰 필요'][i])}});
test('every season includes lip cheek and eye products',()=>{for(const season of ['봄 웜','여름 쿨','가을 웜','겨울 쿨','뉴트럴 가능성']){const kinds=run('verifiedProducts.filter(p=>p.seasons.includes('+JSON.stringify(season)+')).map(p=>p.cat)');for(const cat of ['Lip','Blush','Eyeshadow'])assert.ok(kinds.includes(cat))}});
test('all catalog images exist and reference exact official variant',()=>{const products=JSON.parse(run('JSON.stringify(verifiedProducts)'));for(const p of products){assert.ok(fs.existsSync(p.image));assert.ok(p.source.endsWith('variant='+p.variantId));assert.ok(p.officialShade)}});
process.exitCode=failures?1:0;
