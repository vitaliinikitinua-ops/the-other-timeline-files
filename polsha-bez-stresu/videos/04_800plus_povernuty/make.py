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
 ("H","800+ раптом перестали платити?|Ти не один — це торкнулося|150 тисяч українців.",
      f"ві{A}сімсот плюс ра{A}птом переста{A}ли плати{A}ти? ти не оди{A}н — це торкну{A}лося ста п'ятдесяти{A} ти{A}сяч украї{A}нців."),
 ("C","З 31 січня ZUS зупинив виплату|всім зі статусом UKR.|Щоб отримувати знову,|треба подати нову заяву.",
      f"з тридця{A}ть пе{A}ршого сі{A}чня зус зупини{A}в ви{A}плату всім зі ста{A}тусом у ка ер. щоб отри{A}мувати зно{A}ву, тре{A}ба пода{A}ти нову{A} зая{A}ву."),
 ("U","І три умови: хтось із батьків|працює і платить внески,|дитина в польській школі,|і вся сім'я живе в Польщі.",
      f"і три умо{A}ви: хтось із батькі{A}в працю{A}є і пла{A}тить вне{A}ски, дити{A}на — в по{A}льській шко{A}лі, і вся сім'я{A} живе{A} в по{A}льщі."),
 ("1","Що зробити?|Перше — перевір|у eZUS свої внески.",
      f"що зроби{A}ти? пе{A}рше — переві{A}р у е зус свої{A} вне{A}ски."),
 ("2","Друге — подай нову заяву|через eZUS, банк або mZUS.",
      f"дру{A}ге — пода{A}й нову{A} зая{A}ву че{A}рез е зус, банк або{A} ем зус."),
 ("3","Третє — відповідь|прийде в eZUS.",
      f"тре{A}тє — ві{A}дповідь при{A}йде в е зус."),
 ("B","Не відкладай! Гроші рахують|з місяця, коли подав заяву.|За пропущені не доплатять.",
      f"не відклада{A}й! гро{A}ші раху{A}ють з мі{A}сяця, коли{A} пода{A}в зая{A}ву. за пропу{A}щені не доплатя{A}ть."),
 ("E","Перешли тому,|хто досі чекає на 800+!|І підпишись.",
      f"перешли{A} тому{A}, хто до{A}сі чека{A}є на ві{A}сімсот плюс! і підпиши{A}сь."),
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
    nz=np.where(np.abs(a)>0.01)[0]; a=a[max(0,nz[0]-2500):nz[-1]+1500]
    a=a/max(1e-6,np.abs(a).max())*0.9
    return a,sr
import re, difflib
from faster_whisper import WhisperModel
ASR=WhisperModel("small",device="cpu",compute_type="int8")
NUMW={"0":"нуль","1":"один","2":"два","3":"три","ноль":"нуль","моз":"мос","спокойно":"спокійно","аккаунт":"акаунт","27го":"27","4е":"4","четверте":"4","єзус":"е","езус":"е","ezus":"е","мзус":"ем","mzus":"ем"}
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
    for a,b in [("eZUS","е зус"),("mZUS","ем зус"),("800+","800 плюс"),("150","150"),("CUKR","цукр"),("UKR","укр"),("MOS","мос"),("ZUS","зус"),("Profil Zaufany","профіль зауфани")]: c=c.replace(a,b)
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
ev("boom",S["H"]["vstart"]+0.2)
ev("boom",S["C"]["vstart"]+S["C"]["vdur"]*0.35)
for k in range(3): ev("pop",S["U"]["vstart"]+S["U"]["vdur"]*(0.25+k*0.25))
for k in "123": ev("pop",S[k]["vstart"]+0.3)
ev("pop",S["B"]["vstart"]+S["B"]["vdur"]*0.5)
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
KEEP=["з місяця","статус UKR","крок за кроком","статус UKR","карта побиту","портал MOS","акаунт у MOS","до 4 березня","4 березня 2027","440 злотих","800+:","польської школи","всієї сім'ї"]
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
GREEN=(30,150,70); REDC=(220,40,50); NAV=(46,58,89); YELC=(255,214,10); INK=(25,25,25); GREY=(150,155,170)
def mom(d,cx,cy,r,mood,tau):
    d.ellipse((cx-r*1.15,cy-r*1.05,cx+r*1.15,cy+r*1.35),fill=(120,70,40))
    face(d,cx,cy,r,mood,tau,skin=(250,210,175))
