import sys, math
sys.path.insert(0,"/tmp/claude-0/-home-user-the-other-timeline-files/0bd9b492-2d39-5628-8b8e-071d69c7e472/scratchpad/samples")
from render import font, ctext, face
from PIL import Image, ImageDraw
OUT=sys.argv[1] if len(sys.argv)>1 else "."
NAVY=(46,58,89); YEL=(255,214,10); CREAM=(250,248,240); PINK=(200,80,110); RED=(220,40,50); BLUE=(40,90,170)
def mom(d,cx,cy,r,mood="calm",t=1.0):
    d.ellipse((cx-r*1.15,cy-r*1.05,cx+r*1.15,cy+r*1.35),fill=(120,70,40))
    face(d,cx,cy,r,mood,t,skin=(250,210,175))
def heart(d,cx,cy,s,top,bot):
    # two-colour heart (UA blue/yellow) built from circles+triangle
    img=Image.new("RGBA",(int(s*2.2),int(s*2.2)),(0,0,0,0)); g=ImageDraw.Draw(img)
    S=s; ox,oy=S*1.1,S*0.9
    g.ellipse((ox-S,oy-S*0.6,ox,oy+S*0.4),fill=(255,255,255,255)); g.ellipse((ox,oy-S*0.6,ox+S,oy+S*0.4),fill=(255,255,255,255))
    g.polygon([(ox-S*0.98,oy),(ox+S*0.98,oy),(ox,oy+S*1.15)],fill=(255,255,255,255))
    mask=img.split()[3]; col=Image.new("RGBA",img.size,bot); ImageDraw.Draw(col).rectangle((0,0,img.size[0],oy),fill=top)
    return col,mask,(int(cx-ox),int(cy-oy))
# ---------- avatars 1080x1080 (TikTok crops to circle: keep content in central circle)
def avatar_A():
    im=Image.new("RGB",(1080,1080),NAVY); d=ImageDraw.Draw(im)
    d.ellipse((60,60,1020,1020),outline=YEL,width=36)
    d.rounded_rectangle((330,700,750,1000),90,fill=PINK)
    mom(d,540,500,230)
    return im
def avatar_B():
    im=Image.new("RGB",(1080,1080),YEL); d=ImageDraw.Draw(im)
    d.ellipse((90,90,990,990),fill=NAVY)
    d.rounded_rectangle((360,700,720,960),80,fill=PINK)
    mom(d,540,520,210)
    for cx,cy,top,bot in ((250,330,(0,87,183,255),(255,213,0,255)),(830,330,(255,255,255,255),(220,20,60,255))):
        col,mask,pos=heart(d,cx,cy,85,top,bot); im.paste(col,pos,mask)
    return im
def avatar_C():
    im=Image.new("RGB",(1080,1080),NAVY); d=ImageDraw.Draw(im)
    d.ellipse((150,150,930,930),fill=YEL)
    # big check mark = "без стресу"
    d.line((330,560,480,710,770,380),fill=NAVY,width=95,joint="curve")
    ctext(d,770,"PL · UA",font(70),NAVY)
    return im
for name,fn in (("avatar_A_mama",avatar_A),("avatar_B_mama_serdecka",avatar_B),("avatar_C_halochka",avatar_C)):
    im=fn(); im.save(f"{OUT}/{name}.png")
    # preview as circle
    pv=Image.new("RGB",(1080,1080),"white"); m=Image.new("L",(1080,1080),0); ImageDraw.Draw(m).ellipse((0,0,1080,1080),fill=255); pv.paste(im,(0,0),m); pv.resize((300,300)).save(f"{OUT}/_pv_{name}.png")
# ---------- banner: 3 pinned-video covers 1080x1920; profile grid shows ~3:4 centre (y 240..1680)
W,H=1080,1920; BW=W*3
big=Image.new("RGB",(BW,H),NAVY); d=ImageDraw.Draw(big)
# subtle diagonal stripes
for x in range(-H,BW,140): d.line((x,H,x+H,0),fill=(52,65,99),width=40)
cy=H//2
# left: mom waving + kids
d.rounded_rectangle((540-200,cy+120,540+200,cy+520),90,fill=PINK)
mom(d,540,cy-60,220)
d.line((540+170,cy+190,540+300,cy-60),fill=(250,210,175),width=55)
d.ellipse((540+250,cy-140,540+360,cy-30),fill=(250,210,175))
for kx,col in ((200,(90,170,220)),(890,(250,200,70))):
    d.rounded_rectangle((kx-90,cy+250,kx+90,cy+520),45,fill=col); face(d,kx,cy+170,95,"calm",1.3,skin=(255,220,185))
