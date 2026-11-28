import math, subprocess, sys, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,DUR=1080,1920,30,8.0
N=int(FPS*DUR)
FB="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
_fc={}
def font(sz,bold=True):
    k=(sz,bold)
    if k not in _fc: _fc[k]=ImageFont.truetype(FB if bold else FR,sz)
    return _fc[k]
BRAND="Польща без стресу"
def clamp(x,a=0,b=1): return max(a,min(b,x))
def ease(x): x=clamp(x); return 1-(1-x)**3
def back(x):
    x=clamp(x); c1=1.70158; c3=c1+1
    return 1+c3*(x-1)**3+c1*(x-1)**2
def prog(t,a,b): return clamp((t-a)/(b-a))

def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if d.textlength(test,font=f)<=maxw: cur=test
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def ctext(d,y,text,f,fill,maxw=900,stroke=0,sfill=None,spacing=1.15,cx=W//2):
    lines=wrap(d,text,f,maxw); lh=int(f.size*spacing)
    for i,l in enumerate(lines):
        tw=d.textlength(l,font=f)
        d.text((cx-tw/2,y+i*lh),l,font=f,fill=fill,stroke_width=stroke,stroke_fill=sfill)
    return y+len(lines)*lh

def word_caption(d,t,start,text,y,per=0.28,f=None,maxw=920,col="white",hi=(255,214,10),stroke=8):
    """word-by-word pop caption"""
    f=f or font(74); words=text.split()
    k=int((t-start)/per)+1 if t>=start else 0
    k=min(k,len(words))
    if k<=0: return
    shown=words[:k]
    # layout full text to keep positions stable
    lines=wrap(d," ".join(words),f,maxw); lh=int(f.size*1.18)
    idx=0
    for li,l in enumerate(lines):
        lw=l.split(); tw=d.textlength(l,font=f); x=W/2-tw/2
        for w in lw:
            if idx<k:
                c=hi if idx==k-1 and k<len(words) else col
                d.text((x,y+li*lh),w,font=f,fill=c,stroke_width=stroke,stroke_fill="black")
            x+=d.textlength(w+" ",font=f); idx+=1

def brand(d,dark=False,y=150):
    f=font(34)
    txt=BRAND; tw=d.textlength(txt,font=f)
    x=W/2-tw/2-28
    d.rounded_rectangle((x,y,x+tw+56,y+62),31,fill=(0,0,0,110) if not dark else (255,255,255,170))
    d.text((x+28,y+10),txt,font=f,fill="white" if not dark else (30,30,30))

def cta(d,t,start,text,bg=(255,214,10),fg=(20,20,20)):
    p=back(prog(t,start,start+0.45))
    if p<=0: return
    f=font(60); lines=wrap(d,text,f,820); lh=72
    bw=880; bh=len(lines)*lh+70
    cx,cy=W/2,1380
    s=p
    x0=cx-bw*s/2; y0=cy-bh*s/2
    d.rounded_rectangle((x0,y0,x0+bw*s,y0+bh*s),40,fill=bg)
    if p>0.9:
        ctext(d,cy-bh/2+35,text,f,fg,maxw=820)

# ---------------- audio
SR=44100
def make_audio(events,path):
    a=np.zeros(int(SR*DUR),dtype=np.float32)
    for t,kind in events:
        i=int(t*SR)
        if kind=="pop":
            n=int(0.09*SR); tt=np.arange(n)/SR
            s=np.sin(2*np.pi*(900-5000*tt)*tt)*np.exp(-tt*45)*0.5
        elif kind=="whoosh":
            n=int(0.35*SR); tt=np.arange(n)/SR
            s=np.random.randn(n)*np.sin(np.pi*tt/0.35)*0.18
            s=np.convolve(s,np.ones(30)/30,mode="same")*3
        elif kind=="boom":
            n=int(0.5*SR); tt=np.arange(n)/SR
            s=np.sin(2*np.pi*(120-80*tt)*tt)*np.exp(-tt*7)*0.8
        elif kind=="ding":
            n=int(0.6*SR); tt=np.arange(n)/SR
            s=(np.sin(2*np.pi*1320*tt)+0.5*np.sin(2*np.pi*1980*tt))*np.exp(-tt*6)*0.25
        elif kind=="tick":
            n=int(0.03*SR); tt=np.arange(n)/SR
            s=np.sin(2*np.pi*2500*tt)*np.exp(-tt*120)*0.25
        else: continue
        e=min(len(a),i+len(s)); a[i:e]+=s[:e-i]
    # soft bed
    tt=np.arange(len(a))/SR
    bed=(np.sin(2*np.pi*110*tt)+np.sin(2*np.pi*164.8*tt)+np.sin(2*np.pi*220*tt))*0.02*(0.6+0.4*np.sin(2*np.pi*0.5*tt))
    a+=bed
    a=np.clip(a,-1,1); pcm=(a*32767).astype(np.int16)
    with wave.open(path,"wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def render(name,draw_fn,events):
    wav=f"{name}.wav"; make_audio(events,wav)
    cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",wav,
         "-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-profile:v","high","-c:a","aac","-b:a","128k","-shortest","-movflags","+faststart",f"{name}.mp4"]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(N):
        t=i/FPS
        img=draw_fn(t)
        p.stdin.write(img.convert("RGB").tobytes())
        if i==int(4.5*FPS): img.convert("RGB").save(f"{name}_frame.png")
    p.stdin.close(); p.wait(); os.remove(wav); print("done",name)

# ================= 1. MEME FACE =================
def face(d,cx,cy,r,mood,t,skin=(255,214,170)):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=skin,outline=(40,30,20),width=8)
    # hair
    d.chord((cx-r,cy-r-10,cx+r,cy+r*0.4),180,360,fill=(70,45,30))
    ey=cy-r*0.15; ex=r*0.38
    blink= (t%3.0)<0.12 and mood=="calm"
    if mood=="shock":
        er=r*0.26
        for sx in (-1,1):
            d.ellipse((cx+sx*ex-er,ey-er,cx+sx*ex+er,ey+er),fill="white",outline=(40,30,20),width=6)
            d.ellipse((cx+sx*ex-er*0.25,ey-er*0.25,cx+sx*ex+er*0.25,ey+er*0.25),fill="black")
        # eyebrows up
        for sx in (-1,1):
            d.line((cx+sx*ex-r*0.2,ey-r*0.42,cx+sx*ex+r*0.2,ey-r*0.5),fill=(40,30,20),width=10)
        mr=r*0.2
        d.ellipse((cx-mr,cy+r*0.35-mr*1.2,cx+mr,cy+r*0.35+mr*1.2),fill=(90,20,20),outline=(40,30,20),width=6)
    else:
        er=r*0.12
        for sx in (-1,1):
            if blink: d.line((cx+sx*ex-er,ey,cx+sx*ex+er,ey),fill="black",width=8)
            else: d.ellipse((cx+sx*ex-er,ey-er,cx+sx*ex+er,ey+er),fill="black")
            d.line((cx+sx*ex-r*0.18,ey-r*0.3,cx+sx*ex+r*0.18,ey-r*0.3),fill=(40,30,20),width=9)
        d.arc((cx-r*0.35,cy+r*0.05,cx+r*0.35,cy+r*0.55),20,160,fill=(40,30,20),width=9)

