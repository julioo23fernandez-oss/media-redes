import numpy as np, scipy.signal as ss, scipy.io.wavfile as wf, sys
# Música alegre / celebración: 100 bpm (cuadra con los cortes del reel), mayor, palmas, pluck y campanitas
sr=44100; D=float(sys.argv[1]); OUT=sys.argv[2]; SEED=int(sys.argv[3]) if len(sys.argv)>3 else 5
BPM=100; n=int(sr*D); beat=60/BPM; rng=np.random.default_rng(SEED)
L=np.zeros(n); R=np.zeros(n)
def f(m): return 440*2**((m-69)/12)
def add(w,s,pan=.5,g=1.):
    a=int(s*sr)
    if a<0 or a>=n: return
    b=min(n,a+len(w)); w=w[:b-a]*g; L[a:b]+=w*(1-pan); R[a:b]+=w*pan
def noise(d,lo,hi):
    x=rng.standard_normal(int(d*sr)); b,a=ss.butter(2,[lo/(sr/2),hi/(sr/2)],'band'); return ss.lfilter(b,a,x)
def kick():
    t=np.arange(int(.3*sr))/sr; fr=48+80*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-t*8)*.9
def clap():
    t=np.arange(int(.25*sr))/sr; e=np.exp(-t*22)
    for dd in (.008,.017): e+=np.roll(np.exp(-t*80),int(dd*sr))*.6
    return noise(.25,900,7000)*e*.35
def shaker(g=1):
    t=np.arange(int(.07*sr))/sr; x=rng.standard_normal(len(t)); b,a=ss.butter(2,6500/(sr/2),'high')
    return ss.lfilter(b,a,x)*np.sin(np.pi*t/t[-1])*.07*g
def pluck(m,d=.5,v=1.):
    t=np.arange(int(d*sr))/sr; fr=f(m); w=(np.sin(2*np.pi*fr*t)+.5*np.sin(4*np.pi*fr*t)+.25*np.sin(6*np.pi*fr*t))
    return w*np.minimum(1,t/.002)*np.exp(-t*7)*.10*v
def bell(m,d=1.2):
    t=np.arange(int(d*sr))/sr; fr=f(m); w=np.sin(2*np.pi*fr*t)+.4*np.sin(2*np.pi*fr*2.76*t)*np.exp(-t*6)
    return w*np.exp(-t*3.5)*.06
def bass(m,d):
    t=np.arange(int(d*sr))/sr; w=np.sin(2*np.pi*f(m)*t)+.35*np.sin(4*np.pi*f(m)*t)
    return w*np.minimum(1,t/.008)*np.exp(-t*4)*.28
def pad(ch,d):
    t=np.arange(int(d*sr))/sr; w=sum(np.sin(2*np.pi*f(m)*2**(dt/1200)*t+rng.uniform(0,6)) for m in ch for dt in (-8,8))
    b,a=ss.butter(2,2200/(sr/2)); w=ss.lfilter(b,a,w); return w*np.minimum(1,t/.4)*np.minimum(1,(d-t)/.3)*.018
# C - G - Am - F  (alegre)
prog=[(48,[60,64,67,72]),(43,[59,62,67,71]),(45,[60,64,69,72]),(41,[60,65,69,72])]
mel=[[72,74,76,79,76,74,72,74],[71,74,79,74,71,67,71,74],[72,76,81,79,76,74,72,76],[72,77,81,77,76,74,72,71]]
bar=4*beat
for i in range(int(D/bar)+2):
    t0=i*bar; r,ch=prog[i%4]; add(pad(ch,bar+.4),t0)
    intro=i==0
    for k in range(4):
        tt=t0+k*beat
        if not intro:
            add(kick(),tt,.5,.9 if k in (0,2) else .55)
            if k in (1,3): add(clap(),tt,.5)
            add(bass(r-12,beat*.45),tt); add(bass(r,beat*.3),tt+beat*.5,.5,.55)
            for q in range(4): add(shaker(1 if q%2 else .6),tt+q*beat/4,.35+.3*(q%2))
    for q in range(8):
        add(pluck(mel[i%4][q],.45,1 if q%2==0 else .8),t0+q*beat/2,.3+.4*(q%2),.75 if intro else 1)
    if i%2==1: add(bell(84 if i%4==1 else 88),t0+3.5*beat,.7)
x=np.stack([L,R],1)
irt=np.arange(int(1.0*sr))/sr
for c in (0,1):
    ir=rng.standard_normal(len(irt))*np.exp(-irt*4.5); ir[0]=0; wet=ss.fftconvolve(x[:,c],ir)[:n]; wet/=np.abs(wet).max()+1e-9
    x[:,c]=x[:,c]/np.abs(x[:,c]).max()+.09*wet
x=np.tanh(x*1.3); fd=np.ones(n); fi=int(.15*sr); fo=int(2.0*sr); fd[:fi]=np.linspace(0,1,fi); fd[-fo:]=np.linspace(1,0,fo)**1.5
x*=fd[:,None]; x=x/np.abs(x).max()*.62; wf.write(OUT,sr,(x*32767).astype(np.int16))
