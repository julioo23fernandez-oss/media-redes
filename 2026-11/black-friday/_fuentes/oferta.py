import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, sys
# Música de oferta: animada (124 bpm), drop cuando entra el producto
sr=44100; D=float(sys.argv[1]); OUT=sys.argv[2]; DROP=float(sys.argv[3]); KEY=int(sys.argv[4]); SEED=int(sys.argv[5])
BPM=124; n=int(sr*D); beat=60/BPM; rng=np.random.default_rng(SEED)
L=np.zeros(n); R=np.zeros(n)
def f(m): return 440*2**((m-69+KEY)/12)
def add(w,s,pan=.5,g=1.):
    a=int(s*sr)
    if a<0 or a>=n: return
    b=min(n,a+len(w)); w=w[:b-a]*g; L[a:b]+=w*(1-pan); R[a:b]+=w*pan
def kick():
    t=np.arange(int(.3*sr))/sr; fr=46+90*np.exp(-t*32); return np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-t*8)
def noise(d,lo,hi):
    x=rng.standard_normal(int(d*sr)); b,a=ss.butter(2,[lo/(sr/2),hi/(sr/2)],'band'); return ss.lfilter(b,a,x)
def clap():
    t=np.arange(int(.22*sr))/sr; e=np.exp(-t*24)
    for dd in (.007,.015): e+=np.roll(np.exp(-t*70),int(dd*sr))*.5
    return noise(.22,1000,6000)*e*.32
def hat(o=False):
    d=.16 if o else .045; t=np.arange(int(d*sr))/sr; x=rng.standard_normal(len(t)); b,a=ss.butter(2,7500/(sr/2),'high')
    return ss.lfilter(b,a,x)*np.exp(-t*(16 if o else 80))*.1
def bass(m,d):
    t=np.arange(int(d*sr))/sr; fr=f(m); w=np.sign(np.sin(2*np.pi*fr*t))*.25+np.sin(2*np.pi*fr*t)
    b,a=ss.butter(2,900/(sr/2)); w=ss.lfilter(b,a,w); return w*np.minimum(1,t/.005)*np.exp(-t*5)*.3
def stab(ch,d):
    t=np.arange(int(d*sr))/sr; w=sum(np.sin(2*np.pi*f(m)*k*t)/k**1.4 for m in ch for k in (1,2,3))
    return w*np.minimum(1,t/.004)*np.exp(-t*7)*.05
def pad(ch,d):
    t=np.arange(int(d*sr))/sr; w=sum(np.sin(2*np.pi*f(m)*2**(dt/12)*t+rng.uniform(0,6)) for m in ch for dt in (-.08,.08))
    return w*np.minimum(1,t/.3)*np.minimum(1,(d-t)/.3)*.016
prog=[(57,[57,60,64,69]),(53,[57,60,65,69]),(48,[55,60,64,67]),(55,[55,59,62,67])]
bar=4*beat
for i in range(int(D/bar)+2):
    t0=i*bar; r,ch=prog[i%4]; add(pad(ch,bar+.3),t0)
    for k in range(4):
        tt=t0+k*beat
        if tt<DROP:
            add(stab([c+12 for c in ch],.25),tt,.5,.5); continue
        add(kick(),tt,.5,.95)
        if k in (1,3): add(clap(),tt)
        add(bass(r-12,beat*.42),tt); add(bass(r,beat*.4),tt+beat/2,.5,.6)
        for q in range(4): add(hat(),tt+q*beat/4,.35+.3*(q%2),.45 if q%2==0 else .8)
        if k==3: add(hat(True),tt+beat*.5,.6,.8)
        add(stab([c+12 for c in ch],.2),tt+beat*.75,.3+.4*(k%2),.9)
t=np.arange(int(1.2*sr))/sr; sw=noise(1.2,300,6000)*np.linspace(0,1,len(t))**2.5*.35; add(sw,DROP-1.2)
x=np.stack([L,R],1); d=int(DROP*sr); b,a=ss.butter(2,1600/(sr/2)); x[:d]=ss.lfilter(b,a,x[:d],axis=0)
irt=np.arange(int(.9*sr))/sr
for c in (0,1):
    ir=rng.standard_normal(len(irt))*np.exp(-irt*5); ir[0]=0; wet=ss.fftconvolve(x[:,c],ir)[:n]; wet/=np.abs(wet).max()+1e-9
    x[:,c]=x[:,c]/np.abs(x[:,c]).max()+.08*wet
x=np.tanh(x*1.4); fd=np.ones(n); fi=int(.2*sr); fo=int(1.8*sr); fd[:fi]=np.linspace(0,1,fi); fd[-fo:]=np.linspace(1,0,fo)**1.5
x*=fd[:,None]; x=x/np.abs(x).max()*.62; wf.write(OUT,sr,(x*32767).astype(np.int16))
