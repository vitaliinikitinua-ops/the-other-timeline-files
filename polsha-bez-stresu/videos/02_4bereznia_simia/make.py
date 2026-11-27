import sys, os, math, subprocess, wave, unicodedata
import numpy as np
from PIL import Image, ImageDraw
SP="/tmp/claude-0/-home-user-the-other-timeline-files/0bd9b492-2d39-5628-8b8e-071d69c7e472/scratchpad"
sys.path.insert(0,SP+"/samples")
import render as R
from render import W,H,FPS,font,ctext,wrap,clamp,ease,back,prog,face,partial_line,circle_pts
VOICE=SP+"/voice/uk_UA-ukrainian_tts-medium.onnx"
SPK=int(os.environ.get("SPK","1"))
A="́"
# (scene, caption text, tts text)
SEG=[
 ("A","4 березня 2027|статус UKR закінчується.|А в тебе діти|і жодного плану?",
      f"четве{A}рте бе{A}резня два{A}дцять сьо{A}мого — ста{A}тус у ка ер закі{A}нчується. а в те{A}бе ді{A}ти, і жо{A}дного пла{A}ну?"),
 ("B","Спокійно.|Є карта побиту CUKR|на три роки.|Заява тільки онлайн,|через портал MOS,|і подати її треба|до 4 березня.",
      f"споко{A}йно. є ка{A}рта по{A}биту цукр — на три ро{A}ки. зая{A}ва ті{A}льки онла{A}йн, через портал мос, і пода{A}ти її{A} тре{A}ба до четве{A}ртого бе{A}резня."),
 ("C","І про 800+:|з лютого виплата є,|тільки якщо хтось|із батьків працює,|а дитина ходить|до польської школи.",
      f"і про ві{A}сімсот плюс: з лю{A}того ви{A}плата є, ті{A}льки якщо{A} хтось із батькі{A}в працю{A}є, а дити{A}на хо{A}дить до по{A}льської шко{A}ли."),
 ("D","Що зробити вже зараз.|Перше: перевір|статус UKR для всієї сім'ї.|Друге: заведи|акаунт у MOS|і зроби фото.|Третє: підготуй оплату:|440 злотих за заяву.",
      f"що зроби{A}ти вже за{A}раз. пе{A}рше — переві{A}р ста{A}тус у ка ер для всіє{A}ї сім'ї{A}. друге: заведи{A} ака{A}унт у мос і зроби{A} фо{A}то. тре{A}тє: підготу{A}й опла{A}ту — чоти{A}риста со{A}рок зло{A}тих за зая{A}ву."),
 ("E","Підпишись!|Покажу, як заповнити заяву|крок за кроком!",
      f"підпиши{A}сь — покажу{A}, як запо{A}внити зая{A}ву, крок за кро{A}ком!"),
]

# Voice profile "8d": Tetiana, clearer
VP=dict(spk=2,length=0.92,noise=0.6,noisew=0.8,pitch=1.08,eq="highpass=f=90,equalizer=f=3500:t=q:w=1:g=3")
def tts(text,path):
    text=unicodedata.normalize("NFC",text)
    raw=path+".raw.wav"
    subprocess.run([sys.executable,"-m","piper","-m",VOICE,"-s",str(VP["spk"]),"--length-scale",str(VP["length"]),"--noise-scale",str(VP["noise"]),"--noise-w-scale",str(VP["noisew"]),"-f",raw],input=text.encode(),check=True,capture_output=True)
    af=f"asetrate=22050*{VP['pitch']},aresample=22050,atempo={1.05/VP['pitch']:.4f},{VP['eq']}"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",af,"-ar","22050","-ac","1",path],check=True); os.remove(raw)
    with wave.open(path) as w: sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(0,nz[0]-300):nz[-1]+800]
    a=a/max(1e-6,np.abs(a).max())*0.9
    return a,sr
import re, difflib
from faster_whisper import WhisperModel
ASR=WhisperModel("small",device="cpu",compute_type="int8")
NUMW={"0":"нуль","1":"один","2":"два","3":"три","ноль":"нуль","моз":"мос","спокойно":"спокійно","аккаунт":"акаунт","27го":"27","4е":"4","четверте":"4"}
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
def asr_ref(c):
    for a,b in [("CUKR","цукр"),("UKR","укр"),("MOS","мос"),("800+","800 плюс"),("4 березня 2027","4 березня 27")]: c=c.replace(a,b)
    return c
