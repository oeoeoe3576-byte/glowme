import urllib.request,json,pathlib,concurrent.futures
out=pathlib.Path('docs/catalog-sources');out.mkdir(exist_ok=True)
sites=['romandbeauty.com','colourpop.com','misshaus.com','heimish.us','cosrx.com','beautyofjoseon.com','anua.com','purito.com','tirtir.global','fentybeauty.com','rarebeauty.com','hauslabs.com','makeupbymario.com','jonesroadbeauty.com','iliabeauty.com','tower28beauty.com']
def fetch(host):
 try:
  req=urllib.request.Request('https://'+host+'/products.json?limit=250',headers={'User-Agent':'Mozilla/5.0'})
  d=json.load(urllib.request.urlopen(req,timeout=35));p=d.get('products',[])
  (out/(host+'.json')).write_text(json.dumps(p,ensure_ascii=False),encoding='utf8')
  return host,len(p)
 except Exception as e:return host,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for r in pool.map(fetch,sites):print(r,flush=True)
