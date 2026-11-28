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
 ("H","Карту CUKR можна оформити|не виходячи з дому.|5 кроків — збережи!",
      f"ка{A}рту цукр мо{A}жна оформи{A}ти, не вихо{A}дячи з до{A}му. п'ять кро{A}ків — збережи{A}!"),
 ("1","Крок перший:|новий акаунт|у MOS,|навіть якщо старий уже був.",
      f"крок пе{A}рший: нови{A}й ака{A}унт у мос — на{A}віть якщо{A} стари{A}й уже{A} був."),
 ("2","Крок другий:|зайди через login.gov.pl|і заповни форму.",
      f"крок дру{A}гий: зайди{A} через логін гов пе ел — і запо{A}вни фо{A}рму."),
 ("3","Крок третій: ще ДО подачі|оплати 340 і 100 злотих.|Номери рахунків — на сайті ужонду.",
      f"крок тре{A}тій: ще до пода{A}чі опла{A}ти три{A}ста со{A}рок і сто зло{A}тих. номери{A} раху{A}нків — на са{A}йті ужо{A}нду."),
 ("4","Крок четвертий:|фото не старше|6 місяців|і підтвердження оплат.",
      f"крок четве{A}ртий: фо{A}то не ста{A}рше шести{A} мі{A}сяців, і підтве{A}рдження опла{A}т."),
 ("5","Крок п'ятий:|підпиши електронно|і збережи підтвердження.",
      f"крок п'я{A}тий: підпиши{A} електро{A}нно, і збережи{A} підтве{A}рдження."),
 ("B","Бонус:|відбитки пальців здавати не треба.|До ужонду — тільки по готову карту.",
      f"бо{A}нус: ві{A}дбитки па{A}льців здава{A}ти не тре{A}ба. до ужо{A}нду — ті{A}льки по гото{A}ву ка{A}рту."),
 ("E","Перешли це тому,|хто ще не подав!",
      f"перешли{A} це тому{A}, хто ще не пода{A}в!"),
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
    for a,b in [("CUKR","цукр"),("UKR","укр"),("MOS","мос"),("login.gov.pl","логін гов пл"),("ДО","до")]: c=c.replace(a,b)
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
for k in "12345": ev("ding",S[k]["start"]+0.05)
ev("pop",S["3"]["vstart"]+S["3"]["vdur"]*0.35); ev("pop",S["3"]["vstart"]+S["3"]["vdur"]*0.5)
ev("boom",S["B"]["vstart"]+0.6)
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
GREEN=(30,150,70); REDC=(220,40,50); NAV=(46,58,89); YELC=(255,214,10); INK=(25,25,25)
def mom(d,cx,cy,r,mood,tau):
    d.ellipse((cx-r*1.15,cy-r*1.05,cx+r*1.15,cy+r*1.35),fill=(120,70,40))
    face(d,cx,cy,r,mood,tau,skin=(250,210,175))
