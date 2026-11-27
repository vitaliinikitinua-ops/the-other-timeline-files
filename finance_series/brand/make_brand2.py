import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
A='/home/user/the-other-timeline-files/ep2/fonts/Anton-Regular.ttf'; M='/home/user/the-other-timeline-files/ep2/fonts/Montserrat.ttf'
def mont(s): f=ImageFont.truetype(M,s); f.set_variation_by_name('Black'); return f
def burst(w,h,cx,cy,c1,c2,n=24,rot=0):
    im=Image.new('RGB',(w,h),c1); d=ImageDraw.Draw(im); R=math.hypot(w,h)
    for i in range(n):
        if i%2: continue
        a0=rot+i*2*math.pi/n; a1=rot+(i+1)*2*math.pi/n
        d.polygon([(cx,cy),(cx+R*math.cos(a0),cy+R*math.sin(a0)),(cx+R*math.cos(a1),cy+R*math.sin(a1))],fill=c2)
    v=Image.radial_gradient('L').resize((w,h)).point(lambda x:int(x*0.55))
    return Image.composite(Image.new('RGB',(w,h),(0,0,0)),im,v)
def paste(base,path,cx,cy,height,glow=None):
    c=Image.open(path).convert('RGBA'); bb=c.getbbox(); c=c.crop(bb); s=height/c.height; c=c.resize((int(c.width*s),int(c.height*s)),Image.LANCZOS)
    P=80; cc=Image.new('RGBA',(c.width+2*P,c.height+2*P),(0,0,0,0)); cc.paste(c,(P,P)); c=cc
    x,y=int(cx-c.width/2),int(cy-c.height/2)
    if glow:
        a=c.split()[3].filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(18)); g=Image.new('RGBA',c.size,glow+(0,)); g.putalpha(a); base.alpha_composite(g,(x,y))
    sh=c.split()[3].filter(ImageFilter.MaxFilter(9)); o=Image.new('RGBA',c.size,(0,0,0,255)); o.putalpha(sh); base.alpha_composite(o,(x,y))
    base.alpha_composite(c,(x,y))
def text(d,txt,font,cx,cy,fill,stroke=12,rot=0,base=None):
    bb=d.textbbox((0,0),txt,font=font,stroke_width=stroke); w,h=bb[2]-bb[0],bb[3]-bb[1]
    if rot and base is not None:
        t=Image.new('RGBA',(w+60,h+60),(0,0,0,0)); td=ImageDraw.Draw(t); td.text((30-bb[0],30-bb[1]),txt,font=font,fill=fill,stroke_width=stroke,stroke_fill=(0,0,0))
        t=t.rotate(rot,expand=True,resample=Image.BICUBIC); base.alpha_composite(t,(int(cx-t.width/2),int(cy-t.height/2))); return
    d.text((cx-w/2-bb[0],cy-h/2-bb[1]),txt,font=font,fill=fill,stroke_width=stroke,stroke_fill=(0,0,0))
def arrow(d,x0,y0,x1,y1,col=(255,40,40),w=34):
    d.line((x0,y0,x1,y1),fill=(0,0,0),width=w+16); ang=math.atan2(y1-y0,x1-x0); L=w*2.6
    pts=[(x1+math.cos(ang)*L*0.6,y1+math.sin(ang)*L*0.6),(x1+math.cos(ang+2.4)*L,y1+math.sin(ang+2.4)*L),(x1+math.cos(ang-2.4)*L,y1+math.sin(ang-2.4)*L)]
    d.polygon(pts,fill=(0,0,0)); d.line((x0,y0,x1,y1),fill=col,width=w)
    pts2=[(x1+math.cos(ang)*L*0.45,y1+math.sin(ang)*L*0.45),(x1+math.cos(ang+2.4)*L*0.8,y1+math.sin(ang+2.4)*L*0.8),(x1+math.cos(ang-2.4)*L*0.8,y1+math.sin(ang-2.4)*L*0.8)]
    d.polygon(pts2,fill=col)
# ---------------- avatars
for name,cut,c1,c2,ring,sym in [('avatar_A_shock','cut/av_shock.png',(255,214,0),(255,150,0),(230,30,40),'$?!'),('avatar_B_money','cut/av_money.png',(40,200,110),(20,140,70),(255,214,0),'$$$')]:
    W=800; im=burst(W,W,400,400,c1,c2,28).convert('RGBA'); d=ImageDraw.Draw(im)
    for i,(x,y,s,r) in enumerate([(130,170,120,-18),(670,170,120,18),(120,620,90,12),(690,610,90,-12)]):
        text(d,'$',ImageFont.truetype(A,s),x,y,(60,230,120) if name.endswith('shock') else (255,240,120),10,rot=r,base=im)
    paste(im,cut,400,470,760,glow=(255,255,255))
    d=ImageDraw.Draw(im); d.ellipse((8,8,W-8,W-8),outline=ring,width=26)
    im.convert('RGB').save(name+'.png')
