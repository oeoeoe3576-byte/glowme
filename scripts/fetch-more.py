import urllib.request,json,pathlib,concurrent.futures,sys
sys.stdout.reconfigure(encoding='utf-8')
out=pathlib.Path('docs/catalog-sources')
def fetch(page):
 try:
  p=json.load(urllib.request.urlopen('https://colourpop.com/products.json?limit=250&page='+str(page),timeout=45))['products']
  (out/('colourpop-page'+str(page)+'.json')).write_text(json.dumps(p,ensure_ascii=False),encoding='utf8');return page,len(p)
 except Exception as e:return page,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for r in pool.map(fetch,range(2,11)):print(r,flush=True)
