import sys, os, math, subprocess, wave, unicodedata
import numpy as np
from PIL import Image, ImageDraw
import pathlib
PBS=pathlib.Path(__file__).resolve().parents[2] if "videos" in __file__ else pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(PBS/"lib"))
import render as R
from render import W,H,FPS,font,ctext,wrap,clamp,ease,back,prog,face,partial_line,circle_pts
VOICE=str(PBS/"voice/model/uk_UA-ukrainian_tts-medium.onnx")
SPK=int(os.environ.get("SPK","1"))
A="́"
# (scene, caption text, tts text)
SEG=[
 ("A","Відправив мамі тисячу злотих «без комісії»… а дійшло менше. Знайома ситуація?",
      f"відправив ма{A}мі ти{A}сячу зло{A}тих без комі{A}сії. а дійшло{A} ме{A}нше. знайо{A}ма ситуа{A}ція?"),
 ("B","Весь секрет у тому, що крім комісії є ще курс обміну. Нуль злотих комісії — але невигідний курс. Різниця ховається саме там.",
      f"весь секре{A}т у то{A}му, що крім комі{A}сії є ще курс о{A}бміну. нуль зло{A}тих комі{A}сії — але невигідний курс. рі{A}зниця хова{A}ється са{A}ме там."),
 ("C","Тому порівнюй не комісію, а одне число: скільки гривень отримає мама.",
      f"тому{A} порі{A}внюй, не комі{A}сію, а одне{A} число{A}: скі{A}льки гри{A}вень отри{A}має ма{A}ма."),
 ("D","Три правила. Перше: дивись на кінцеву суму в гривнях. Друге: порівняй два або три сервіси. Третє: перевір ліміти і час доставки.",
      f"три пра{A}вила. пе{A}рше: диви{A}сь на кінце{A}ву су{A}му в гри{A}внях. друге: порівняй два або три сервіси. тре{A}тє: переві{A}р ліміти{A} і час доста{A}вки."),
 ("E","Підпишись — пояснюємо життя в Польщі без стресу!",
      f"підпиши{A}сь — поя{A}снюємо життя{A} в по{A}льщі — без стре{A}су!"),
]
# Voice profile "8d": Tetiana, clearer
VP=dict(spk=2,length=0.92,noise=0.6,noisew=0.8,pitch=1.08,eq="highpass=f=90,equalizer=f=3500:t=q:w=1:g=3")
def tts(text,path):
    text=unicodedata.normalize("NFC",text)
    raw=path+".raw.wav"
    subprocess.run([sys.executable,"-m","piper","-m",VOICE,"-s",str(VP["spk"]),"--length-scale",str(VP["length"]),"--noise-scale",str(VP["noise"]),"--noise-w-scale",str(VP["noisew"]),"-f",raw],input=text.encode(),check=True,capture_output=True)
    af=f"asetrate=22050*{VP['pitch']},aresample=22050,atempo={1/VP['pitch']:.4f},{VP['eq']}"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",af,"-ar","22050","-ac","1",path],check=True); os.remove(raw)
    with wave.open(path) as w: sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(0,nz[0]-300):nz[-1]+800]
    a=a/max(1e-6,np.abs(a).max())*0.9
    return a,sr
import re, difflib
from faster_whisper import WhisperModel
ASR=WhisperModel("small",device="cpu",compute_type="int8")
NUMW={"0":"нуль","1":"один","2":"два","3":"три","ноль":"нуль"}
def norm(t):
    t=t.lower().replace("ё","е"); t=re.sub(r"(\d)-(\d)",r"\1 \2",t)
    ws=re.findall(r"[a-zа-яіїєґ0-9']+",t); return [NUMW.get(w,w) for w in ws]
def score(a,sr,ref):
    a16=np.interp(np.arange(0,len(a),sr/16000),np.arange(len(a)),a).astype(np.float32)
    segs,_=ASR.transcribe(a16,language="uk",beam_size=5); hyp=" ".join(x.text for x in segs)
    return difflib.SequenceMatcher(None,norm(ref),norm(hyp)).ratio(),hyp
TAKES=int(os.environ.get("TAKES","6"))
QA=[]
SPLIT=re.compile(r"(?<=[.?!…])\s+")
def best_one(tag,cap,text):
    best=None
    for k in range(TAKES):
        a,sr=tts(text,f"_{tag}_{k}.wav"); sc,hyp=score(a,sr,cap)
        if best is None or sc>best[0]: best=(sc,a,sr,hyp)
        if sc>=0.99: break
    return best