def check(d,x,y,s,col=GREEN,w=12): d.line((x,y,x+s*0.35,y+s*0.4,x+s,y-s*0.45),fill=col,width=w)
def phone(d,cx,cy,h,col=(30,30,35)):
    w=int(h*0.52); d.rounded_rectangle((cx-w//2,cy-h//2,cx+w//2,cy+h//2),22,fill=col); d.rounded_rectangle((cx-w//2+10,cy-h//2+26,cx+w//2-10,cy+h//2-26),12,fill="white")
def card(d,x,y,w,h,fill,outline=None): d.rounded_rectangle((x,y,x+w,y+h),30,fill=fill,outline=outline,width=4 if outline else 0)
def slide_x(tau,st): q=ease(prog(tau,st,st+0.35)); return W-(W-90)*q, q
def scene_H(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=NAV)
    d.rounded_rectangle((90,280,990,410),34,fill=REDC); ctext(d,300,"800+ НЕ ПРИЙШЛО?",font(74),"white")
    v=s["vdur"]; shock=tau>PAD_BEFORE+0.15
    sh=math.sin(tau*80)*12*(1-prog(tau,0.3,0.9)) if shock else 0
    mom(d,330+sh,780,150,"shock" if shock else "calm",tau)
    d.rounded_rectangle((200+sh,930,460+sh,1160),60,fill=(200,80,110))
    # phone with bank notification
    cx,cy=690,830; phone(d,cx,cy,520)
    d.rounded_rectangle((cx-115,cy-200,cx+115,cy-120),16,fill=(235,238,245)); d.text((cx-100,cy-188),"ZUS · 800+",font=font(30),fill=NAV)
    d.text((cx-100,cy-150),"wypłata",font=font(26,False),fill=GREY)
    p=back(prog(tau,PAD_BEFORE+0.15,PAD_BEFORE+0.5))
    if p>0.05: ctext(d,cy-70,"0 zł",font(int(90*min(1,p))),REDC,cx=cx)
    if tau>PAD_BEFORE+v*0.5:
        q=back(prog(tau,PAD_BEFORE+v*0.5,PAD_BEFORE+v*0.5+0.35))
        if q>0.05:
            d.rounded_rectangle((540-360*q,1040,540+360*q,1140),36,fill=YELC)
            if q>0.9: ctext(d,1058,"~150 000 українців",font(54),INK)
def scene_C(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=CREAM)
    partial_line(d,[(300,330),(780,330),(780,800),(300,800),(300,330)],prog(tau,0,0.6),width=10)
    if tau>0.4: partial_line(d,[(300,450),(780,450)],prog(tau,0.4,0.7),width=10)
    if tau>0.6: ctext(d,365,"СІЧЕНЬ"[:int(6*prog(tau,0.6,0.9))],font(50),INK)
    if tau>0.9: ctext(d,490,"31",font(190),REDC)
    if tau>1.1: ctext(d,700,"2026"[:int(4*prog(tau,1.1,1.4))],font(52),INK)
    v=PAD_BEFORE+s["vdur"]
    q=back(prog(tau,v*0.3,v*0.3+0.3))
    if q>0.05:
        # STOP stamp, rotated look via thick outline
        d.rounded_rectangle((540-330*q,850,540+330*q,1010),24,outline=REDC,width=12,fill=(255,235,235))
        if q>0.9: ctext(d,872,"STOP 800+",font(64),REDC); ctext(d,950,"для статусу UKR",font(36),REDC)
    q=back(prog(tau,v*0.62,v*0.62+0.3))
    if q>0.05:
        d.rounded_rectangle((540-300*q,1060,540+300*q,1150),40,fill=GREEN)
        if q>0.9: ctext(d,1074,"→ нова заява",font(52),"white")
def scene_U(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(18,22,40))
    for x in range(0,W,90): d.line((x,0,x,H),fill=(28,34,60),width=2)
    for y in range(0,H,90): d.line((0,y,W,y),fill=(28,34,60),width=2)
    ctext(d,280,"3 умови для 800+",font(66),"white")
    items=[("Батьки працюють","внески ZUS ≥ 50% мінімалки"),("Дитина в польській школі","від 6 років · дані в SIO"),("Живете в Польщі","і батьки, і дитина")]
    for i,(a,b) in enumerate(items):
        st=PAD_BEFORE+s["vdur"]*(0.25+i*0.25)-0.15; x,q=slide_x(tau,st)
        if q<=0: continue
        y=400+i*190
        d.rounded_rectangle((x-30,y,x+810,y+160),28,fill=(36,44,78))
        d.ellipse((x-5,y+35,x+85,y+125),fill=(60,200,130)); check(d,x+15,y+82,48,col="white",w=9)
        d.text((x+110,y+28),a,font=font(42),fill="white"); d.text((x+110,y+95),b,font=font(32,False),fill=(170,180,210))
    if tau>PAD_BEFORE+s["vdur"]*0.85:
        ctext(d,990,"Виняток: дитина з інвалідністю",font(32),(255,214,10),maxw=820)
        ctext(d,1035,"(польське рішення) — без умови роботи",font(30,False),(200,205,225),maxw=820)
def step_title(d,n,txt): ctext(d,290,f"Крок {n}/3",font(44),NAV); ctext(d,350,txt,font(62),INK,maxw=840)
def scene_1(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205)); step_title(d,1,"Перевір внески")
    x,q=slide_x(tau,0.2)
    if q>0:
        cx=int(x+380); phone(d,cx,800,560)
        d.rounded_rectangle((cx-125,560,cx+125,640),16,fill=(0,120,60)); ctext(d,575,"eZUS",font(44),"white",cx=cx)
        for i,(m,ok) in enumerate([("październik",True),("listopad",True)]):
            y=680+i*110; d.rounded_rectangle((cx-125,y,cx+125,y+90),14,fill=(235,245,238))
            d.text((cx-110,y+12),m,font=font(28,False),fill=INK); d.text((cx-110,y+48),"składki",font=font(26),fill=GREEN)
            if tau>0.7+i*0.4: check(d,cx+60,y+50,40,w=8)
def scene_2(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205)); step_title(d,2,"Нова заява онлайн")
    chips=[("eZUS",(0,120,60)),("Банк",(30,90,170)),("mZUS",(230,120,30))]
    for i,(c,col) in enumerate(chips):
        x,q=slide_x(tau,0.2+i*0.45)
        if q<=0: continue
        y=500+i*190; d.rounded_rectangle((x,y,x+780,y+150),34,fill=col)
        ctext(d,y+38,c,font(66),"white",cx=int(x+390))
    if tau>1.6: ctext(d,1090,"також: Emp@tia · тільки онлайн",font(32,False),(110,110,120))
