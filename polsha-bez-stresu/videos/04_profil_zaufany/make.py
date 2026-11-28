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
 ("H","Поки одні стоять у черзі в ужонді,|інші роблять те саме з дивана.|Секрет — Profil Zaufany:|один раз підтвердиш,|і далі все онлайн.",
      f"по{A}ки одні{A} стоя{A}ть у че{A}рзі в ужо{A}нді, і{A}нші ро{A}блять те са{A}ме з дива{A}на. секре{A}т — про{A}філь зауфа{A}ни: оди{A}н раз підтве{A}рдиш — і да{A}лі все онла{A}йн."),
 ("W","Це твій безкоштовний|електронний підпис|для державних справ.|Діє три роки.",
      f"це твій безкошто{A}вний електро{A}нний пі{A}дпис для держа{A}вних справ. ді{A}є три ро{A}ки."),
 ("U","З ним ти з дивана:|подаєш заяву на CUKR,|оформлюєш 800+ через ZUS,|бачиш рецепти від лікаря|і подаєш податкову декларацію.",
      f"з ним ти з дива{A}на: подає{A}ш зая{A}ву на цукр, оформлює{A}ш ві{A}сімсот плюс через зус, ба{A}чиш реце{A}пти від лі{A}каря і подає{A}ш пода{A}ткову деклара{A}цію."),
 ("K","Як зробити?|Перше — заповни заявку онлайн|на сайті Profil Zaufany.|Друге — прийди з паспортом|і підтверди дані особисто:|в ужонді гміни, ZUS чи податковій.",
      f"як зроби{A}ти? пе{A}рше — запо{A}вни зая{A}вку онла{A}йн, на са{A}йті про{A}філю зауфа{A}ни. дру{A}ге — прийди{A} з па{A}спортом і підтве{A}рди да{A}ні особи{A}сто: в ужо{A}нді гмі{A}ни, зус чи пода{A}тковій."),
 ("E","Перешли тому,|хто досі стоїть у чергах!|І підпишись.",
      f"перешли{A} тому{A}, хто до{A}сі стої{A}ть у черга{A}х! і підпиши{A}сь."),
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
    for a,b in [("CUKR","цукр"),("UKR","укр"),("MOS","мос"),("ZUS","зус"),("Profil Zaufany","профіль зауфани")]: c=c.replace(a,b)
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
ev("boom",S["H"]["vstart"]+S["H"]["vdur"]*0.75)
for k in range(4): ev("pop",S["U"]["vstart"]+S["U"]["vdur"]*(0.15+k*0.21))
ev("pop",S["K"]["vstart"]+S["K"]["vdur"]*0.15); ev("pop",S["K"]["vstart"]+S["K"]["vdur"]*0.55)
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
GREEN=(30,150,70); REDC=(220,40,50); NAV=(46,58,89); YELC=(255,214,10); INK=(25,25,25); GREY=(150,155,170)
def mom(d,cx,cy,r,mood,tau):
    d.ellipse((cx-r*1.15,cy-r*1.05,cx+r*1.15,cy+r*1.35),fill=(120,70,40))
    face(d,cx,cy,r,mood,tau,skin=(250,210,175))
