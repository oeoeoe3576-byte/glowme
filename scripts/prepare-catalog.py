import json,pathlib,re,collections,html,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path('.')
brands={'romandbeauty.com':'롬앤','colourpop.com':'컬러팝','misshaus.com':'미샤','heimish.us':'헤이미쉬','cosrx.com':'코스알엑스','beautyofjoseon.com':'조선미녀','anua.com':'아누아','tirtir.global':'티르티르','fentybeauty.com':'펜티 뷰티','rarebeauty.com':'레어 뷰티','hauslabs.com':'하우스 랩스','makeupbymario.com':'메이크업 바이 마리오','jonesroadbeauty.com':'존스 로드','iliabeauty.com':'일리아','tower28beauty.com':'타워28','milanicosmetics.com':'밀라니','danessamyricksbeauty.com':'다네사 마이릭스','kyliecosmetics.com':'카일리 코스메틱','bareminerals.com':'베어미네랄','saiehello.com':'세이','milkmakeup.com':'밀크 메이크업','naturerepublicusa.com':'네이처리퍼블릭','us.innisfree.com':'이니스프리','sokoglam.com':'Soko Glam','www.roseroseshop.com':'RRS','peachandlily.com':'피치앤릴리','laneige.com':'라네즈','thefaceshop.com':'더페이스샵','theskinfood.us':'스킨푸드'}
labels={'Lip':'립','Blush':'블러셔','Eyeshadow':'아이섀도','Foundation':'쿠션·파운데이션','Toner':'토너','Skin':'스킨·에센스','Lotion':'로션','Moisturizer':'크림','Serum':'세럼','Sunscreen':'선크림','Base':'메이크업 베이스','Primer':'프라이머','Cleanser':'클렌저'}
def plain(x):return re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>',' ',x or ''))).strip()
def category(p):
 title=p['title'].lower();typ=p['product_type'].lower();s=title+' '+typ
 if re.search(r'lip butter|fruit fetish|lux balm|full collection|summer pack|2x|3x|1x free|2-pack|3-pack|free gift|blister|\bcard\b|toner pads|eye primer',title):return None
 if re.search(r'\b(set|duo|trio|kit|bundle|brush|puff|gift|refill|mini|travel|sample|pouch|bag|merch|mirror|sponge|body|hand|hair|eye cream|foot|mask pack|sheet mask|liner|pencil|mascara|concealer|highlighter|bronzer)\b',s):return None
 if 'lip' in s and 'cheek' in s:return 'Blush'
 if re.search('blush|cheek',s):return 'Blush'
 if re.search('eyeshadow|eye shadow|shadow|eye palette|better than palette|better than eyes',s):return 'Eyeshadow'
 if re.search('lipstick|lip tint|lip gloss|glossy lip|lippie stix|glasting|juicy lasting|lip stain|lip balm|lip oil|melting balm|lip color|lip colour',s):return 'Lip'
 if re.search(r'foundation|cushion| bb cream',s):return 'Foundation'
 if re.search(r'primer',s):return 'Primer'
 if re.search(r'glow base|makeup base|make up base|make-up base|tone.up',s):return 'Base'
 if re.search('sunscreen|sun cream|suncream|sun stick|sun milk|sun serum|sun fluid|sunblock|relief sun|sunprise|sun protect',s):return 'Sunscreen'
 if re.search('toner',s) and not re.search('pad',s):return 'Toner'
 if re.search('cream|moisturizer|moisturiser',title) and not re.search('sun|bb',title):return 'Moisturizer'
 if re.search('essence|first treatment|\bskin$',title):return 'Skin'
 if re.search('lotion|emulsion|fluid moisturizer',title):return 'Lotion'
 if re.search('serum|ampoule',s):return 'Serum'
 if re.search('cleanser|cleansing|face wash',s):return 'Cleanser'
 if re.search('cream|moisturizer|moisturiser',s):return 'Moisturizer'
 return None
rules=[('봄 웜 라이트',r'peach|apricot|light coral|pale coral|pastel|light warm|soft coral'),('봄 웜 브라이트',r'coral|orange|tangerine|bright warm|vibrant warm|tomato|warm pink|warm red'),('여름 쿨 라이트',r'light pink|pale pink|baby pink|lavender|lilac|pastel pink|cool pink|soft pink'),('여름 쿨 뮤트',r'mauve|dusty|muted pink|soft rose|cool rose|rosewood|cool nude|gray.pink'),('가을 웜 뮤트',r'beige|nude|muted|taupe|soft brown|warm rose|warm neutral|milk tea'),('가을 웜 딥',r'brown|bronze|terracotta|brick|chocolate|copper|rust|burgundy'),('겨울 쿨 브라이트',r'fuchsia|magenta|hot pink|bright pink|cherry|vibrant pink|cool red|blue.red'),('겨울 쿨 딥',r'plum|berry|wine|deep red|deep pink|burgundy|deep purple|black cherry')]
def undertone(s):
 s=s.lower()
 if re.search(r'neutral to cool',s):return '뉴트럴·쿨'
 if re.search(r'neutral to warm|\d+wn\b',s):return '뉴트럴·웜'
 if re.search(r'neutral|\d\s*n\b|\d+n\d*',s):return '뉴트럴'
 if re.search(r'warm|golden|yellow|\d\s*w\b|\d+w\d*',s):return '웜·옐로'
 if re.search(r'cool|rosy|pink undertone|\d\s*c\b|\d+c\d*',s):return '쿨·핑크'
 if 'olive' in s:return '올리브'
 return ''
