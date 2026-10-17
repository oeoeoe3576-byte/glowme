import json,re,pathlib,collections,sys,urllib.parse
sys.stdout.reconfigure(encoding='utf-8');root=pathlib.Path('.')
ps=json.load(open('docs/catalog-candidates.json',encoding='utf8'));old=json.loads((root/'docs/product-evidence.json').read_text(encoding='utf8'))
tones=['봄 웜 라이트','봄 웜 브라이트','여름 쿨 라이트','여름 쿨 뮤트','가을 웜 뮤트','가을 웜 딥','겨울 쿨 브라이트','겨울 쿨 딥']
manual=[[0,1],[2,3],[4,5],[6,7],[3,4],[0,1],[2,3],[4,5],[0,1],[2,3],[4,5],[6,7]]
selected=[];vids=set();keys=set()
brandmap={'COSRX':'코스알엑스','ANUA':'아누아','MISSHA':'미샤','TIRTIR':'티르티르','INNISFREE':'이니스프리','ETUDE HOUSE':'에뛰드','ETUDE':'에뛰드','AESTURA':'에스트라','BEAUTY OF JOSEON':'조선미녀','SKINFOOD':'스킨푸드','CENTELLIAN 24':'센텔리안24','VT':'브이티','IUNIK':'아이유닉','COSNORI':'코스노리','HANSKIN':'한스킨','REJURAN':'리쥬란','NUMBUZIN':'넘버즈인','DALBA':'달바','BEPLAIN':'비플레인','MEDIHEAL':'메디힐','MEDICUBE':'메디큐브','La ROCHE-POSAY':'라로슈포제'}
def key(p):
 s=p['name'].lower();s=re.sub(r'\[[^]]*\]|\([^)]*\)|\b\d+(?:\.\d+)?\s*(?:fl.?oz|ml|g|oz)\b|\bnew\b|\b20\d\d\b','',s);s=re.sub(r'[^a-z0-9가-힣]','',s)
 return p['brand'].lower()+s
for i,p in enumerate(old):
 p['tones']=[tones[t] for t in manual[i]];p['imageEvidence']='variant_image';p['sourceType']='brand';p['toneEvidence']='Previously reviewed official shade family';p['undertone']='';selected.append(p);vids.add(str(p['variantId']));keys.add(key(p))
clean=[]
for p in ps:
 p['brand']=brandmap.get(p['brand'],p['brand'])
 if p['brand']=='DAISO':
  m=re.search(r'\[DAISO\]\s+([A-Z][A-Z0-9 .]+?)\s+(?:Peach|Balancing|UV|Power|Tone|Hyaffeine|Healthy|Bonyongo|Clear|Enjoy|Blur|Personal)',p['name']);p['brand']=m[1].strip() if m else '다이소 협업'
 n=p['name'].lower()
 if re.search(r'1pack|\dx\b|x\s*\d+ea|\beye\b|antiphlamine|vaseline|body|2ea|3ea|4ea|5ea|10ml\)|azelaic acid|tone cover lotion|lip essence|sachet|trial|collector|color routine|short.dated| - ca|essence & ampoule|cleanser &',n):continue
 if p['cat']=='Base' and not re.search('base|tone.up',n):continue
 if p['cat']=='Lotion' and re.search('sun |sunblock|spf',n):continue
 if p['cat']=='Lotion' and 'oil free ultra moisturizing' in n:continue
 if p['cat']=='Skin' and 'advanced snail 96' in n and any(x['cat']=='Skin' and 'advanced snail 96' in x['name'].lower() for x in clean):continue
 p['sourceType']='retailer' if any(h in p['source'] for h in ['roseroseshop','sokoglam','peachandlily']) else 'brand'
 clean.append(p)
def add(p):
 k=key(p)
 if str(p['variantId']) in vids or k in keys:return False
 if p['cat'] not in ['Lip','Blush','Eyeshadow','Foundation']:
  # One product per normalized brand/title; no size/repack variants.
  stem=re.sub(r'\s*·.*$','',p['line']).lower();stem=re.sub(r'\[[^]]*\]|\([^)]*\)|\d+(?:\.\d+)?\s*(?:ml|g)|\W','',stem)
  pk=p['brand']+'-'+stem
  if pk in keys:return False
  keys.add(pk)
 selected.append(p);vids.add(str(p['variantId']));keys.add(k);return True
for cat in ['Lip','Blush','Eyeshadow']:
 pool=[p for p in clean if p['cat']==cat]
 for tone in tones:
  for p in pool:
   if sum(tone in x['tones'] for x in selected if x['cat']==cat)>=10:break
   if tone in p['tones']:add(p)
 for p in pool:
  if sum(x['cat']==cat for x in selected)>=100:break
  add(p)
# Real shade-coded options across more than ten brands.
fp=[p for p in clean if p['cat']=='Foundation' and p['sourceType']=='brand']
for brand in sorted(set(p['brand'] for p in fp)):
 pool=[p for p in fp if p['brand']==brand];used=0
 for under in ['쿨·핑크','뉴트럴','웜·옐로','올리브']:
  for p in [p for p in pool if p['undertone']==under][:3]:
   if add(p):used+=1
 for p in pool:
  if used>=12:break
  if add(p):used+=1
for cat in ['Toner','Skin','Lotion','Base','Sunscreen','Primer','Moisturizer','Serum','Cleanser']:
 for p in clean:
  if sum(x['cat']==cat for x in selected)>=20:break
  if p['cat']==cat:add(p)
(root/'docs/catalog-selected.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2),encoding='utf8')
print('Selected',len(selected),collections.Counter(p['cat'] for p in selected))
for cat in ['Lip','Blush','Eyeshadow']:print(cat,{t:sum(t in p['tones'] for p in selected if p['cat']==cat) for t in tones})
print('Foundation',len(set(p['brand'] for p in selected if p['cat']=='Foundation')))
for cat in ['Base','Lotion']:
 print(cat,[(p['brand'],p['name']) for p in selected if p['cat']==cat])