def check(d,x,y,s,col=GREEN,w=12): d.line((x,y,x+s*0.35,y+s*0.4,x+s,y-s*0.45),fill=col,width=w)
def phone(d,cx,cy,h,col=(30,30,35)):
    w=int(h*0.52); d.rounded_rectangle((cx-w//2,cy-h//2,cx+w//2,cy+h//2),22,fill=col); d.rounded_rectangle((cx-w//2+10,cy-h//2+26,cx+w//2-10,cy+h//2-26),12,fill="white")
def scene_H(d,img,tau,s):
    d.rectangle((0,0,W//2,H),fill=(70,74,90)); d.rectangle((W//2,0,W,H),fill=NAV)
    d.rounded_rectangle((90,280,990,410),34,fill=REDC); ctext(d,300,"Черга чи диван?",font(72),"white")
    # left: queue
    d.rounded_rectangle((60,470,470,550),16,fill=(200,60,60)); ctext(d,482,"URZĄD",font(48),"white",cx=265)
    for i in range(5):
        x=110+i*80; y=760+int(6*math.sin(tau*3+i))
        d.ellipse((x-28,y-28,x+28,y+28),fill=GREY); d.rounded_rectangle((x-30,y+30,x+30,y+150),20,fill=(110,115,130))
    hero_mood="shock" if tau>PAD_BEFORE+s["vdur"]*0.3 else "calm"
    face(d,265,1010,85,hero_mood,tau,skin=(240,200,160)); d.rounded_rectangle((185,1095,345,1180),30,fill=(90,120,170))
    # right: couch
    d.rounded_rectangle((590,960,1010,1100),40,fill=(150,90,60)); d.rounded_rectangle((570,880,640,1100),30,fill=(130,75,50)); d.rounded_rectangle((960,880,1030,1100),30,fill=(130,75,50))
    mom(d,800,790,110,"calm",tau+0.5); d.rounded_rectangle((700,890,900,1000),40,fill=(200,80,110))
    phone(d,900,880,120)
    if tau>PAD_BEFORE+s["vdur"]*0.45: check(d,860,880,60,w=10)
    if tau>PAD_BEFORE+s["vdur"]*0.72:
        p=back(prog(tau,PAD_BEFORE+s["vdur"]*0.72,PAD_BEFORE+s["vdur"]*0.72+0.35))
        if p>0.05:
            d.rounded_rectangle((540-330*p,580,540+330*p,690),36,fill=YELC)
            if p>0.9: ctext(d,598,"Profil Zaufany",font(58),INK)
def scene_W(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=CREAM)
    partial_line(d,[(330,330),(750,330),(750,1050),(330,1050),(330,330)],prog(tau,0,0.6),width=10)
    if tau>0.4: ctext(d,420,"Profil",font(70),(30,90,170)); ctext(d,500,"Zaufany",font(70),(30,90,170))
    pts=[(400+i*7,700+math.sin(i/2.5)*30) for i in range(40)]
    partial_line(d,pts,prog(tau,0.6,1.4),width=8,fill=(30,60,160))
    partial_line(d,[(390,760),(690,760)],prog(tau,0.6,0.9),width=4,fill=INK)
    v=PAD_BEFORE+s["vdur"]
    tags=[("безкоштовно",0.35,(30,150,70)),("3 роки",0.8,REDC)]
    for t,f0,col in tags:
        q=back(prog(tau,v*f0,v*f0+0.35))
        if q>0.05:
            y=860 if t=="безкоштовно" else 950
            d.rounded_rectangle((540-200*q,y,540+200*q,y+75),36,fill=col)
            if q>0.9: ctext(d,y+12,t,font(44),"white")
def scene_U(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(18,22,40))
    for x in range(0,W,90): d.line((x,0,x,H),fill=(28,34,60),width=2)
    for y in range(0,H,90): d.line((0,y,W,y),fill=(28,34,60),width=2)
    ctext(d,290,"Що можна з дивана",font(66),"white")
    items=[("Заява CUKR","MOS"),("800+","ZUS"),("Рецепти, направлення","IKP"),("Податкова декларація","e-Urząd Skarbowy")]
    for i,(a,b) in enumerate(items):
        st=PAD_BEFORE+s["vdur"]*(0.15+i*0.21)-0.15; q=ease(prog(tau,st,st+0.35))
        if q<=0: continue
        x=W-(W-60)*q; y=420+i*175
        d.rounded_rectangle((x,y,x+840,y+145),28,fill=(36,44,78))
        d.ellipse((x+25,y+30,x+110,y+115),fill=(60,200,130)); check(d,x+45,y+75,45,col="white",w=9)
        d.text((x+135,y+22),a,font=font(48),fill="white"); d.text((x+135,y+85),b,font=font(32,False),fill=(170,180,210))
def scene_K(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=(255,235,205))
    ctext(d,290,"Як зробити?",font(70),NAV)
    v=PAD_BEFORE+s["vdur"]
    q=ease(prog(tau,v*0.12,v*0.12+0.4))
    if q>0:
        x=W-(W-60)*q
        d.rounded_rectangle((x,410,x+840,620),30,fill=(30,90,170))
        d.text((x+40,440),"1. Заявка онлайн",font=font(58),fill="white")
        d.text((x+40,530),"pz.gov.pl",font=font(44,False),fill=(210,225,250))
    
    q=ease(prog(tau,v*0.45,v*0.45+0.4))
    if q>0:
        x=W-(W-60)*q
        d.rounded_rectangle((x,730,x+840,1090),30,fill="white",outline=(200,200,210),width=4)
        d.text((x+40,755),"2. Підтвердити особисто",font=font(48),fill=NAV)
        d.text((x+40,830),"з паспортом:",font=font(40,False),fill=INK)
        d.text((x+40,895),"ужонд гміни · ZUS",font=font(44),fill=REDC)
        d.text((x+40,960),"· податкова",font=font(44),fill=REDC)
        check(d,x+720,1010,60,w=10)
    if tau>v*0.8: ctext(d,1120,"деякі банки дозволяють онлайн — перевір у своєму",font(26,False),(110,110,120),maxw=860)
def scene_E(d,img,tau,s):
    d.rectangle((0,0,W,H),fill=NAV)
    p=back(prog(tau,0.0,0.4))
    mom(d,540,560,int(150*max(0.05,p)),"calm",tau+1)
    if p>0.05:
        d.rounded_rectangle((540-400*p,800,540+400*p,960),45,fill=YELC)
        if p>0.9: ctext(d,835,"ПЕРЕШЛИ ДРУГУ",font(68),INK)
    if p>0.9: ctext(d,1010,"+ підпишись: нові відео щодня",font(42),"white")
    if p>0.9: ctext(d,1090,"Джерело: gov.pl, станом на 28.11.2026.",font(28,False),(190,200,225),maxw=860)
def progress(d,s): return
FN={"H":scene_H,"W":scene_W,"U":scene_U,"K":scene_K,"E":scene_E}
CREAM=(250,248,240)
N=int(TOTAL*FPS)
cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","mix.wav",
     "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-profile:v","high","-c:a","aac","-b:a","160k","-ar","44100","-shortest","-movflags","+faststart","video04_profil_zaufany.mp4"]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(N):
    t=i/FPS
    s=segs[-1]
    for sg in segs:
        if sg["start"]<=t<sg["start"]+sg["dur"]: s=sg; break
    img=Image.new("RGB",(W,H)); d=ImageDraw.Draw(img,"RGBA")
    FN[s["scene"]](d,img,t-s["start"],s)
    R.brand(d,dark=(s["scene"] in "WK"))
    progress(d,s)
    caption(d,t)
    # flash transition
    for sg in segs[1:]:
        dt=t-sg["start"]
        if 0<=dt<0.18: d.rectangle((0,0,W,H),fill=(255,255,255,int(160*(1-dt/0.18))))
    p.stdin.write(img.tobytes())
    if i%int(FPS*4)==0: img.save(f"frame_{i//FPS:02d}.png")
p.stdin.close(); p.wait(); print("ok")