# ---------------- banner A: RICH vs BROKE
W,H=2560,1440
left=burst(W//2,H,W//2-150,H//2,(30,170,90),(20,120,60),26); right=burst(W//2,H,150,H//2,(220,40,50),(150,20,30),26)
b=Image.new('RGBA',(W,H)); b.paste(left,(0,0)); b.paste(right,(W//2,0)); d=ImageDraw.Draw(b)
d.polygon([(W//2-70,0),(W//2+70,0),(W//2+25,H*0.46),(W//2+95,H*0.46),(W//2-70,H),(W//2-15,H*0.54),(W//2-85,H*0.54)],fill=(255,214,0),outline=(0,0,0))
paste(b,'cut/rich.png',790,760,980,glow=(255,240,140))
paste(b,'cut/broke.png',1770,760,980,glow=(255,140,140))
d=ImageDraw.Draw(b)
text(d,'RICH',ImageFont.truetype(A,190),470,470,(255,255,255),14,rot=8,base=b)
text(d,'BROKE',ImageFont.truetype(A,190),2110,470,(255,255,255),14,rot=-8,base=b)
d=ImageDraw.Draw(b)
text(d,'$198,344',ImageFont.truetype(A,110),760,880,(255,240,120),10,rot=-5,base=b)
text(d,'-$12,782',ImageFont.truetype(A,110),1800,880,(255,240,240),10,rot=5,base=b)
d=ImageDraw.Draw(b)
text(d,'VS',ImageFont.truetype(A,200),W//2,760,(255,214,0),16)
d.rectangle((0,1000,W,1110),fill=(15,10,30))
text(d,'THE OTHER TIMELINE  ·  ONE CHOICE. TWO LIVES. REAL NUMBERS.',mont(48),W//2,1055,(255,255,255),5)
b.convert('RGB').save('banner_A_rich_vs_broke.png')
# ---------------- banner B: WHAT IF?! with cast + arrows
b=burst(W,H,W//2,H//2,(255,200,0),(255,140,0),36).convert('RGBA'); d=ImageDraw.Draw(b)
for path,cx,hh in [('cut/scammer.png',640,700),('cut/crypto.png',960,720),('cut/grandma.png',1600,720),('cut/landlord.png',1930,700)]:
    paste(b,path,cx,900,hh,glow=(255,255,255))
paste(b,'cut/rich.png',W//2,900,820,glow=(255,255,255))
d=ImageDraw.Draw(b)
d.rectangle((0,1000,W,1110),fill=(15,10,30))
text(d,'THE OTHER TIMELINE  ·  NEW VIDEO EVERY DAY',mont(52),W//2,1055,(255,214,0),5)
text(d,'WHAT IF...?!',ImageFont.truetype(A,200),W//2,470,(255,255,255),18,rot=-3,base=b)
d=ImageDraw.Draw(b)
arrow(d,560,420,610,580); arrow(d,2000,420,1950,580)
b.convert('RGB').save('banner_B_what_if.png')
# previews
for n in ['banner_A_rich_vs_broke','banner_B_what_if']:
    im=Image.open(n+'.png'); im.crop(((W-1546)//2,(H-423)//2,(W+1546)//2,(H+423)//2)).save('/tmp/claude-0/-home-user-the-other-timeline-files/f3ffade0-7edf-532a-8602-28fd55a8d2b9/scratchpad/'+n+'_safe.jpg',quality=85)
g=Image.new('RGB',(1280*2+20,720+400+20),(0,0,0))
g.paste(Image.open('banner_A_rich_vs_broke.png').resize((1280,720)),(0,0)); g.paste(Image.open('banner_B_what_if.png').resize((1280,720)),(1300,0))
for i,n in enumerate(['avatar_A_shock','avatar_B_money']):
    a=Image.open(n+'.png').resize((400,400)); m=Image.new('L',(400,400),0); ImageDraw.Draw(m).ellipse((0,0,400,400),fill=255); g.paste(a,(i*420,740),m)
g.save('/tmp/claude-0/-home-user-the-other-timeline-files/f3ffade0-7edf-532a-8602-28fd55a8d2b9/scratchpad/brand2_prev.jpg',quality=85)
