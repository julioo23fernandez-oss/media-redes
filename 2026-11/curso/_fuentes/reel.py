import numpy as np, subprocess, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D='/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/curso/'
A='/mnt/user-data/attachments/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/'
DS='/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/ds/'
FP='/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf'
def f(px,w='Medium'): return ImageFont.truetype(FP%w,px)
RED=(210,18,43); CREAM=(236,232,226); INK=(31,31,31); GREY=(105,102,98); W=(255,255,255)
Wd,Hd,FPS=1080,1920,30
logo=Image.open(A+'ec1b456c-100dental-logo.png').convert('RGBA')
dsl=Image.open(DS+'im-003_a.png').convert('RGBA')
def fitw(im,w): return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def eio(x): x=min(max(x,0),1); return x*x*(3-2*x)

def read_clip(name,start,dur):
    cmd=['ffmpeg','-loglevel','error','-ss',str(start),'-i',D+'px/'+name+'.mp4','-t',str(dur+0.1),'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-']
    raw=subprocess.run(cmd,capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,Hd,Wd,3); return a
def photo_916(path,cx,zoom=1.0):
    im=Image.open(path).convert('RGB'); h=im.height; w=int(h*9/16)
    x0=int(min(max(cx-w/2,0),im.width-w)); return im.crop((x0,0,x0+w,h)).resize((Wd,Hd),Image.LANCZOS)
def zoomimg(im,z,ay=0.5,ax=0.5):
    if abs(z-1)<1e-4: return im
    cx,cy=Wd*ax,Hd*ay; a=1/z
    return im.transform((Wd,Hd),Image.AFFINE,(a,0,cx-cx*a,0,a,cy-cy*a),resample=Image.BICUBIC)

def label(c,t,y,txt,sub=None,t0=0.25):
    # etiqueta pequeña arriba: pastilla roja + subtítulo en pastilla crema
    k=ease((t-t0)/0.45)
    if k<=0: return
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L); al=int(255*k); dy=int(18*(1-k))
    fo=f(38,'Bold'); w=d.textlength(txt,font=fo)+56
    d.rounded_rectangle([70,y+dy,70+w,y+dy+72],radius=36,fill=RED+(al,)); d.text((70+w/2,y+dy+36),txt,font=fo,fill=W+(al,),anchor='mm')
    if sub:
        fo2=f(28,'Medium'); w2=d.textlength(sub,font=fo2)+44
        d.rounded_rectangle([70,y+dy+86,70+w2,y+dy+140],radius=27,fill=CREAM+(int(235*k),)); d.text((70+w2/2,y+dy+113),sub,font=fo2,fill=INK+(al,),anchor='mm')
    c.alpha_composite(L)