def laptop(d,cx,cy,w,screen=(230,240,250)):
    h=int(w*0.62); d.rounded_rectangle((cx-w//2,cy-h,cx+w//2,cy),18,fill=(60,64,75)); d.rectangle((cx-w//2+16,cy-h+16,cx+w//2-16,cy-14),fill=screen)
    d.rounded_rectangle((cx-w//2-50,cy,cx+w//2+50,cy+28),12,fill=(90,95,108))
def check(d,x,y,s,col=GREEN,w=12): d.line((x,y,x+s*0.35,y+s*0.4,x+s,y-s*0.45),fill=col,width=w)
def scene_H(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=NAV)
    # title visible from frame 0 (no empty first frame), gentle pulse
    pul=1+0.03*math.sin(tau*6)
    d.rounded_rectangle((540-430,280,540+430,420),34,fill=REDC); ctext(d,300,"CUKR з дивана",font(int(76*pul)),"white")
    p=back(prog(tau,0.0,0.35)); k=0.6+0.4*clamp(p,0,1.2)
    d.rounded_rectangle((540-200,470,540+200,560),40,fill=YELC); ctext(d,484,"5 кроків",font(60),INK)
    mom(d,380,860,int(150*k),"calm",tau)
    d.rounded_rectangle((380-140,860+150*k-30,380+140,1180),60,fill=(200,80,110))
    laptop(d,720,1080,300); ctext(d,890,"MOS",font(64),GREEN,cx=720)
    if tau>0.8: check(d,820,820,70)
def scene_1(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=CREAM); D=s["dur"]
    partial_line(d,[(110,420),(500,420),(500,720),(110,720),(110,420)],prog(tau,0,0.5))
    if tau>0.3: ctext(d,480,"старий",font(60),INK,cx=305); ctext(d,560,"акаунт",font(60),INK,cx=305)
    t1=D*0.55; partial_line(d,[(130,440),(480,700)],prog(tau,t1,t1+0.25),width=14,fill=REDC); partial_line(d,[(480,440),(130,700)],prog(tau,t1+0.15,t1+0.4),width=14,fill=REDC)
    partial_line(d,[(560,570),(620,570)],prog(tau,0.6,0.8)); 
    if tau>0.8: partial_line(d,[(600,550),(620,570),(600,590)],prog(tau,0.8,0.9))
    p=back(prog(tau,0.7,1.1))
    if p>0.05:
        d.rounded_rectangle((650,420,650+330*p,720),30,fill=GREEN)
        if p>0.9: ctext(d,470,"НОВИЙ",font(58),"white",cx=815); ctext(d,550,"акаунт",font(52),"white",cx=815); check(d,780,660,60,col="white",w=10)
    if tau>1.2: ctext(d,800,"у MOS",font(80),GREEN)
def scene_2(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205))
    d.rounded_rectangle((90,330,900,1130),30,fill="white",outline=(200,200,210),width=4)
    d.rectangle((90,330,900,400),fill=(230,232,240)); 
    for i,c in enumerate([(240,90,90),(240,190,60),(90,190,110)]): d.ellipse((120+i*45,350,148+i*45,378),fill=c)
    d.rounded_rectangle((280,345,860,385),18,fill="white"); d.text((300,350),"login.gov.pl",font=font(30,False),fill=(60,60,70))
    d.rounded_rectangle((180,450,810,530),20,fill=(220,40,50)); ctext(d,465,"Zaloguj się",font(46),"white",cx=495)
    labels=["Imię i nazwisko","PESEL","Adres w Polsce","Dane paszportu"]
    for i,l in enumerate(labels):
        y=600+i*120; d.text((180,y),l,font=font(32,False),fill=(90,90,100))
        d.rounded_rectangle((180,y+40,810,y+95),14,outline=(180,180,195),width=3)
        fp=prog(tau,0.6+i*0.45,1.0+i*0.45)
        if fp>0: d.rounded_rectangle((190,y+52,190+600*fp,y+83),10,fill=(200,220,245))
        if fp>=1: check(d,760,y+70,35,w=8)
    # cursor
    cy=600+min(3,int(max(0,tau-0.6)/0.45))*120+68; cx=190+600*prog((tau-0.6)%0.45,0,0.45)
    d.polygon([(cx,cy),(cx+28,cy+34),(cx+12,cy+34),(cx+20,cy+56),(cx+10,cy+60),(cx+2,cy+38),(cx-8,cy+48)],fill=INK)
def scene_3(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(18,22,40))
    for x in range(0,W,90): d.line((x,0,x,H),fill=(28,34,60),width=2)
    for y in range(0,H,90): d.line((0,y,W,y),fill=(28,34,60),width=2)
    p=back(prog(tau,0.0,0.35))
    if p>0.05:
        d.rounded_rectangle((540-400*p,290,540+400*p,410),30,fill=REDC)
        if p>0.9: ctext(d,312,"ДО подачі заяви!",font(60),"white")
    v=PAD_BEFORE+s["vdur"]
    for i,(amt,who,f0) in enumerate([("340 zł","місто (опłata skarbowa)",0.3),("100 zł","ужонд (за карту)",0.47)]):
        st=v*f0; q=ease(prog(tau,st,st+0.35))
        if q<=0: continue
        x=W-(W-60)*q; y=500+i*200
        d.rounded_rectangle((x,y,x+840,y+165),30,fill=(36,44,78))
        d.text((x+40,y+28),amt,font=font(80),fill=YELC); d.text((x+380,y+40),who.split(" (")[0],font=font(50),fill="white")
        d.text((x+380,y+100),"("+who.split(" (")[1],font=font(30,False),fill=(170,180,210))
    st=v*0.62; q=back(prog(tau,st,st+0.4))
    if q>0.05:
        d.rounded_rectangle((540-300*q,930,540+300*q,1090),40,fill=YELC)
        if q>0.9: ctext(d,955,"= 440 zł",font(96),INK)
def scene_4(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=CREAM)
    partial_line(d,[(90,330),(400,330),(400,730),(90,730),(90,330)],prog(tau,0,0.6),width=10)
    if tau>0.5:
        sc=ease(prog(tau,0.5,0.9)); mom(d,245,510,int(95*max(0.05,sc)),"calm",tau)
        d.rounded_rectangle((245-95,610,245+95,730),36,fill=(200,80,110))
    if tau>0.7: ctext(d,750,"35 × 45 мм",font(42),INK,cx=245)
    items=["до 6 місяців","світлий фон","від 684×883 px","+ чеки оплат"]
    for i,t in enumerate(items):
        st=0.6+i*0.55; q=ease(prog(tau,st,st+0.3))
        if q<=0: continue
        y=360+i*130; x=450+(1-q)*400
        check(d,x,y+40,45,w=9); d.text((x+65,y+12),t,font=font(40),fill=INK)
def scene_5(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205))
    d.rounded_rectangle((200,300,880,1100),24,fill="white",outline=(200,200,210),width=4)
    for i in range(6): d.line((260,400+i*60,820-(i%2)*120,400+i*60),fill=(210,210,220),width=10)
    # signature drawn
    pts=[(300+i*9,850+math.sin(i/3.0)*40*(1 if i<30 else 0.5)) for i in range(55)]
    partial_line(d,pts,prog(tau,0.4,1.6),width=8,fill=(30,60,160))
    d.text((300,920),"Profil Zaufany / podpis osobisty",font=font(30,False),fill=(90,90,100))
    q=back(prog(tau,PAD_BEFORE+s["vdur"]*0.6,PAD_BEFORE+s["vdur"]*0.6+0.4))
    if q>0.05:
        d.ellipse((700-110*q,980-110*q,700+110*q,980+110*q),fill=GREEN)
        if q>0.9: ctext(d,950,"UPO",font(56),"white",cx=700)
def scene_B(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=NAV)
    p=back(prog(tau,0.0,0.3))
    if p>0.05:
        d.rounded_rectangle((540-300*p,280,540+300*p,400),30,fill=YELC)
        if p>0.9: ctext(d,300,"БОНУС",font(70),INK)
    # fingerprint icon
    cx,cy=540,640
    for r in range(30,170,22): d.arc((cx-r,cy-r*1.2,cx+r,cy+r*1.2),200,520,fill=(200,210,230),width=9)
    hit=0.6
    if tau>hit:
        partial_line(d,[(cx-170,cy-200),(cx+170,cy+200)],prog(tau,hit,hit+0.25),width=24,fill=REDC)
        ctext(d,880,"НЕ потрібні",font(70),REDC)
    if tau>PAD_BEFORE+s["vdur"]*0.55:
        d.rounded_rectangle((70,990,920,1110),30,fill=CREAM); ctext(d,1017,"До ужонду — тільки по карту",font(44),NAV,cx=495)
def scene_E(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=NAV)
    p=back(prog(tau,0.0,0.4))
    mom(d,540,560,int(150*max(0.05,p)),"calm",tau+1)
    if p>0.05:
        d.rounded_rectangle((540-400*p,800,540+400*p,960),45,fill=YELC)
        if p>0.9: ctext(d,835,"ПЕРЕШЛИ ДРУГУ",font(68),INK)
    if p>0.9: ctext(d,1010,"+ підпишись: нові відео щодня",font(42),"white")
    if p>0.9: ctext(d,1090,"Станом на 28.11.2026. Не є юридичною консультацією.",font(28,False),(190,200,225),maxw=860)
def progress(d,s):
    k=s["scene"]
    if k not in "12345": return
    n=int(k); x0,y0,w,h=140,235,800,16
    for i in range(5):
        d.rounded_rectangle((x0+i*(w/5)+4,y0,x0+(i+1)*(w/5)-4,y0+h),8,fill=YELC if i<n else (120,125,140))
FN={"H":scene_H,"1":scene_1,"2":scene_2,"3":scene_3,"4":scene_4,"5":scene_5,"B":scene_B,"E":scene_E}
CREAM=(250,248,240)
N=int(TOTAL*FPS)
cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","mix.wav",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-profile:v","high","-c:a","aac","-b:a","160k","-ar","44100","-shortest","-movflags","+faststart","video05_cukr_mos_5krokiv.mp4"]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    s=segs[-1]
    for sg in segs:
        if sg["start"]<=t<sg["start"]+sg["dur"]: s=sg; break
    img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img,"RGBA")
    FN[s["scene"]](d,img,t-s["start"],s)
    R.brand(d,dark=(s["scene"] in "14"))
    progress(d,s)
    caption(d,t)
    # flash transition
    for sg in segs[1:]:
        dt=t-sg["start"]
        if 0<=dt<0.18: d.rectangle((0,0,W,H),fill=(255,255,255,int(160*(1-dt/0.18))))
    p.stdin.write(img.tobytes())
    if i%int(FPS*4)==0: img.save(f"frame_{i//FPS:02d}.png")
p.stdin.close(); p.wait(); print("ok")
