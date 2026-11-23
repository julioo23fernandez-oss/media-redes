import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, sys
sr=44100; D=float(sys.argv[1]); OUT=sys.argv[2]; STY=sys.argv[3]
BPM=100; n=int(sr*D); beat=60/BPM; rng=np.random.default_rng(11)
L=np.zeros(n); R=np.zeros(n)
def f(m): return 440*2**((m-69)/12)
def add(w,s,pan=.5,g=1.):
    a=int(s*sr)
    if a<0 or a>=n: return
    b=min(n,a+len(w)); w=w[:b-a]*g; L[a:b]+=w*(1-pan); R[a:b]+=w*pan
def noise(d,lo,hi):
    x=rng.standard_normal(int(d*sr)); b,a=ss.butter(2,[lo/(sr/2),hi/(sr/2)],'band'); return ss.lfilter(b,a,x)
def kick(g=.9):
    t=np.arange(int(.3*sr))/sr; fr=50+90*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-t*8)*g
def snap():
    t=np.arange(int(.12*sr))/sr; return noise(.12,1500,8000)*np.exp(-t*40)*.3
def clap():
    t=np.arange(int(.25*sr))/sr; e=np.exp(-t*22)
    for dd in (.008,.017): e+=np.roll(np.exp(-t*80),int(dd*sr))*.6
    return noise(.25,900,7000)*e*.35
def hat(o=False):
    d=.15 if o else .04; t=np.arange(int(d*sr))/sr; x=rng.standard_normal(len(t)); b,a=ss.butter(2,8000/(sr/2),'high')
    return ss.lfilter(b,a,x)*np.exp(-t*(15 if o else 90))*.08
def ks(m,d=.8,v=1.,bright=.5):  # Karplus-Strong: guitarra/ukelele
    N=int(sr/f(m)); buf=rng.uniform(-1,1,N); out=np.zeros(int(d*sr)); 
    for i in range(len(out)):
        out[i]=buf[i%N]; buf[i%N]=bright*buf[i%N]+(1-bright)*buf[(i+1)%N]*.996 if False else .5*(buf[i%N]+buf[(i+1)%N])*.994
    return out*.25*v
def epiano(ch,d,v=1.):
    t=np.arange(int(d*sr))/sr; w=sum(np.sin(2*np.pi*f(m)*t+ .3*np.sin(2*np.pi*f(m)*2*t)*np.exp(-t*4)) for m in ch)
    return w*np.minimum(1,t/.004)*np.exp(-t*2.2)*.06*v
def whistle(m,d):
    t=np.arange(int(d*sr))/sr; vib=1+.006*np.sin(2*np.pi*5.5*t)*np.minimum(1,t/.2)
    w=np.sin(2*np.pi*f(m)*np.cumsum(vib)/sr)+.08*noise(d,1500,4000)[:len(t)]
    return w*np.minimum(1,t/.05)*np.minimum(1,(d-t)/.08)*.09
def bassp(m,d,g=.3):
    t=np.arange(int(d*sr))/sr; w=np.sin(2*np.pi*f(m)*t)+.3*np.sign(np.sin(2*np.pi*f(m)*t))*.3
    return w*np.minimum(1,t/.006)*np.exp(-t*6)*g
def strings(ch,d):
    t=np.arange(int(d*sr))/sr; w=sum(ss.sawtooth(2*np.pi*f(m)*2**(dt/1200)*t) for m in ch for dt in (-6,6))
    b,a=ss.butter(2,2500/(sr/2)); w=ss.lfilter(b,a,w); return w*np.minimum(1,t/.15)*np.minimum(1,(d-t)/.2)*.012
bar=4*beat
if STY=='ukelele':   # acústico, palmas y silbido
    prog=[(48,[60,64,67,72]),(43,[59,62,67,71]),(45,[57,60,64,69]),(41,[57,60,65,69])]
    strum=[0,.5,.75,1.5,2,2.5,3,3.5]
    mel=[(0,76,.5),(.5,79,.5),(1,81,1),(2,79,.5),(2.5,76,.5),(3,74,1)]
    for i in range(int(D/bar)+2):
        t0=i*bar; r,ch=prog[i%4]
        for k,s in enumerate(strum):
            for j,m in enumerate(ch if k%2==0 else ch[::-1]): add(ks(m+12,.6,.9 if k in (0,4) else .6),t0+s*beat+j*.012,.35+.1*j)
        add(bassp(r-12,beat*.9),t0); add(bassp(r-12,beat*.9),t0+2*beat)
        if i>=1:
            for k in range(4):
                add(kick(.7),t0+k*beat) if k in (0,2) else add(clap(),t0+k*beat)
        if i>=2 and i%2==0:
            for s,m,d in mel: add(whistle(m,d*beat*.95),t0+s*beat,.55)
elif STY=='disco':   # funky, bajo en octavas, cuerdas
    prog=[(45,[64,69,72,76]),(50,[62,66,69,74]),(43,[62,67,71,74]),(48,[60,64,67,72])]
    for i in range(int(D/bar)+2):
        t0=i*bar; r,ch=prog[i%4]; add(strings(ch,bar),t0)
        for k in range(4):
            tt=t0+k*beat
            if i>=1:
                add(kick(),tt); add(hat(True),tt+beat/2,.6)
                if k in (1,3): add(clap(),tt)
                for q in (1,3): add(hat(),tt+q*beat/4,.4)
            add(bassp(r-12,beat*.35,.32),tt); add(bassp(r,beat*.3,.25),tt+beat/2)
        for q in (0,1.5,2.5,3.5): add(epiano([c+12 for c in ch],.35,.8),t0+q*beat,.6)
