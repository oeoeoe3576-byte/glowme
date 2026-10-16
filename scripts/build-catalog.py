import json,pathlib,urllib.request,concurrent.futures
root=pathlib.Path(__file__).resolve().parent.parent
specs=[('the-juicy-lasting-tint','더 쥬시 래스팅 틴트','Lip','립',[
('BARE APRICOT','10 베어 애프리콧',['봄 웜'],'#ed947e'),('BARE GRAPE','03 베어 그레이프',['여름 쿨'],'#bd8395'),('EAT DOTORI','13 잇 도토리',['가을 웜'],'#995848'),('PLUM COKE','16 플럼 콕',['겨울 쿨'],'#78344c'),('ALMOND ROSE','14 아몬드 로즈',['뉴트럴 가능성'],'#ab7377')]),
('better-than-cheek','베러 댄 치크','Blush','블러셔',[('PEACH CHIP','C01 피치 칩',['봄 웜'],'#eeb09d'),('BLUEBERRY CHIP','C02 블루베리 칩',['여름 쿨','겨울 쿨'],'#c79bab'),('NUTTY NUDE','N01 너티 누드',['가을 웜','뉴트럴 가능성'],'#b78c77')]),
('better-than-palette','베러 댄 팔레트','Eyeshadow','아이섀도',[('01 Pampas Garden','01 팜파스 가든',['봄 웜'],'#cfa283'),('03 Rosebud Garden','03 로즈버드 가든',['여름 쿨','뉴트럴 가능성'],'#bc8e99'),('02 Mahogany Garden','02 마호가니 가든',['가을 웜'],'#88634c'),('07 Berry Fuchsia Garden','07 베리 푸시아 가든',['겨울 쿨'],'#a95882')])]
products=[]
for handle,name,cat,kind,variants in specs:
 d=json.loads((root/'docs'/('source-'+handle+'.json')).read_text(encoding='utf8'))
 for title,shade,seasons,color in variants:
  v=next(v for v in d['variants'] if v['title']==title); image=v['featured_image']; assert v['id'] in image['variant_ids']
  pid='romand-'+str(v['id']); products.append(dict(id=pid,brand='롬앤',name=name+' · '+shade,line=name,shadeName=shade,officialShade=title,cat=cat,kind=kind,seasons=seasons,shade=color,image='assets/products/'+pid+'.jpg',imageSource=image['src'],source='https://romandbeauty.com/products/'+handle+'?variant='+str(v['id']),variantId=v['id'],verifiedAt='2026-10-16',description='공식 색상별 상품 사진 · '+title))
def download(p):
 data=urllib.request.urlopen(p['imageSource'],timeout=45).read(); (root/p['image']).write_bytes(data); print('Downloaded',p['officialShade'],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(download,products))
(root/'data/products.js').write_text('const verifiedProducts = '+json.dumps(products,ensure_ascii=False,indent=2)+';\n',encoding='utf8')
(root/'docs/product-evidence.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf8')