def best_one(tag,cap,text):
    best=None
    for k in range(TAKES):
        a,sr=tts(text,f"_{tag}_{k}.wav"); sc,hyp=score(a,sr,cap)
        if best is None or sc>best[0]: best=(sc,a,sr,hyp)
        if sc>=0.99: break
    return best
def best_tts(i,cap,text):
    cs=SPLIT.split(cap.replace('|',' ').strip()); ts=SPLIT.split(text.strip())
    if len(cs)!=len(ts): cs,ts=[cap],[text]
    # merge very short sentences with the previous one (ASR is unreliable on 1-2 words)
    C,T=[],[]
    for c,t in zip(cs,ts):
        if C and len(c.split())<3: C[-1]+=" "+c; T[-1]+=" "+t
        else: C.append(c); T.append(t)
    cs,ts=C,T
    parts=[]; sr=22050
    for j,(c,t) in enumerate(zip(cs,ts)):
        sc,a,sr,hyp=best_one(f"{i}_{j}",asr_ref(c),t); QA.append((i,j,round(sc,3),c,hyp.strip())); parts.append(a); parts.append(np.zeros(int(0.16*sr),dtype=np.float32))
    return np.concatenate(parts[:-1]),sr
PAD_BEFORE,PAD_AFTER=0.15,0.2
segs=[]; t=0
for i,(sc,cap,tx) in enumerate(SEG):
    cf=f'voicecache_{i}.npy'
    if os.path.exists(cf) and os.environ.get('REUSE')=='1': a=np.load(cf); sr=22050
    else: a,sr=best_tts(i,cap,tx); np.save(cf,a)
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
ev("boom",S["A"]["vstart"]+S["A"]["vdur"]*0.45)
ev("pop",S["B"]["start"]+0.6); ev("pop",S["B"]["start"]+S["B"]["dur"]*0.45); ev("pop",S["B"]["start"]+S["B"]["dur"]*0.75)
ev("pop",S["C"]["vstart"]+S["C"]["vdur"]*0.45); ev("pop",S["C"]["vstart"]+S["C"]["vdur"]*0.75); ev("ding",S["C"]["vstart"]+S["C"]["vdur"]*0.82)
for k in range(3): ev("pop",S["D"]["vstart"]+S["D"]["vdur"]*(0.2+k*0.27))
ev("ding",S["E"]["start"]+0.2)
for k,tt in EV: sfx(k,max(0,tt))
x=np.arange(len(mix))/SR
mix+=(np.sin(2*np.pi*110*x)+np.sin(2*np.pi*164.8*x)+np.sin(2*np.pi*220*x))*0.012*(0.6+0.4*np.sin(2*np.pi*0.5*x))
mix=mix[:int(SR*TOTAL)]; mix=mix/max(1,np.abs(mix).max()*1.05)
with wave.open("mix.wav","wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())

# ---- captions (chunked karaoke, safe-zone aware)
CAP_CX,CAP_W,CAP_Y=515,780,1240
NOEND={"до","у","в","і","й","а","з","із","для","на","через","про","по","не","що","як","—","за","та"}
NB="\u00a0"
KEEP=["крок за кроком","статус UKR","карта побиту","портал MOS","акаунт у MOS","до 4 березня","4 березня 2027","440 злотих","800+:","польської школи","всієї сім'ї"]
def prep(cap):
    cap=cap.replace(" — "," ").replace("—","")
    for k in KEEP: cap=cap.replace(k,k.replace(" ",NB))
    return cap
def chunks_for(s):
    if "|" in s["cap"]:
        res2=[c.split() for c in s["cap"].split("|")]; words=s["cap"].replace("|"," ").split()
        total=sum(len(w)+1 for w in words); t=s["vstart"]; res=[]
        for c in res2:
            L=sum(len(w)+1 for w in c); d=s["vdur"]*L/total; res.append((t,t+d,c)); t+=d
        return res
    words=prep(s["cap"]).split(); out=[]; cur=[]
    for i,w in enumerate(words):
        cur.append(w); nxt=words[i+1] if i+1<len(words) else None
        L=len(" ".join(cur))
        end_punct=w[-1] in ".:?!…,"
        brk=(end_punct and len(cur)>=2) or w[-1] in ".?!…" or len(cur)>=5 or L>=24
        if brk and nxt is not None:
            # don't end on a function word / dash / bare number before its noun
            while len(cur)>1 and (cur[-1].lower() in NOEND or cur[-1].isdigit()):
                nxt_word=cur.pop(); out.append(cur); cur=[nxt_word]; break
            else:
                out.append(cur); cur=[]
    if cur: out.append(cur)
    # merge a lone trailing dash/short word into previous chunk
    res2=[]
    for c in out:
        if res2 and (c==["—"] or (len(c)==1 and len(c[0])<=2)): res2[-1]+=c
        else: res2.append(c)
    total=sum(len(w)+1 for w in words); t=s["vstart"]; res=[]
    for c in res2:
        L=sum(len(w)+1 for w in c); d=s["vdur"]*L/total
        res.append((t,t+d,c)); t+=d
    return res
CH=[c for s in segs for c in chunks_for(s)]
def caption(d,t):
    for a,b,c in CH:
        if a<=t<b+0.15:
            c=" ".join(w.replace(NB," ") for w in c).split(); txt=" ".join(c)
            tot=sum(len(w)+1 for w in c); acc=0; k=0
            for i,w in enumerate(c):
                if a+(b-a)*acc/tot<=t: k=i
                acc+=len(w)+1
            pop=back(prog(t,a,a+0.15)); f=font(max(40,int(66*(0.88+0.12*pop)))); lh=82
            lines=wrap(d,txt,f,CAP_W)
            wmax=max(d.textlength(l,font=f) for l in lines)
            d.rounded_rectangle((CAP_CX-wmax/2-34,CAP_Y-18,CAP_CX+wmax/2+34,CAP_Y+len(lines)*lh+6),28,fill=(0,0,0,135))
            idx=0
            for li,l in enumerate(lines):
                tw=d.textlength(l,font=f); xx=CAP_CX-tw/2
                for w in l.split():
                    col=(255,214,10) if idx==k else "white"
                    # NOTE: word index counts space-separated words of the chunk
                    d.text((xx,CAP_Y+li*lh),w,font=f,fill=col,stroke_width=5,stroke_fill="black"); xx+=d.textlength(w+" ",font=f); idx+=1
            return
# ---- scenes
def mom(d,cx,cy,r,mood,tau):
    d.ellipse((cx-r*1.15,cy-r*1.05,cx+r*1.15,cy+r*1.35),fill=(120,70,40))
    face(d,cx,cy,r,mood,tau,skin=(250,210,175))
def scene_A(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(46,58,89))
    hit=PAD_BEFORE+s["vdur"]*0.45; shock=tau>=hit
    sh=(math.sin(tau*90)*16*(1-prog(tau,hit,hit+0.7))) if shock else 0
    r=int(175*(1+0.1*ease(prog(tau,hit,hit+0.25))))
    d.rounded_rectangle((540-170+sh,780+r-40,540+170+sh,1180),60,fill=(200,80,110))
    mom(d,540+sh,760,r,"shock" if shock else "calm",tau)
    for kx,ph in ((235,0.3),(800,0.7)):
        kr=95; ky=960
        d.rounded_rectangle((kx-90,ky+kr-20,kx+90,1180),40,fill=(90,170,220) if kx<540 else (250,200,70))
        face(d,kx,ky,kr,"shock" if tau>=hit+0.15 else "calm",tau+ph,skin=(255,220,185))
    if shock and tau<hit+0.9:
        for i in range(10):
            a=i*math.pi/5+tau*2; d.line((540+math.cos(a)*(r+50),760+math.sin(a)*(r+50),540+math.cos(a)*(r+105),760+math.sin(a)*(r+105)),fill=(255,214,10),width=11)
    p=back(prog(tau,0.05,0.4))
    if p>0:
        d.rounded_rectangle((540-440*p,290,540+440*p,430),30,fill=(220,40,50))
        if p>0.9: ctext(d,318,"PESEL UKR — до 4.03.2027",font(58),"white")
def scene_B(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(250,248,240)); D=s["dur"]
    # card
    partial_line(d,[(120,330),(560,330),(560,600),(120,600),(120,330)],prog(tau,0.0,0.6))
    if tau>0.5: ctext(d,370,"CUKR"[:int(4*prog(tau,0.5,0.8))],font(90),(30,90,170),cx=340)
    if tau>0.9: ctext(d,500,"3 роки",font(56),(25,25,25),cx=340)
    # laptop
    t1=D*0.4
    partial_line(d,[(590,360),(910,360),(910,560),(590,560),(590,360)],prog(tau,t1,t1+0.5))
    partial_line(d,[(560,600),(940,600)],prog(tau,t1+0.3,t1+0.6))
    if tau>t1+0.5: ctext(d,420,"MOS",font(80),(30,150,70),cx=750)
    if tau>t1+0.7: ctext(d,620,"тільки онлайн",font(44),(25,25,25),cx=750)
    # calendar
    t2=D*0.68
    partial_line(d,[(330,760),(750,760),(750,1130),(330,1130),(330,760)],prog(tau,t2,t2+0.4))
    if tau>t2+0.3: ctext(d,790,"до",font(50),(25,25,25))
    if tau>t2+0.45: ctext(d,880,"4.03",font(130),(220,40,50))
    if tau>t2+0.6: ctext(d,1040,"2027",font(56),(25,25,25))
    partial_line(d,circle_pts(540,945,290,240,wob=0.03),prog(tau,t2+0.7,t2+1.3),width=12,fill=(220,40,50))
def scene_C(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(18,22,40))
    for x in range(0,W,90): d.line((x,0,x,H),fill=(28,34,60),width=2)
    for y in range(0,H,90): d.line((0,y,W,y),fill=(28,34,60),width=2)
    ctext(d,300,"800+ з 1.02.2026",font(70),"white")
    rows=[("Батьки працюють",0.45),("Дитина в польській школі",0.75)]
    for i,(txt,f0) in enumerate(rows):
        st=PAD_BEFORE+s["vdur"]*f0-0.2; p=ease(prog(tau,st,st+0.35))
        if p<=0: continue
        y=520+i*190; x=W-(W-60)*p
        d.rounded_rectangle((x,y,x+840,y+150),30,fill=(36,44,78))
        d.ellipse((x+30,y+30,x+120,y+120),fill=(60,200,130))
        d.line((x+52,y+77,x+72,y+98,x+102,y+52),fill="white",width=12)
        d.text((x+140,y+52),txt,font=font(44),fill="white")
    st=PAD_BEFORE+s["vdur"]*0.82; p=back(prog(tau,st,st+0.4))
    if p>0.05:
        d.rounded_rectangle((540-300*p,920,540+300*p,1100),40,fill=(255,214,10))
        if p>0.9: ctext(d,945,"= 800+",font(100),(20,20,20))
def scene_D(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205)); off=tau*25
    for x,w,h,c in [(0,180,420,(120,170,200)),(170,150,560,(90,140,180)),(310,200,380,(140,190,215)),(500,160,600,(80,125,165)),(650,220,460,(120,170,200)),(860,180,520,(95,145,185))]:
        X=(x-off)%(W+200)-100; d.rectangle((X,1180-h,X+w,1180),fill=c)
    d.rectangle((0,1180,W,H),fill=(70,160,110))
    p=back(prog(tau,0.0,0.4))
    if p>0:
        d.rounded_rectangle((540-450*p,290,540+450*p,430),36,fill=(40,60,110))
        if p>0.95: ctext(d,318,"Що зробити вже зараз",font(64),"white")
    cards=["Статус UKR усієї сім'ї","Акаунт у MOS + фото","Підготуй 440 zł"]
    for i,c in enumerate(cards):
        st=PAD_BEFORE+s["vdur"]*(0.2+i*0.27)-0.1; p=ease(prog(tau,st,st+0.35))
        if p<=0: continue
        x=W-(W-60)*p; y=500+i*175
        d.rounded_rectangle((x,y,x+840,y+145),30,fill="white")
        d.ellipse((x+25,y+27,x+115,y+117),fill=(230,80,60)); ctext(d,y+42,str(i+1),font(56),"white",cx=int(x+70))
        d.text((x+138,y+46),c,font=font(50),fill=(30,30,40))
def scene_E(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(46,58,89))
    p=back(prog(tau,0.0,0.45))
    mom(d,540,620,int(160*max(0.01,p)),"calm",tau+1)
    if p>0:
        d.rounded_rectangle((540-380*p,880,540+380*p,1040),45,fill=(255,214,10))
        if p>0.9: ctext(d,915,"ПІДПИШИСЬ",font(76),(20,20,20))
    if p>0.9: ctext(d,1090,"Джерело: gov.pl, станом на 27.11.2026. Не є юридичною консультацією.",font(30,False),(190,200,225),maxw=900)
FN={"A":scene_A,"B":scene_B,"C":scene_C,"D":scene_D,"E":scene_E}
N=int(TOTAL*FPS)
cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","mix.wav",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-profile:v","high","-c:a","aac","-b:a","160k","-ar","44100","-shortest","-movflags","+faststart","video02_4bereznia_simia.mp4"]
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