def logos_chip(c,y=150,al=255):
    l=fitw(logo,250); ds=fitw(dsl,190)
    w=l.width+ds.width+90; h=max(l.height,ds.height)+36
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L)
    x0=(Wd-w)//2; d.rounded_rectangle([x0,y,x0+w,y+h],radius=h//2,fill=W+(al,))
    l2=l.copy(); l2.putalpha(l2.split()[-1].point(lambda v:int(v*al/255)))
    ds2=ds.copy(); ds2.putalpha(ds2.split()[-1].point(lambda v:int(v*al/255)))
    L.alpha_composite(l2,(x0+30,y+(h-l.height)//2)); L.alpha_composite(ds2,(x0+30+l.width+30,y+(h-ds.height)//2))
    c.alpha_composite(L)

def cover(c,t):
    logos_chip(c,140)
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L)
    k=ease((t-0.15)/0.5); al=int(255*k); dy=int(24*(1-k))
    fo=f(30,'Bold'); s='CURSO · 20 NOV · GRANADA'; w=d.textlength(s,font=fo)+52
    d.rounded_rectangle([70,330+dy,70+w,394+dy],radius=32,fill=W+(al,)); d.text((70+w/2,362+dy),s,font=fo,fill=RED+(al,),anchor='mm')
    fo=f(104,'Bold')
    for i,line in enumerate(('Endodoncia','2026')):
        tw=d.textlength(line,font=fo); y=420+i*132+dy
        d.rectangle([70,y,70+tw+56,y+126],fill=RED+(al,)); d.text((98,y+63),line,font=fo,fill=W+(al,),anchor='lm')
    fo=f(32,'Medium'); s='Tendencias, tecnología y evidencia científica'; w=d.textlength(s,font=fo)+48
    d.rounded_rectangle([70,700+dy,70+w,760+dy],radius=30,fill=CREAM+(int(240*k),)); d.text((70+w/2,730+dy),s,font=fo,fill=INK+(al,),anchor='mm')
    c.alpha_composite(L)

def closing(t,dur):
    c=Image.new('RGBA',(Wd,Hd),CREAM+(255,)); d=ImageDraw.Draw(c)
    def a(dl): return ease((t-dl)/0.5)
    l=fitw(logo,420); c.alpha_composite(l,((Wd-l.width)//2,430))
    d.text((540,600),'×',font=f(54,'Medium'),fill=GREY,anchor='mm')
    ds=fitw(dsl,330); c.alpha_composite(ds,((Wd-ds.width)//2,660))
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); dd=ImageDraw.Draw(L)
    k=a(0.2); dd.text((540,1000+int(20*(1-k))),'Gracias a todos los que vinisteis',font=f(46,'Bold'),fill=INK+(int(255*k),),anchor='mm')
    k=a(0.6); dd.text((540,1075+int(20*(1-k))),'y a Dentsply Sirona por hacerlo posible.',font=f(34,'Medium'),fill=GREY+(int(255*k),),anchor='mm')
    k=a(1.1); dd.text((540,1220+int(20*(1-k))),'¿Te avisamos del próximo curso?',font=f(38,'Medium'),fill=INK+(int(255*k),),anchor='mm')
    k=a(1.5); fo=f(46,'Bold'); s='Escríbenos CURSO'; w=dd.textlength(s,font=fo)+90
    dd.rounded_rectangle([540-w/2,1290,540+w/2,1390],radius=50,fill=RED+(int(255*k),)); dd.text((540,1340),s,font=fo,fill=W+(int(255*k),),anchor='mm')
    c.alpha_composite(L); return c

# ---- guion ----
SEG=[ # (tipo, fuente, inicio, dur, zoom0, zoom1, ancla_y, ancla_x, texto)
 ('v','IMG_3443',1.0,3.0,1.22,1.26,0.80,0.62,'cover'),
 ('v','IMG_3436_60',0.3,2.4,1.14,1.14,0.78,0.5,('20 de noviembre','Hotel Macià Real de La Alhambra')),
 ('v','IMG_3437_60',0.4,2.4,1.05,1.05,0.6,0.5,('Café de bienvenida',None)),
 ('v','IMG_3438',0.4,3.0,1.18,1.22,0.80,0.5,('Sala llena',None)),
 ('p',A+'80177d22-image.jpg',None,3.0,1.0,1.035,0.5,0.5,('Dr. Juan Miraglia','Endodoncia microscópica y microcirugía apical')),
 ('v','IMG_3444',0.8,3.0,1.25,1.29,0.80,0.6,('Mínima invasión','Motores, limas y selladores biocerámicos')),
 ('v','IMG_3442',0.4,3.0,1.30,1.34,0.96,0.45,('Taller práctico','Con la última tecnología de Dentsply Sirona')),
 ('c',A+'009644e6-image.jpg',None,2.7,1,1,0.5,0.5,('RECIPROC® Mínima','y ProRoot® BioSealer')),
 ('end',None,None,3.9,1,1,0.5,0.5,None),
]
XF=10  # frames de fundido
PH={}
def seg_frames(s):
    typ,src,st,dur,z0,z1,ay,ax,txt=s; N=int(round(dur*FPS)); out=[]
    if typ=='v': clip=read_clip(src,st,dur/2 if src.endswith('_60') else dur)
    if typ=='p': base=photo_916(src,900)
    if typ=='c':
        ph=Image.open(src).convert('RGB'); ph.thumbnail((860,1150),Image.LANCZOS)
        mk=Image.new('L',ph.size,0); ImageDraw.Draw(mk).rounded_rectangle([0,0,ph.width-1,ph.height-1],radius=28,fill=255)
        cardbg=Image.new('RGBA',(Wd,Hd),CREAM+(255,)); sh=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); px=(Wd-ph.width)//2; py=450
        ImageDraw.Draw(sh).rounded_rectangle([px+6,py+16,px+ph.width+6,py+ph.height+16],radius=28,fill=(0,0,0,70)); sh=sh.filter(ImageFilter.GaussianBlur(16))
        cardbg.alpha_composite(sh); cardbg.paste(ph,(px,py),mk)
    for i in range(N):
        t=i/FPS; z=z0+(z1-z0)*eio(t/dur)
        if typ=='v': im=Image.fromarray(clip[min(i,len(clip)-1)]); im=zoomimg(im,z,ay,ax).convert('RGBA')
        elif typ=='p': im=zoomimg(base,z,ay,ax).convert('RGBA')
        elif typ=='c': im=cardbg.copy()
        else: im=closing(t,dur)
        if txt=='cover': cover(im,t)
        elif txt: label(im,t,250 if typ!='c' else 250,txt[0],txt[1])
        out.append(im.convert('RGB'))
    return out

if __name__=='__main__':
    mode=sys.argv[1]; mkdir=__import__('os').makedirs(D+'st',exist_ok=True)
    if mode!='stills':
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p',D+'raw.mp4'],stdin=subprocess.PIPE)
    cnt=[0]
    def emit(im):
        if mode=='stills':
            if cnt[0]%15==0: im.resize((270,480)).save(D+'st/s_%03d.jpg'%cnt[0])
        else: p.stdin.write(im.tobytes())
        cnt[0]+=1
    tail=[]; xf_prev=0
    for idx,s_ in enumerate(SEG):
        fr=seg_frames(s_)
        nxt=SEG[idx+1][0] if idx+1<len(SEG) else None
        xf_next=9 if nxt in ('c','end') else 0
        if xf_prev:
            for k in range(xf_prev):
                a=(k+1)/(xf_prev+1); emit(Image.blend(tail[k],fr[k],eio(a)))
            body=fr[xf_prev:]
        else:
            for im in tail: emit(im)
            body=fr
        if xf_next:
            for im in body[:-xf_next]: emit(im)
            tail=body[-xf_next:]
        else:
            tail=body
        xf_prev=xf_next
        del fr; print(s_[1],cnt[0],flush=True)
    for im in tail: emit(im)
    print('total s',cnt[0]/FPS)
    if mode!='stills': p.stdin.close(); p.wait()