elif STY=='pop':                # 'pop': piano brillante, palmas, campanas
    prog=[(41,[65,69,72,77]),(48,[64,67,72,76]),(45,[64,69,72,76]),(43,[62,67,71,74])]
    for i in range(int(D/bar)+2):
        t0=i*bar; r,ch=prog[i%4]
        for q in range(8): add(epiano(ch,.6,1 if q%2==0 else .7),t0+q*beat/2,.45+.1*(q%2))
        add(bassp(r-12,bar*.5,.28),t0); add(bassp(r-12,bar*.4,.25),t0+2.5*beat)
        if i>=1:
            for k in range(4):
                add(kick(.85),t0+k*beat)
                if k in (1,3): add(clap(),t0+k*beat); add(snap(),t0+k*beat+beat*.75,.7)
                add(hat(),t0+k*beat+beat/2,.35)
        if i%2==1: add(epiano([84,88,91],1.2,.9),t0+3*beat,.7)

def marimba(m,d=.5,v=1.):
    t=np.arange(int(d*sr))/sr; fr=f(m); w=np.sin(2*np.pi*fr*t)+.35*np.sin(2*np.pi*fr*4*t)*np.exp(-t*25)
    return w*np.minimum(1,t/.002)*np.exp(-t*9)*.13*v
def plk(m,d=.4,v=1.):
    t=np.arange(int(d*sr))/sr; w=ss.sawtooth(2*np.pi*f(m)*t)+ss.sawtooth(2*np.pi*f(m)*1.004*t)
    b,a=ss.butter(2,3200/(sr/2)); w=ss.lfilter(b,a,w); return w*np.minimum(1,t/.003)*np.exp(-t*8)*.06*v
if STY=='pop2':   # pop-house: acordes a contratiempo, bombo a negras
    prog=[(45,[64,69,72,76]),(41,[65,69,72,77]),(48,[64,67,72,76]),(43,[62,67,71,74])]
    for i in range(int(D/bar)+2):
        t0=i*bar; r,ch=prog[i%4]
        for k in range(4):
            tt=t0+k*beat
            add(epiano(ch,.32,1.0),tt+beat/2,.5)
            add(bassp(r-12,beat*.4,.3),tt+beat/2)
            if i>=1:
                add(kick(.9),tt); add(hat(True),tt+beat/2,.6)
                if k in (1,3): add(clap(),tt)
        if i%2==1:
            for q,m in enumerate([76,79,81,79]): add(plk(m+12,.3,.8),t0+(2+q*.5)*beat,.65)
elif STY=='pop3': # pop con melodía pegadiza de pluck
    prog=[(48,[60,64,67,72]),(45,[60,64,69,72]),(41,[60,65,69,72]),(43,[59,62,67,71])]
    mel=[[79,76,79,81,79,76,74,76],[76,72,76,79,77,76,74,72],[77,76,77,81,79,77,76,77],[74,71,74,79,77,74,71,74]]
    for i in range(int(D/bar)+2):
        t0=i*bar; r,ch=prog[i%4]
        add(epiano(ch,bar*.9,.8),t0); add(epiano(ch,bar*.5,.6),t0+2*beat)
        add(bassp(r-12,beat*.9,.3),t0); add(bassp(r-12,beat*.5,.25),t0+1.5*beat); add(bassp(r-12,beat*.9,.3),t0+2*beat)
        if i>=1:
            for k in range(4):
                add(kick(.8),t0+k*beat) if k in (0,2) else (add(clap(),t0+k*beat),add(snap(),t0+k*beat,.6))
                for q in (0,1): add(hat(),t0+k*beat+q*beat/2,.35+.3*q)
            for q in range(8): add(plk(mel[i%4][q],.35,1 if q%2==0 else .75),t0+q*beat/2,.5)
elif STY=='pop4': # pop tropical: marimba, palmas y shaker
    prog=[(50,[62,66,69,74]),(47,[62,66,71,74]),(43,[62,67,71,74]),(45,[61,64,69,73])]
    pat=[0,.75,1.5,2,2.75,3.5]
    for i in range(int(D/bar)+2):
        t0=i*bar; r,ch=prog[i%4]
        for j,s_ in enumerate(pat): add(marimba(ch[j%4]+12,.45,1 if j in (0,3) else .8),t0+s_*beat,.3+.4*(j%2))
        add(bassp(r-12,beat*.7,.3),t0); add(bassp(r-12,beat*.5,.28),t0+1.5*beat); add(bassp(r-5,beat*.7,.26),t0+2.5*beat)
        add(epiano(ch,bar,.5),t0)
        if i>=1:
            for k in range(4):
                add(kick(.75),t0+k*beat) if k in (0,2) else add(clap(),t0+k*beat)
                for q in range(4): add(hat(),t0+k*beat+q*beat/4,.4+.2*(q%2),.7 if q%2 else .4)
x=np.stack([L,R],1)
irt=np.arange(int(1.0*sr))/sr
for c in (0,1):
    ir=rng.standard_normal(len(irt))*np.exp(-irt*4.5); ir[0]=0; wet=ss.fftconvolve(x[:,c],ir)[:n]; wet/=np.abs(wet).max()+1e-9
    x[:,c]=x[:,c]/np.abs(x[:,c]).max()+.09*wet
x=np.tanh(x*1.3); fd=np.ones(n); fi=int(.15*sr); fo=int(2.0*sr); fd[:fi]=np.linspace(0,1,fi); fd[-fo:]=np.linspace(1,0,fo)**1.5
x*=fd[:,None]; x=x/np.abs(x).max()*.62; wf.write(OUT,sr,(x*32767).astype(np.int16))