products=[];seen=set();rejected=collections.Counter()
for f in root.glob('docs/catalog-sources/*.json'):
 host='colourpop.com' if f.stem.startswith('colourpop') else 'sokoglam.com' if f.stem.startswith('sokoglam') else 'www.roseroseshop.com' if f.stem.startswith('rrs-') else 'naturerepublicusa.com' if f.stem.startswith('nature-') else f.stem
 if host not in brands:continue
 for p in json.loads(f.read_text(encoding='utf8')):
  if host=='naturerepublicusa.com' and re.search('TIRTIR|BEAUTY OF JOSEON|BENETUS|FREEMAY|ANUA|Cell Fusion C',p['title'],re.I):continue
  if any(re.fullmatch(r'(?:unit|sub|product|)type:(?:kit|bundle)|category:(?:Bundles|Set)|sets \+ bundles|unittype:bundle|unittype:kit',t,re.I) for t in p.get('tags',[])):continue
  cat=category(p)
  if not cat:continue
  body=plain(p.get('body_html'));variants=p['variants'];single=len(variants)==1
  if re.search(r'shades included|kit includes|trio kit|set includes|\btrial\b|\bsachet\b|\bshort-dated\b|collector|color routine|cleanser &|essence & ampoule|lip essence|\bkits\b| - ca\b',p['title']+' '+body[:300],re.I):continue
  for v in variants:
   key=(host,v['id'])
   if key in seen or not v.get('available'):continue
   seen.add(key)
   if cat not in ['Lip','Blush','Eyeshadow','Foundation'] and v!=variants[0]:continue
   im=v.get('featured_image')
   if not im:im=next((x for x in p['images'] if v['id'] in x.get('variant_ids',[])),None)
   evidence='variant_image'
   if not im and (single or cat not in ['Lip','Blush','Eyeshadow','Foundation']):im=next(iter(p['images']),None);evidence='single_product_image'
   if not im:rejected['no_exact_image']+=1;continue
   shade=v['title'] if v['title']!='Default Title' else p['title']
   desc=plain((im.get('alt') or '')+' '+shade)
   if single:desc+=' '+re.split(r'kakadu|cherry oil|plum oil|seed oil|infused|extract|ingredients|formula|blend of|nourishing|enriched|marshmallow|cupua|shea|vitamin',body,flags=re.I)[0][:450]
   desc=re.sub(r'\bwith (?:a |an )?[^.!?;]*?flavo(?:u)?r', '', desc, flags=re.I)
   desc=re.sub(r'\b(?:not|without)\b[^.!?;]{0,100}', '', desc, flags=re.I)
   # Multi-variant product copy must not be used to classify every shade alike.
   tones=[tone for tone,pat in rules if re.search(r'\b(?:'+pat+r')\b',desc,re.I)] if cat in ['Lip','Blush','Eyeshadow'] else []
   if cat in ['Lip','Blush','Eyeshadow'] and not tones:rejected['no_shade_descriptor']+=1;continue
   under=(undertone(v['title']) or undertone(desc)) if cat=='Foundation' else ''
   if cat=='Foundation' and not under:rejected['no_undertone']+=1;continue
   pid=host.split('.')[0]+'-'+str(v['id']);title=plain(p['title']);name=title+(' · '+shade if not single or v['title']!='Default Title' else '')
   if host=='colourpop.com' and v['title']=='Default Title':line=plain(p['product_type']);name=line+' · '+title
   else:line=title
   products.append(dict(id=pid,brand=p.get('vendor',brands[host]) if host in ['sokoglam.com','peachandlily.com','www.roseroseshop.com'] else brands[host],name=name,line=line,shadeName=shade if cat in ['Lip','Blush','Eyeshadow','Foundation'] else v['title'].replace('Default Title',''),officialShade=v['title'],cat=cat,kind=labels[cat],seasons=[],tones=tones,undertone=under,image='assets/products/'+pid+'.webp',imageSource=im['src'],source='https://'+host+'/products/'+p['handle']+'?variant='+str(v['id']),variantId=v['id'],productId=p['id'],verifiedAt='2026-10-17',imageEvidence=evidence,toneEvidence=desc[:1100],description=body[:500]))
(root/'docs/catalog-candidates.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf8')
print('Candidates',len(products),collections.Counter(p['cat'] for p in products));print('Rejected',rejected)
for cat in ['Lip','Blush','Eyeshadow']:print(cat,{t:sum(t in p['tones'] for p in products if p['cat']==cat) for t,_ in rules})
print('Foundation brands',sorted(set(p['brand'] for p in products if p['cat']=='Foundation')))