def v1(t):
    img=Image.new("RGB",(W,H),(46,58,89)); d=ImageDraw.Draw(img,"RGBA")
    # office wall + counter
    d.rectangle((0,1150,W,H),fill=(120,90,70))
    d.rectangle((0,1120,W,1160),fill=(90,65,50))
    # sign URZĄD
    d.rounded_rectangle((300,330,780,440),20,fill=(220,40,50))
    ctext(d,350,"URZĄD",font(70),"white")
    # clerk window
    d.rectangle((640,560,1010,1120),fill=(180,210,230),outline=(60,70,90),width=10)
    face(d,825,860,110,"calm",t+1,skin=(240,200,160))
    d.rectangle((715,970,935,1120),fill=(60,90,140))
    shock=t>=3.6
    sh= (math.sin(t*90)*14*(1-prog(t,3.6,4.3))) if shock else 0
    zoom=1+0.12*ease(prog(t,3.6,3.9))
    r=int(170*zoom)
    cx=300+sh; cy=880
    d.rectangle((cx-150,cy+r-20,cx+150,1150),fill=(240,170,40))
    face(d,cx,cy,r,"shock" if shock else "calm",t)
    if shock and t<4.6:
        for i in range(10):
            a=i*math.pi/5+t*2; d.line((cx+math.cos(a)*(r+40),cy+math.sin(a)*(r+40),cx+math.cos(a)*(r+90),cy+math.sin(a)*(r+90)),fill=(255,214,10),width=10)
    # speech bubble clerk
    if 1.8<=t:
        p=back(prog(t,1.8,2.2)); 
        if p>0:
            bx,by,bw,bh=520,620,520,150
            d.rounded_rectangle((bx+bw/2-bw*p/2,by,bx+bw/2+bw*p/2,by+bh*p),30,fill="white")
            if p>0.9: ctext(d,by+22,"Brakuje jednego dokumentu",font(44),(20,20,20),maxw=470,cx=bx+bw//2)
    brand(d)
    word_caption(d,t,0.2,"Коли в ужонді кажуть:",470,per=0.25,f=font(64))
    if t<6.2: pass
    cta(d,t,6.2,"Список усіх документів — у профілі")
    return img
E1=[(0.2,"tick"),(0.45,"tick"),(0.7,"tick"),(1.8,"pop"),(3.6,"boom"),(6.2,"ding")]

# ================= 2. CHAT =================
MSGS=[(0.6,"in","Мама","Синку, гроші дійшли?"),(2.0,"out","","Відправив через банк"),(3.4,"in","Мама","Прийшло на 120 грн менше..."),(4.8,"out","","ЩО?!"),]
def v2(t):
    img=Image.new("RGB",(W,H),(229,221,213)); d=ImageDraw.Draw(img,"RGBA")
    # pattern
    for yy in range(0,H,120):
        for xx in range((yy//120)%2*60,W,120): d.ellipse((xx,yy,xx+10,yy+10),fill=(210,200,190))
    # header
    d.rectangle((0,0,W,300),fill=(7,94,84))
    d.ellipse((60,170,160,270),fill=(250,200,120)); ctext(d,195,"М",font(50),(7,94,84),cx=110)
    d.text((190,180),"Мама",font=font(52),fill="white"); 
    typing=any(0<(m[0]-t)<0.6 and m[1]=="in" for m in MSGS)
    d.text((190,245),"друкує..." if typing else "онлайн",font=font(32,False),fill=(200,235,230))
    y=420
    for st,side,who,txt in MSGS:
        if t<st: break
        p=back(prog(t,st,st+0.3))
        f=font(54 if txt!="ЩО?!" else 90,False if txt!="ЩО?!" else True)
        lines=wrap(d,txt,f,640); lh=int(f.size*1.25)
        bw=max(d.textlength(l,font=f) for l in lines)+70; bh=len(lines)*lh+50
        x= 50 if side=="in" else W-50-bw
        col=(255,255,255) if side=="in" else (220,248,198)
        s=p; ox=x if side=="in" else x+bw
        x0=ox if side=="in" else ox-bw*s
        d.rounded_rectangle((x0,y,x0+bw*s,y+bh*s),30,fill=col)
        if p>0.85:
            for i,l in enumerate(lines): d.text((x+35,y+25+i*lh),l,font=f,fill=(20,20,20) if txt!="ЩО?!" else (200,20,20))
        y+=bh+40
    if t>=6.0:
        d.rectangle((0,0,W,H),fill=(0,0,0,int(140*ease(prog(t,6.0,6.3)))))
    brand(d,y=320)
    cta(d,t,6.1,"Як переказувати дешевше — у профілі")
    return img
E2=[(0.6,"pop"),(2.0,"pop"),(3.4,"pop"),(4.8,"boom"),(6.1,"ding")]

# ================= 3. DOODLE =================
def partial_line(d,pts,p,width=10,fill=(25,25,25)):
    # draw polyline up to fraction p
    L=[math.dist(pts[i],pts[i+1]) for i in range(len(pts)-1)]; tot=sum(L); lim=tot*clamp(p); acc=0
    for i,l in enumerate(L):
        if acc+l<=lim: d.line((pts[i],pts[i+1]),fill=fill,width=width); acc+=l
        else:
            r=(lim-acc)/l if l else 0
            x=pts[i][0]+(pts[i+1][0]-pts[i][0])*r; y=pts[i][1]+(pts[i+1][1]-pts[i][1])*r
            d.line((pts[i],(x,y)),fill=fill,width=width); break
def circle_pts(cx,cy,rx,ry,n=60,wob=0):
    return [(cx+rx*math.cos(2*math.pi*i/n-1.4)*(1+wob*math.sin(i*1.7)),cy+ry*math.sin(2*math.pi*i/n-1.4)) for i in range(n+3)]
def v3(t):
    img=Image.new("RGB",(W,H),(250,248,240)); d=ImageDraw.Draw(img,"RGBA")
    # calendar
    cal=[(300,420),(780,420),(780,880),(300,880),(300,420)]
    partial_line(d,cal,prog(t,0.1,1.0))
    if t>0.6: partial_line(d,[(300,540),(780,540)],prog(t,0.6,1.0))
    if t>1.0:
        f=font(48); s="БЕРЕЗЕНЬ"; n=int(len(s)*prog(t,1.0,1.4)); ctext(d,455,s[:n],f,(25,25,25))
        f2=font(190); s2="4"; 
        if t>1.4: ctext(d,590,s2,f2,(220,40,50))
        if t>1.6: ctext(d,800,"2027"[:int(4*prog(t,1.6,1.9))],font(52),(25,25,25))
    partial_line(d,circle_pts(540,700,330,330,wob=0.03),prog(t,2.0,2.8),width=12,fill=(220,40,50))
    # arrow
    partial_line(d,[(540,1050),(540,1180)],prog(t,2.8,3.1)); 
    if t>3.1: partial_line(d,[(490,1130),(540,1180),(590,1130)],prog(t,3.1,3.3))
    if t>3.3:
        s="Що далі?"; n=int(len(s)*prog(t,3.3,3.9)); ctext(d,1210,s[:n],font(90),(25,25,25))
    items=["PESEL UKR","Карта CUKR","Карта побиту"]
    for i,it in enumerate(items):
        st=4.2+i*0.55
        if t<st: break
        y=1360+i*110
        d.rectangle((250,y,310,y+60),outline=(25,25,25),width=7)
        if t>st+0.3: partial_line(d,[(258,y+30),(278,y+52),(306,y+4)],prog(t,st+0.3,st+0.5),width=9,fill=(30,150,70))
        n=int(len(it)*prog(t,st,st+0.35)); d.text((340,y-2),it[:n],font=font(56),fill=(25,25,25))
    # hand-drawn underline
    brand(d,dark=True)
    if t>=6.4:
        d.rectangle((0,0,W,H),fill=(250,248,240,int(250*ease(prog(t,6.4,6.7)))))
        cta(d,t,6.5,"Що зробити до 4.03.2027 — у профілі",bg=(25,25,25),fg="white")
    return img
E3=[(0.1,"whoosh"),(1.4,"pop"),(2.0,"whoosh"),(3.3,"tick"),(4.5,"pop"),(5.05,"pop"),(5.6,"pop"),(6.5,"ding")]

# ================= 4. FLAT 2D =================
def v4(t):
    img=Image.new("RGB",(W,H),(255,235,205)); d=ImageDraw.Draw(img,"RGBA")
    # sun
    d.ellipse((760,250,960,450),fill=(255,190,80))
    # skyline parallax
    off=t*25
    for i,(x,w,h,c) in enumerate([(0,180,500,(120,170,200)),(170,150,650,(90,140,180)),(310,200,420,(140,190,215)),(500,160,720,(80,125,165)),(650,220,520,(120,170,200)),(860,180,610,(95,145,185))]):
        X=(x-off)%(W+200)-100
        d.rectangle((X,1350-h,X+w,1350),fill=c)
        for wy in range(1350-h+40,1330,70):
            for wx in range(int(X)+25,int(X+w)-30,55): d.rectangle((wx,wy,wx+25,wy+35),fill=(255,240,180,160))
    d.rectangle((0,1350,W,H),fill=(70,160,110))
    # walking character
    step=math.sin(t*8)
    cx=200+t*45; by=1350
    d.line((cx,by-120,cx-30*step,by),fill=(40,40,60),width=22); d.line((cx,by-120,cx+30*step,by),fill=(40,40,60),width=22)
    d.rounded_rectangle((cx-50,by-330,cx+50,by-110),40,fill=(230,80,60))
    d.ellipse((cx-60,by-450,cx+60,by-330),fill=(255,214,170))
    d.ellipse((cx+10,by-410,cx+26,by-394),fill="black")
    d.line((cx+40,by-280,cx+110,by-340),fill=(255,214,170),width=20)
    # title card
    p=back(prog(t,0.2,0.7))
    if p>0:
        d.rounded_rectangle((90,330,90+900*p,560),40,fill=(40,60,110))
        if p>0.95: ctext(d,360,"3 речі, які треба зробити до березня",font(66),"white",maxw=820)
    cards=["Перевір статус PESEL","Збери документи","Подай заяву вчасно"]
    for i,c in enumerate(cards):
        st=1.8+i*1.2
        p=ease(prog(t,st,st+0.4))
        if p<=0: continue
        x=W-(W-90)*p+ (0)
        y=640+i*170
        d.rounded_rectangle((x,y,x+900,y+140),30,fill="white")
        d.ellipse((x+25,y+25,x+115,y+115),fill=(230,80,60)); ctext(d,y+40,str(i+1),font(56),"white",cx=int(x+70))
        d.text((x+140,y+42),c,font=font(54),fill=(30,30,40))
    brand(d)
    cta(d,t,6.0,"Покроковий гайд — у профілі")
    return img
E4=[(0.2,"whoosh"),(1.8,"whoosh"),(3.0,"whoosh"),(4.2,"whoosh"),(6.0,"ding")]

# ================= 5. INFOGRAPHIC =================
def v5(t):
    img=Image.new("RGB",(W,H),(18,22,40)); d=ImageDraw.Draw(img,"RGBA")
    for x in range(0,W,90): d.line((x,0,x,H),fill=(28,34,60),width=2)
    for y in range(0,H,90): d.line((0,y,W,y),fill=(28,34,60),width=2)
    yy=ctext(d,300,"Переказ 1000 zł в Україну",font(70),"white",maxw=900)
    ctext(d,yy+15,"скільки дійде мамі?",font(52,False),(170,180,210))
    base=1250
    bars=[("Варіант А",0.78,(230,80,80),"−"),("Варіант Б",0.97,(60,200,130),"+")]
    for i,(lab,val,col,_) in enumerate(bars):
        st=1.0+i*1.3; p=ease(prog(t,st,st+1.0))
        x=220+i*380; bw=260; hmax=600
        h=hmax*val*p
        d.rounded_rectangle((x,base-h,x+bw,base),24,fill=col)
        ctext(d,base+30,lab,font(48),"white",cx=x+bw//2)
        if p>0: ctext(d,base-h-80,f"{int(100*val*p)}%",font(64),"white",cx=x+bw//2)
    d.line((150,base,930,base),fill=(200,200,220),width=6)
    if t>3.6:
        p=back(prog(t,3.6,4.0))
        d.rounded_rectangle((540-380*p,1400,540+380*p,1520),30,fill=(255,214,10))
        if p>0.9: ctext(d,1420,"Різниця — до 19%",font(60),(20,20,20))
    ctext(d,1560,"*приклад, цифри умовні",font(34,False),(130,140,170))
    brand(d)
    if t>=6.0:
        d.rectangle((0,0,W,H),fill=(0,0,0,int(160*ease(prog(t,6.0,6.3)))))
    cta(d,t,6.1,"Порівняння сервісів — у профілі")
    return img
E5=[(1.0,"whoosh"),(2.3,"whoosh"),(3.6,"pop"),(6.1,"ding")]

if __name__=="__main__":
  jobs={"1_mem_oblychchia":(v1,E1),"2_perepyska":(v2,E2),"3_dudl":(v3,E3),"4_ploska_2d":(v4,E4),"5_infografika":(v5,E5)}
  for k in sys.argv[1:] or jobs:
    fn,ev=jobs[k]; render(k,fn,ev)
