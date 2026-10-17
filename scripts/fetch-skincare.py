import urllib.request,json,pathlib,concurrent.futures,sys
sys.stdout.reconfigure(encoding='utf-8');out=pathlib.Path('docs/catalog-sources')
jobs=[('sokoglam.com',i) for i in range(2,7)]+[(h,1) for h in ['peachandlily.com','laneige.com','theskinfood.us','thefaceshop.com']]
def f(job):
 h,p=job
 try:
  d=json.load(urllib.request.urlopen(urllib.request.Request('https://'+h+'/products.json?limit=250&page='+str(p),headers={'User-Agent':'Mozilla/5.0'}),timeout=30))['products'];(out/((h if p==1 else h.split('.')[0]+'-page'+str(p))+'.json')).write_text(json.dumps(d,ensure_ascii=False),encoding='utf8');return h,p,len(d)
 except Exception as e:return h,p,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for x in pool.map(f,jobs):print(x,flush=True)