# middle: title
mx=W+W//2
d.rounded_rectangle((W+70,cy-420,2*W-70,cy-250),40,fill=RED)
ctext(d,cy-395,"ПОЛЬЩА",font(110),"white",cx=mx)
ctext(d,cy-200,"без стресу",font(120),YEL,cx=mx)
for i,t in enumerate(["Документи","Гроші · 800+","Робота · школа"]):
    y=cy+10+i*150
    d.rounded_rectangle((W+150,y,2*W-150,y+115),57,fill=CREAM)
    ctext(d,y+25,t,font(60),NAVY,cx=mx)
ctext(d,cy+470,"простими словами",font(54),"white",cx=mx)
# right: subscribe
rx=2*W+W//2
ctext(d,cy-400,"Нові відео",font(90),"white",cx=rx)
ctext(d,cy-290,"щодня",font(110),YEL,cx=rx)
d.rounded_rectangle((2*W+130,cy-80,3*W-130,cy+90),60,fill=YEL)
ctext(d,cy-55,"ПІДПИШИСЬ",font(88),NAVY,cx=rx)
d.polygon([(rx-90,cy+200),(rx+90,cy+200),(rx,cy+330)],fill=YEL)
ctext(d,cy+380,"@polshabezstresu",font(50),(190,200,225),cx=rx)
for i in range(3):
    big.crop((i*W,0,(i+1)*W,H)).save(f"{OUT}/banner_{i+1}_of_3.png")
# preview of profile grid (3:4 centre crop of each)
pv=Image.new("RGB",(3*360+20,480),"white")
for i in range(3):
    tile=big.crop((i*W,240,(i+1)*W,1680)).resize((360,480)); pv.paste(tile,(i*370,0))
pv.save(f"{OUT}/_pv_banner_grid.png")

# ---------- wide profile background (content drawn on 3000x1000, centred into each size)
def content():
    C=Image.new("RGBA",(3000,1000),(0,0,0,0)); d=ImageDraw.Draw(C)
    cx,cy=470,430
    d.rounded_rectangle((cx-150,cy+170,cx+150,cy+470),70,fill=PINK)
    mom(d,cx,cy,165)
    d.line((cx+130,cy+230,cx+235,cy+30),fill=(250,210,175),width=44); d.ellipse((cx+195,cy-30,cx+285,cy+60),fill=(250,210,175))
    for kx,col in ((cx-270,(90,170,220)),(cx+300,(250,200,70))):
        d.rounded_rectangle((kx-75,cy+330,kx+75,cy+520),38,fill=col); face(d,kx,cy+265,78,"calm",1.3,skin=(255,220,185))
    mx=1500
    d.rounded_rectangle((mx-370,120,mx+370,290),40,fill=RED); ctext(d,140,"ПОЛЬЩА",font(118),"white",cx=mx)
    ctext(d,320,"без стресу",font(130),YEL,cx=mx)
    for i,t in enumerate(["Документи","Гроші · 800+","Робота · школа"]):
        x0=mx-645+i*440; d.rounded_rectangle((x0,560,x0+410,665),52,fill=CREAM); ctext(d,591,t,font(42),NAVY,cx=x0+205)
    ctext(d,720,"простими словами",font(56),"white",cx=mx)
    rx=2530
    ctext(d,170,"Нові відео",font(84),"white",cx=rx); ctext(d,275,"щодня",font(110),YEL,cx=rx)
    d.rounded_rectangle((rx-330,470,rx+330,620),60,fill=YEL); ctext(d,500,"ПІДПИШИСЬ",font(72),NAVY,cx=rx)
    ctext(d,680,"@polshabezstresu",font(46),(190,200,225),cx=rx)
    return C
CT=content()
def wide(Wd,Hd,name):
    bg=Image.new("RGB",(Wd,Hd),NAVY); g=ImageDraw.Draw(bg)
    sw=max(10,Wd//60)
    for x in range(-Hd,Wd,sw*3): g.line((x,Hd,x+Hd,0),fill=(52,65,99),width=sw)
    sc=min(Wd*0.97/3000,Hd*0.9/1000); c=CT.resize((int(3000*sc),int(1000*sc)),Image.LANCZOS)
    bg.paste(c,((Wd-c.width)//2,(Hd-c.height)//2),c); bg.save(f"{OUT}/{name}.png"); return bg
pv=[wide(1920,1080,"fon_16x9_1920x1080"),wide(1500,500,"fon_3x1_1500x500")]
print("ok")