def scene_3(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205)); step_title(d,3,"Відповідь прийде в eZUS")
    x,q=slide_x(tau,0.2)
    if q>0:
        d.rounded_rectangle((x,520,x+800,1000),30,fill="white",outline=(200,200,210),width=4)
        # envelope
        ex,ey=int(x+400),660
        d.rectangle((ex-170,ey-90,ex+170,ey+110),fill=(250,240,210),outline=INK,width=6)
        d.line((ex-170,ey-90,ex,ey+30,ex+170,ey-90),fill=INK,width=6)
        ctext(d,820,"Informacja o przyznaniu",font(42),NAV,cx=ex)
        ctext(d,885,"+ лист на e-mail",font(36,False),GREY,cx=ex)
        if tau>0.8: check(d,ex+130,ey-110,70,w=12)
def scene_B(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=CREAM)
    ctext(d,290,"Не відкладай!",font(80),REDC)
    months=["лют","бер","кві","тра","чер","лип","сер","вер","жов","лис"]
    for i,m in enumerate(months):
        r,c=divmod(i,5); x=100+c*160; y=470+r*210
        st=0.1+i*0.06
        if tau<st: continue
        cur=(i==len(months)-1)
        d.rounded_rectangle((x,y,x+140,y+170),20,fill=GREEN if cur else (225,225,230))
        ctext(d,y+55,m,font(42),"white" if cur else GREY,cx=x+70)
        if not cur and tau>PAD_BEFORE+s["vdur"]*0.5: d.line((x+20,y+150,x+120,y+20),fill=REDC,width=10)
    if tau>PAD_BEFORE+s["vdur"]*0.3:
        q=back(prog(tau,PAD_BEFORE+s["vdur"]*0.3,PAD_BEFORE+s["vdur"]*0.3+0.35))
        if q>0.05:
            d.rounded_rectangle((540-360*q,940,540+360*q,1040),36,fill=YELC)
            if q>0.9: ctext(d,960,"гроші — з місяця заяви",font(48),INK)
    ctext(d,1080,"*приклад: заява в листопаді",font(28,False),GREY)
