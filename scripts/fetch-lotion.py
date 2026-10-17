import urllib.request,json,pathlib,concurrent.futures,sys
sys.stdout.reconfigure(encoding='utf-8');out=pathlib.Path('docs/catalog-sources')
jobs=[('www.roseroseshop.com','collections/lotion/products.json',1),('www.roseroseshop.com','collections/makeup-base/products.json',1)]+[('www.roseroseshop.com','products.json',p) for p in range(1,9)]+[('naturerepublicusa.com','products.json',2)]
def fetch(job):
 host,path,page=job
 try:
  d=json.load(urllib.request.urlopen(urllib.request.Request('https://'+host+'/'+path+'?limit=250&page='+str(page),headers={'User-Agent':'Mozilla/5.0'}),timeout=30))['products'];key=('rrs-'+path.replace('/','-')+'-'+str(page)) if 'roserose' in host else 'nature-page2';(out/(key+'.json')).write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');return key,len(d)
 except Exception as e:return str(job),str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for x in pool.map(fetch,jobs):print(x,flush=True)
p=pathlib.Path('scripts/prepare-catalog.py');s=p.read_text(encoding='utf8').replace("'sokoglam.com':'Soko Glam'","'sokoglam.com':'Soko Glam','www.roseroseshop.com':'RRS'").replace("|\\+|eye primer","|eye primer");s=s.replace("else f.stem\n", "else 'www.roseroseshop.com' if f.stem.startswith('rrs-') else 'naturerepublicusa.com' if f.stem.startswith('nature-') else f.stem\n");s=s.replace("['sokoglam.com','peachandlily.com']","['sokoglam.com','peachandlily.com','www.roseroseshop.com']");p.write_text(s,encoding='utf8')
