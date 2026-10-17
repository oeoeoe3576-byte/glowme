import urllib.request,json,pathlib,concurrent.futures,sys
sys.stdout.reconfigure(encoding='utf-8');out=pathlib.Path('docs/catalog-sources')
sites=['milanicosmetics.com','danessamyricksbeauty.com','kyliecosmetics.com','bareminerals.com','saiehello.com','milkmakeup.com','benefitcosmetics.com','naturerepublicusa.com','etudehouse.com','us.innisfree.com','sokoglam.com']
def f(host):
 try:
  p=json.load(urllib.request.urlopen(urllib.request.Request('https://'+host+'/products.json?limit=250',headers={'User-Agent':'Mozilla/5.0'}),timeout=25))['products'];(out/(host+'.json')).write_text(json.dumps(p,ensure_ascii=False),encoding='utf8');return host,len(p)
 except Exception as e:return host,str(e)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for x in pool.map(f,sites):print(x,flush=True)
