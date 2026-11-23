import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, sys
# Música informativa: tranquila con pulso (100 bpm), piano + pad + percusión suave
sr=44100; D=float(sys.argv[1]); OUT=sys.argv[2]; SEED=int(sys.argv[3]) if len(sys.argv)>3 else 7
BPM=100; n=int(sr*D); beat=60/BPM; rng=np.random.default_rng(SEED)
L=np.zeros(n); R=np.zeros(n)
def f(m): return 440*2**((m-69)/12)
def add(w,s,pan=.5,g=1.):
    a=int(s*sr)
    if a<0 or a>=n: return
    b=min(n,a+len(w)); w=w[:b-a]*g; L[a:b]+=w*(1-pan); R[a:b]+=w*pan
def piano(m,d=1.6,v=1.):
    t=np.arange(int(d*sr))/sr; fr=f(m)
    w=sum(np.sin(2*np.pi*fr*k*t*(1+0.0004*k*k))*np.exp(-t*(2.2+1.6*k))/k**1.1 for k in range(1,7))
    return w*np.minimum(1,t/.003)*.11*v
def pad(ch,d):
    t=np.arange(int(d*sr))/sr; w=sum(np.sin(2*np.pi*f(m)*2**(dt/1200)*t+rng.uniform(0,6)) for m in ch for dt in (-7,7))
    b,a=ss.butter(2,1800/(sr/2)); w=ss.lfilter(b,a,w)
    return w*np.minimum(1,t/.6)*np.minimum(1,(d-t)/.5)*.022
def kick():
    t=np.arange(int(.35*sr))/sr; fr=42+60*np.exp(-t*28); return np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-t*7)*.75
def rim():
    t=np.arange(int(.12*sr))/sr; x=rng.standard_normal(len(t)); b,a=ss.butter(2,[1800/(sr/2),5000/(sr/2)],'band')
    return (ss.lfilter(b,a,x)*.5+np.sin(2*np.pi*820*t)*.4)*np.exp(-t*45)*.22
def shaker():
    t=np.arange(int(.08*sr))/sr; x=rng.standard_normal(len(t)); b,a=ss.butter(2,6000/(sr/2),'high')
    return ss.lfilter(b,a,x)*np.sin(np.pi*t/t[-1])*.05
def bass(m,d):
    t=np.arange(int(d*sr))/sr; w=np.sin(2*np.pi*f(m)*t)+.3*np.sin(4*np.pi*f(m)*t)
    return w*np.minimum(1,t/.01)*np.exp(-t*2.5)*.22
# D - Bm - G - A
prog=[(50,[62,66,69,74]),(47,[62,66,71,74]),(43,[62,67,71,74]),(45,[61,64,69,73])]
arp=[0,2,1,3,2,1,3,2]; bar=4*beat
for i in range(int(D/bar)+2):
    t0=i*bar; r,ch=prog[i%4]; add(pad([c-12 for c in ch],bar+.6),t0,.5,1)
    add(bass(r-12,bar*.9),t0); add(bass(r-12,beat*1.5),t0+2.5*beat,.5,.5)
    for q in range(8):
        add(piano(ch[arp[q]]+(12 if q==4 else 0),1.4,.85 if q%2 else 1),t0+q*beat/2,.3+.4*(q%2))
    if i>=1:
        for k in range(4):
            if k in (0,2): add(kick(),t0+k*beat,.5,.8 if k==0 else .55)
            if k in (1,3): add(rim(),t0+k*beat,.45)
            for q in (0,1): add(shaker(),t0+k*beat+q*beat/2,.6,.7 if q else 1)
x=np.stack([L,R],1)
irt=np.arange(int(1.4*sr))/sr
for c in (0,1):
    ir=rng.standard_normal(len(irt))*np.exp(-irt*3.5); ir[0]=0; wet=ss.fftconvolve(x[:,c],ir)[:n]; wet/=np.abs(wet).max()+1e-9
    x[:,c]=x[:,c]/np.abs(x[:,c]).max()+.12*wet
x=np.tanh(x*1.2); fd=np.ones(n); fi=int(.4*sr); fo=int(2.2*sr); fd[:fi]=np.linspace(0,1,fi); fd[-fo:]=np.linspace(1,0,fo)**1.5
x*=fd[:,None]; x=x/np.abs(x).max()*.6; wf.write(OUT,sr,(x*32767).astype(np.int16))