def scene_E(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=NAV)
    p=back(prog(tau,0.0,0.4))
    mom(d,540,560,int(150*max(0.05,p)),"calm",tau+1)
    if p>0.05:
        d.rounded_rectangle((540-400*p,800,540+400*p,960),45,fill=YELC)
        if p>0.9: ctext(d,835,"ПЕРЕШЛИ ДРУГУ",font(68),INK)
    if p>0.9: ctext(d,1010,"+ підпишись: нові відео щодня",font(42),"white")
    if p>0.9: ctext(d,1090,"Джерело: zus.pl, gov.pl, станом на 28.11.2026.",font(28,False),(190,200,225),maxw=860)
def progress(d,s):
    k=s["scene"]
    if k not in "123": return
    n=int(k); x0,y0,w,h=140,235,800,16
    for i in range(3):
        d.rounded_rectangle((x0+i*(w/3)+4,y0,x0+(i+1)*(w/3)-4,y0+h),8,fill=YELC if i<n else (120,125,140))
FN={"H":scene_H,"C":scene_C,"U":scene_U,"1":scene_1,"2":scene_2,"3":scene_3,"B":scene_B,"E":scene_E}
CREAM=(250,248,240)
N=int(TOTAL*FPS)
cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","mix.wav",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-profile:v","high","-c:a","aac","-b:a","160k","-ar","44100","-shortest","-movflags","+faststart","video04_800plus_povernuty.mp4"]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    s=segs[-1]
    for sg in segs:
        if sg["start"]<=t<sg["start"]+sg["dur"]: s=sg; break
    img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img,"RGBA")
    FN[s["scene"]](d,img,t-s["start"],s)
    R.brand(d,dark=(s["scene"] in "C123"))
    progress(d,s)
    caption(d,t)
    # flash transition
    for sg in segs[1:]:
        dt=t-sg["start"]
        if 0<=dt<0.18: d.rectangle((0,0,W,H),fill=(255,255,255,int(160*(1-dt/0.18))))
    p.stdin.write(img.tobytes())
    if i%int(FPS*4)==0: img.save(f"frame_{i//FPS:02d}.png")
p.stdin.close(); p.wait(); print("ok")