def best_tts(i,cap,text):
    cs=SPLIT.split(cap.strip()); ts=SPLIT.split(text.strip())
    if len(cs)!=len(ts): cs,ts=[cap],[text]
    # merge very short sentences with the previous one (ASR is unreliable on 1-2 words)
    C,T=[],[]
    for c,t in zip(cs,ts):
        if C and len(c.split())<3: C[-1]+=" "+c; T[-1]+=" "+t
        else: C.append(c); T.append(t)
    cs,ts=C,T
    parts=[]; sr=22050
    for j,(c,t) in enumerate(zip(cs,ts)):
        sc,a,sr,hyp=best_one(f"{i}_{j}",c,t); QA.append((i,j,round(sc,3),c,hyp.strip())); parts.append(a); parts.append(np.zeros(int(0.16*sr),dtype=np.float32))
    return np.concatenate(parts[:-1]),sr
PAD_BEFORE,PAD_AFTER=0.25,0.35
segs=[]; t=0
for i,(sc,cap,tx) in enumerate(SEG):
    a,sr=best_tts(i,cap,tx)
    d=len(a)/sr
    segs.append(dict(scene=sc,cap=cap,audio=a,sr=sr,start=t,vstart=t+PAD_BEFORE,vdur=d,dur=PAD_BEFORE+d+PAD_AFTER))
    t+=PAD_BEFORE+d+PAD_AFTER
TOTAL=t+0.6
for q in QA: print("QA",q)
print("total",round(TOTAL,2),[round(s["dur"],2) for s in segs])

# ---- audio mix
SR=44100; mix=np.zeros(int(SR*TOTAL)+SR,dtype=np.float32)
for s in segs:
    a=s["audio"]; a=np.repeat(a,2) if s["sr"]==22050 else a
    i=int(s["vstart"]*SR); mix[i:i+len(a)]+=a*0.95
def sfx(kind,tt):
    n={"pop":0.09,"whoosh":0.35,"boom":0.5,"ding":0.6}[kind]; n=int(n*SR); x=np.arange(n)/SR
    if kind=="pop": s=np.sin(2*np.pi*(900-5000*x)*x)*np.exp(-x*45)*0.35
    elif kind=="whoosh":
        rng=np.random.default_rng(1); s=rng.standard_normal(n)*np.sin(np.pi*x/0.35)*0.12; s=np.convolve(s,np.ones(30)/30,mode="same")*3
    elif kind=="boom": s=np.sin(2*np.pi*(120-80*x)*x)*np.exp(-x*7)*0.6
    else: s=(np.sin(2*np.pi*1320*x)+0.5*np.sin(2*np.pi*1980*x))*np.exp(-x*6)*0.2
    i=int(tt*SR); mix[i:i+n]+=s[:len(mix)-i]
