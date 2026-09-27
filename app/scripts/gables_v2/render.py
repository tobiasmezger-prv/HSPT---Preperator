"""Portable original SVGs; inputs and accessible descriptions contain no solutions."""
import json,math,html
from pathlib import Path
OUT=Path(__file__).resolve().parents[2]/'content/staging/gables-v2'
def render(v):
 parts=[]
 def line(x,y,a,b):parts.append(f'<path d="M{x},{y} L{a},{b}" fill="none" stroke="#1e293b" stroke-width="2"/>')
 def text(x,y,s,size=18):parts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="middle">{html.escape(str(s))}</text>')
 def rect(x,y,w,h,fill='white'):parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#1e293b" stroke-width="1.5"/>')
 h=250;desc=''
 if v['type']=='grids':
  gs=v['panels'];h=190;desc='Equal cells. '+ '; '.join(f"{g['label']}: {g['rows']} rows by {g['cols']} columns; shaded cells (row-major, starting at 1): "+', '.join(str(x+1) for x in g['shaded']) for g in gs)
  for k,g in enumerate(gs):
   cell=28;x=(k+.5)*600/len(gs)-g['cols']*cell/2;text(x+g['cols']*cell/2,28,g['label'])
   for r in range(g['rows']):
    for c in range(g['cols']):rect(x+c*cell,45+r*cell,cell,cell,'#385d7a' if r*g['cols']+c in g['shaded'] else 'white')
 elif v['type']=='bars':
  h=290;desc=v['unit']+'; '+', '.join(f'{a}: {b}' for a,b in zip(v['labels'],v['values']))+f". Vertical scale 0 to {v['maximum']} in steps of {v['tick']}."
  text(300,25,v['unit']);base=240;scale=190/v['maximum'];line(60,45,60,base);line(60,base,570,base)
  for tick in range(0,v['maximum']+1,v['tick']):
   y=base-tick*scale;parts.append(f'<path d="M60,{y} H570" stroke="#cbd5e1"/>');text(38,y+5,tick,15)
  for i,(label,value) in enumerate(zip(v['labels'],v['values'])):
   x=75+i*480/len(v['labels']);rect(x,base-value*scale,65,value*scale,'#385d7a');text(x+32,267,label)
 elif v['type']=='rectangles':
  desc='Rectangles, dimensions in '+v['unit']+'. '+'; '.join(f"{g['label']}: width {g['width']}, height {g['height']}" for g in v['panels'])
  for i,g in enumerate(v['panels']):
   w=g['width']*19;hh=g['height']*19;cx=(i+.5)*600/len(v['panels']);x=cx-w/2;y=75
   text(cx,30,g['label']);rect(x,y,w,hh);text(cx,y-12,f"{g['width']} {v['unit']}");text(x+w+32,y+hh/2+5,f"{g['height']} {v['unit']}",16)
  text(300,235,'Use labeled dimensions.',14)
 elif v['type']=='angles':
  layout=v['layout'];ox=280;oy=205;rad=160
  def point(a,r):return (ox+math.cos(math.radians(a))*r,oy-math.sin(math.radians(a))*r)
  def ray(a,label):
   x,y=point(a,rad);line(ox,oy,x,y);x,y=point(a,rad+20);text(x,y+5,label)
  def arc(a,b,label,r=55):
   x,y=point(a,r);xx,yy=point(b,r);parts.append(f'<path d="M{x},{y} A{r},{r} 0 0 0 {xx},{yy}" fill="none" stroke="#526a85"/>');x,y=point((a+b)/2,r+26);text(x,y+5,label,17)
  text(ox-12,oy+23,'O');h=255
  if layout in ['straight','three']:
   ray(180,'A');ray(0,'B')
   if layout=='straight':
    a=180-v['known'];ray(a,'C');arc(a,180,str(v['known'])+'°');arc(0,a,'?');desc=f"A, O, B collinear. Ray OC lies above line AB. Angle AOC is {v['known']} degrees; angle COB is unknown."
   else:
    a=180-v['known'][0];b=a-v['known'][1];ray(a,'C');ray(b,'D');arc(a,180,str(v['known'][0])+'°',70);arc(b,a,str(v['known'][1])+'°',55);arc(0,b,'x',55);desc='A, O, B collinear; rays OC and OD are above the line in order A, C, D, B. Angles AOC = 42°, COD = 65°, DOB = x.'
  else:
   ray(0,'P');ray(90,'Q');a=v['known'] if layout=='right' else 30;ray(a,'R');parts.append(f'<path d="M{ox},{oy-18} h18 v18" fill="none" stroke="#1e293b" stroke-width="2"/>');arc(0,a,str(v['known'])+'°' if layout=='right' else 'x',70);arc(a,90,'?' if layout=='right' else '2x',70);desc='POQ is marked as a right angle. Ray OR lies inside it. '+('POR = 34°, ROQ unknown.' if layout=='right' else 'POR = x, ROQ = 2x.')
  text(300,250,'Not to scale.',13)
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 {h}" role="img" aria-label="{html.escape(desc,quote=True)}"><title>{html.escape(desc)}</title><rect width="600" height="{h}" fill="white"/><g font-family="Arial, sans-serif" fill="#172b40">'+''.join(parts)+'</g></svg>',desc

def run():
 bank=json.loads((OUT/'bank.json').read_text());assets=OUT/'assets';assets.mkdir(exist_ok=True)
 for q in bank:
  if 'visual' in q:
   svg,alt=render(q['visual']);(assets/f"{q['id']}.svg").write_text(svg);q['visual']['alt']=alt
 (OUT/'bank.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
