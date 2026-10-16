import urllib.request,json,pathlib,concurrent.futures
root=pathlib.Path(__file__).resolve().parent.parent
(root/'data').mkdir(exist_ok=True)
def get(handle):
 d=json.load(urllib.request.urlopen('https://romandbeauty.com/products/'+handle+'.js',timeout=45))
 (root/'docs'/('source-'+handle+'.json')).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
 print(handle,[(v['title'],v['id'],v.get('featured_image',{}).get('src')) for v in d['variants']],flush=True)
 return d
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 list(pool.map(get,['the-juicy-lasting-tint','better-than-cheek','better-than-palette']))