EV=[]
def ev(k,t): EV.append((k,t))
S={s["scene"]:s for s in segs}
for s in segs[1:]: ev("whoosh",s["start"]-0.1)
ev("boom",S["A"]["vstart"]+S["A"]["vdur"]*0.62)
ev("pop",S["B"]["start"]+0.5); ev("pop",S["B"]["start"]+S["B"]["dur"]*0.35)
ev("pop",S["C"]["start"]+S["C"]["dur"]*0.55)
for k in range(3): ev("pop",S["D"]["vstart"]+S["D"]["vdur"]*(0.12+k*0.3))
ev("ding",S["E"]["start"]+0.2)
for k,tt in EV: sfx(k,max(0,tt))
x=np.arange(len(mix))/SR
mix+=(np.sin(2*np.pi*110*x)+np.sin(2*np.pi*164.8*x)+np.sin(2*np.pi*220*x))*0.012*(0.6+0.4*np.sin(2*np.pi*0.5*x))
mix=mix[:int(SR*TOTAL)]; mix=mix/max(1,np.abs(mix).max()*1.05)
with wave.open("mix.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())

# ---- captions (chunked karaoke)
def chunks_for(s):
    words=s["cap"].split(); out=[]; cur=[]
    for w in words:
        cur.append(w)
        if len(cur)>=4 or w[-1] in ".:?!…—":
            out.append(cur); cur=[]
    if cur: out.append(cur)
    total=sum(len(w)+1 for w in words); t=s["vstart"]; res=[]
    for c in out:
        L=sum(len(w)+1 for w in c); d=s["vdur"]*L/total
        res.append((t,t+d,c)); t+=d
    return res
CH=[c for s in segs for c in chunks_for(s)]
def caption(d,t):
    for a,b,c in CH:
        if a<=t<b+0.15:
            f=font(70); txt=" ".join(c); lines=wrap(d,txt,f,940); lh=86
            y0=1250
            # word index
            tot=sum(len(w)+1 for w in c); acc=0; k=0
            for i,w in enumerate(c):
                if a+(b-a)*acc/tot<=t: k=i
                acc+=len(w)+1
            pop=back(prog(t,a,a+0.15)); sz=int(70*(0.85+0.15*pop)); f=font(max(40,sz))
            idx=0
            for li,l in enumerate(wrap(d,txt,f,940)):
                tw=d.textlength(l,font=f); xx=W/2-tw/2
                for w in l.split():
                    col=(255,214,10) if idx==k else "white"
                    d.text((xx,y0+li*lh),w,font=f,fill=col,stroke_width=9,stroke_fill="black"); xx+=d.textlength(w+" ",font=f); idx+=1
            return

# ---- scenes
def scene_A(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(46,58,89))
    hit=PAD_BEFORE+s["vdur"]*0.62
    shock=tau>=hit
    sh=(math.sin(tau*90)*16*(1-prog(tau,hit,hit+0.7))) if shock else 0
    r=int(210*(1+0.1*ease(prog(tau,hit,hit+0.25))))
    cx,cy=540+sh,700
    d.rounded_rectangle((cx-190,cy+r-30,cx+190,1180),60,fill=(240,170,40))
    face(d,cx,cy,r,"shock" if shock else "calm",tau)
    # phone
    px,py=790,880; d.rounded_rectangle((px,py,px+200,py+330),28,fill=(30,30,35)); d.rounded_rectangle((px+12,py+30,px+188,py+300),16,fill="white")
    if not shock:
        ctext(d,py+80,"0%",font(70),(30,160,80),cx=px+100); ctext(d,py+170,"комісії",font(34),(30,160,80),cx=px+100)
    else:
        ctext(d,py+90,"−???",font(54),(210,40,40),cx=px+100); ctext(d,py+170,"грн",font(40),(210,40,40),cx=px+100)
    d.line((cx+150,cy+r+40,px+20,py+200),fill=(255,214,170),width=34)
    if shock and tau<hit+0.9:
        for i in range(10):
            a=i*math.pi/5+tau*2; d.line((cx+math.cos(a)*(r+40),cy+math.sin(a)*(r+40),cx+math.cos(a)*(r+95),cy+math.sin(a)*(r+95)),fill=(255,214,10),width=11)
    p=back(prog(tau,0.05,0.4))
    if p>0:
        d.rounded_rectangle((540-420*p,300,540+420*p,420),30,fill=(220,40,50))
        if p>0.9: ctext(d,322,"Переказ мамі",font(64),"white")
def scene_B(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(250,248,240)); D=s["dur"]
    partial_line(d,[(110,420),(500,420),(500,760),(110,760),(110,420)],prog(tau,0.0,0.6))
    partial_line(d,[(580,420),(970,420),(970,760),(580,760),(580,420)],prog(tau,0.2,0.8))
    if tau>0.5: ctext(d,450,"КОМІСІЯ"[:int(7*prog(tau,0.5,0.9))],font(52),(25,25,25),cx=305)
    if tau>0.7: ctext(d,450,"КУРС"[:int(4*prog(tau,0.7,1.0))],font(52),(25,25,25),cx=775)
    if tau>1.0: ctext(d,560,"0 zł",font(110),(30,150,70),cx=305)
    if tau>1.2: ctext(d,560,"?",font(130),(25,25,25),cx=775)
    t1=D*0.45; partial_line(d,[(150,600),(460,700)],prog(tau,t1,t1+0.3),width=14,fill=(220,40,50))
    t2=D*0.6; partial_line(d,circle_pts(775,590,250,230,wob=0.03),prog(tau,t2,t2+0.7),width=12,fill=(220,40,50))
    t3=D*0.72
    if tau>t3:
        partial_line(d,[(775,860),(775,990)],prog(tau,t3,t3+0.25)); 
        if tau>t3+0.25: partial_line(d,[(725,940),(775,990),(825,940)],prog(tau,t3+0.25,t3+0.4))
        s2="тут ховається різниця"; n=int(len(s2)*prog(tau,t3+0.3,t3+1.0)); ctext(d,1030,s2[:n],font(56),(220,40,50))
def scene_C(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(18,22,40))
    for x in range(0,W,90): d.line((x,0,x,H),fill=(28,34,60),width=2)
    for y in range(0,H,90): d.line((0,y,W,y),fill=(28,34,60),width=2)
    yy=ctext(d,300,"Скільки отримає мама?",font(66),"white")
    base=1080
    for i,(lab,sub,val,col,word) in enumerate([("Сервіс А","0 zł комісії",0.72,(230,80,80),"менше"),("Сервіс Б","є комісія",0.95,(60,200,130),"більше")]):
        st=0.3+i*0.7; p=ease(prog(tau,st,st+0.9)); x=200+i*400; bw=280; h=520*val*p
        d.rounded_rectangle((x,base-h,x+bw,base),24,fill=col)
        ctext(d,base+20,lab,font(46),"white",cx=x+bw//2); ctext(d,base+75,sub,font(32,False),(170,180,210),cx=x+bw//2)
        if p>0.95: ctext(d,base-h-75,word,font(54),"white",cx=x+bw//2)
    d.line((150,base,930,base),fill=(200,200,220),width=6)
    ctext(d,base+130,"*приклад, цифри умовні",font(30,False),(130,140,170))
def scene_D(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205)); off=tau*25
    for x,w,h,c in [(0,180,420,(120,170,200)),(170,150,560,(90,140,180)),(310,200,380,(140,190,215)),(500,160,600,(80,125,165)),(650,220,460,(120,170,200)),(860,180,520,(95,145,185))]:
        X=(x-off)%(W+200)-100; d.rectangle((X,1180-h,X+w,1180),fill=c)
    d.rectangle((0,1180,W,H),fill=(70,160,110))
    p=back(prog(tau,0.0,0.4))
    if p>0:
        d.rounded_rectangle((540-450*p,290,540+450*p,430),36,fill=(40,60,110))
        if p>0.95: ctext(d,318,"3 правила переказу",font(66),"white")
    cards=["Дивись суму в гривнях","Порівнюй 2–3 сервіси","Перевір ліміти і час"]
    for i,c in enumerate(cards):
        st=PAD_BEFORE+s["vdur"]*(0.12+i*0.3)-0.1; p=ease(prog(tau,st,st+0.35))
        if p<=0: continue
        x=W-(W-80)*p; y=500+i*175
        d.rounded_rectangle((x,y,x+920,y+145),30,fill="white")
        d.ellipse((x+25,y+27,x+115,y+117),fill=(230,80,60)); ctext(d,y+42,str(i+1),font(56),"white",cx=int(x+70))
        d.text((x+140,y+44),c,font=font(54),fill=(30,30,40))
def scene_E(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(46,58,89))
    p=back(prog(tau,0.0,0.45))
    face(d,540,640,int(170*max(0.01,p)),"calm",tau+1)
    if p>0:
        d.rounded_rectangle((540-380*p,900,540+380*p,1060),45,fill=(255,214,10))
        if p>0.9: ctext(d,935,"ПІДПИШИСЬ",font(76),(20,20,20))
FN={"A":scene_A,"B":scene_B,"C":scene_C,"D":scene_D,"E":scene_E}
N=int(TOTAL*FPS)
cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","mix.wav",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-profile:v","high","-c:a","aac","-b:a","160k","-ar","44100","-shortest","-movflags","+faststart","video01_perekaz_mami.mp4"]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    s=segs[-1]
    for sg in segs:
        if sg["start"]<=t<sg["start"]+sg["dur"]: s=sg; break
    img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img,"RGBA")
    FN[s["scene"]](d,img,t-s["start"],s)
    R.brand(d,dark=(s["scene"]=="B"))
    caption(d,t)
    # flash transition
    for sg in segs[1:]:
        dt=t-sg["start"]
        if 0<=dt<0.18: d.rectangle((0,0,W,H),fill=(255,255,255,int(160*(1-dt/0.18))))
    p.stdin.write(img.tobytes())
    if i%int(FPS*4)==0: img.save(f"frame_{i//FPS:02d}.png")
p.stdin.close(); p.wait(); print("ok")
