from PIL import Image, ImageDraw, ImageFont
exec(open('make_brand2.py').read().split('# ---------------- avatars')[0])   # reuse helpers: burst, paste, text, arrow, mont, A, M
W,H=2560,1440; Y0,Y1=508,931; SX0,SX1=507,2053
left=burst(W//2,H,W//2-120,(Y0+Y1)//2,(30,170,90),(20,120,60),26); right=burst(W//2,H,120,(Y0+Y1)//2,(220,40,50),(150,20,30),26)
b=Image.new('RGBA',(W,H)); b.paste(left,(0,0)); b.paste(right,(W//2,0)); d=ImageDraw.Draw(b)
# lightning divider
d.polygon([(W//2-55,0),(W//2+55,0),(W//2+20,H*0.47),(W//2+80,H*0.47),(W//2-55,H),(W//2-12,H*0.53),(W//2-70,H*0.53)],fill=(255,214,0),outline=(0,0,0))
# desktop/tablet-only side cast (outside the mobile safe area)
for path,cx in [('cut/grandma.png',190),('cut/crypto.png',420)]: paste(b,path,cx,Y0+330,560,glow=(255,255,255))
for path,cx in [('cut/landlord.png',2140),('cut/scammer.png',2380)]: paste(b,path,cx,Y0+330,560,glow=(255,255,255))
# main pair inside the safe area (heads + torsos fully inside 508..931)
paste(b,'cut/rich.png',SX0+215,Y0+300,640,glow=(255,240,140))
paste(b,'cut/broke.png',SX1-215,Y0+300,640,glow=(255,140,140))
d=ImageDraw.Draw(b)
# centre block (fits ~ 800 px wide between the two characters)
text(d,'RICH',ImageFont.truetype(A,132),W//2-225,Y0+110,(255,255,255),12,rot=4,base=b)
text(d,'BROKE',ImageFont.truetype(A,132),W//2+240,Y0+110,(255,255,255),12,rot=-4,base=b)
d=ImageDraw.Draw(b)
text(d,'VS',ImageFont.truetype(A,100),W//2,Y0+120,(255,214,0),12)
d.rounded_rectangle((W//2-430,Y0+215,W//2+430,Y0+320),28,fill=(15,10,30),outline=(255,214,0),width=6)
text(d,'THE OTHER TIMELINE',ImageFont.truetype(A,86),W//2,Y0+268,(255,255,255),0)
text(d,'ONE CHOICE. TWO LIVES. REAL NUMBERS.',mont(38),W//2,Y0+372,(255,255,255),6)
b=b.convert('RGB'); b.save('banner_C_all_devices.png')
# device previews: TV full, desktop 2560x423, tablet 1855x423, mobile 1546x423
crops={'desktop':(0,Y0,W,Y1),'tablet':((W-1855)//2,Y0,(W+1855)//2,Y1),'mobile':(SX0,Y0,SX1,Y1)}
pv=Image.new('RGB',(1280,720+3*(int(423*1280/2560)+10)+400),(0,0,0)); y=0
pv.paste(b.resize((1280,720)),(0,0)); y=730
for k,(x0,y0,x1,y1) in crops.items():
    c=b.crop((x0,y0,x1,y1)); s=1280/2560 if k=='desktop' else 1280/2560*1.3
    c=c.resize((int(c.width*s),int(c.height*s))); pv.paste(c,((1280-c.width)//2,y)); ImageDraw.Draw(pv).text((6,y+4),k,fill=(255,255,0)); y+=c.height+10
pv.crop((0,0,1280,y)).save('/tmp/claude-0/-home-user-the-other-timeline-files/f3ffade0-7edf-532a-8602-28fd55a8d2b9/scratchpad/banner3_prev.jpg',quality=85)
