import sys
_src=open('/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/curso/reel.py').read().split('def label(')[0]
exec(_src)
import subprocess

def fade(t,dur,a_in=0.4,lead=0.25,out=0.3):
    k=ease((t-lead)/a_in)
    if t>dur-out: k*=max(0,(dur-t)/out)
    return k
def shadowed(L,draw_fn):
    # sombra suave (no degradado): misma forma, desenfocada
    sh=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); draw_fn(ImageDraw.Draw(sh),(0,0,0),0.45)
    sh=sh.filter(ImageFilter.GaussianBlur(9)); L.alpha_composite(sh); draw_fn(ImageDraw.Draw(L),W,1.0)

def lower(c,t,dur,kicker,title,sub=None,y=1330,big=60):
    k=fade(t,dur)
    if k<=0: return
    dy=int(14*(1-ease((t-0.25)/0.4)))
    def fn(d,col,m):
        al=int(255*k*m)
        if kicker: d.text((72,y-big-26+dy),kicker,font=f(26,'Medium'),fill=col+(al,),anchor='ls')
        d.text((68,y+dy),title,font=f(big,'Bold'),fill=col+(al,),anchor='ls')
        if sub: d.text((72,y+52+dy),sub,font=f(30,'Regular'),fill=col+(al,),anchor='ls')
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); shadowed(L,fn)
    k2=k; L2=ImageDraw.Draw(L); L2.rectangle([72,y-big-70+dy,72+44,y-big-66+dy],fill=RED+(int(255*k2),))
    c.alpha_composite(L)

def logo_chip(c,t,dur):
    k=fade(t,dur,0.4,0.1,0.3)
    if k<=0: return
    l=fitw(logo,170); ds=fitw(dsl,112); h=max(l.height,ds.height)+24; w=l.width+ds.width+20+44
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L)
    x0,y0=70,150; d.rounded_rectangle([x0,y0,x0+w,y0+h],radius=h//2,fill=W+(int(235*k),))
    for im,x in ((l,x0+22),(ds,x0+22+l.width+20)):
        im2=im.copy(); im2.putalpha(im2.split()[-1].point(lambda v:int(v*k))); L.alpha_composite(im2,(x,y0+(h-im.height)//2))
    c.alpha_composite(L)

def top_title(c,t,dur):
    k=fade(t,dur,0.5,0.2,0.3)
    if k<=0: return
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L); al=int(255*k); dy=int(14*(1-ease((t-0.2)/0.5)))
    d.rectangle([72,290+dy,116,294+dy],fill=RED+(al,))
    d.text((72,346+dy),'CURSO · 20.11.2026 · GRANADA',font=f(26,'Medium'),fill=RED+(al,),anchor='ls')
    d.text((66,436+dy),'Endodoncia 2026',font=f(88,'Bold'),fill=INK+(al,),anchor='ls')
    d.text((72,490+dy),'Con el Dr. Juan Miraglia y Dentsply Sirona',font=f(32,'Regular'),fill=(60,58,55,al),anchor='ls')
    c.alpha_composite(L)

def closing3(t,dur):
    c=Image.new('RGBA',(Wd,Hd),CREAM+(255,))
    def a(dl): return ease((t-dl)/0.6)
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); dd=ImageDraw.Draw(L)
    l=fitw(logo,380); ds=fitw(dsl,330)
    dd.text((540,850),'en colaboración con',font=f(28,'Regular'),fill=(70,68,64,int(255*a(0.1))),anchor='ms')
    for im,x,y,dl in ((l,(Wd-l.width)//2,640,0.0),(ds,(Wd-ds.width)//2,890,0.15)):
        k=a(dl); im2=im.copy(); im2.putalpha(im2.split()[-1].point(lambda v:int(v*k))); L.alpha_composite(im2,(x,y))
    k=a(0.5); dd.rectangle([518,1110,562,1114],fill=RED+(int(255*k),))
    dd.text((540,1190),'Endodoncia 2026',font=f(50,'Bold'),fill=INK+(int(255*k),),anchor='ms')
    k=a(0.9); dd.text((540,1270),'Síguenos para no perderte más',font=f(40,'Bold'),fill=RED+(int(255*k),),anchor='ms')
    c.alpha_composite(L); return c


def read60(name,start,dur,speed):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-ss',str(start),'-i',D+'px/'+name+'.mp4','-t',str(dur*speed+0.2),'-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,Hd,Wd,3); N=int(round(dur*FPS))
    idx=[min(len(a)-1,int(round(i*2*speed))) for i in range(N)]; return a,idx
ph=Image.open(A+'6256e1da-image.jpg').convert('RGB')
def photo_card(t,dur):
    c=Image.new('RGBA',(Wd,Hd),CREAM+(255,))
    z=1.0+0.03*eio(t/dur); w=1080; h=int(ph.height*w/ph.width)
    p=ph.resize((int(w*z),int(h*z)),Image.LANCZOS).crop((int(w*(z-1)/2),int(h*(z-1)/2),int(w*(z-1)/2)+w,int(h*(z-1)/2)+h))
    x,y=(Wd-w)//2,(Hd-h)//2-40
    sh=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle([x+4,y+14,x+w+4,y+h+14],radius=0,fill=(0,0,0,40)); sh=sh.filter(ImageFilter.GaussianBlur(18)); c.alpha_composite(sh)
    mk=Image.new('L',(w,h),0); ImageDraw.Draw(mk).rectangle([0,0,w-1,h-1],fill=255); c.paste(p,(x,y),mk)
    k=fade(t,dur,0.5,0.3,0.0); d=ImageDraw.Draw(c); al=int(255*k)
    x=70; d.rectangle([x,y+h+70,x+44,y+h+74],fill=RED+(al,))
    d.text((x,y+h+130),'Más de 30 profesionales',font=f(44,'Bold'),fill=INK+(al,),anchor='ls') if False else d.text((x,y+h+130),'Gracias a todos',font=f(44,'Bold'),fill=INK+(al,),anchor='ls')
    d.text((x,y+h+180),'Hotel Macià Real de La Alhambra · 20 de noviembre',font=f(28,'Regular'),fill=(70,68,64,al),anchor='ls')
    return c


def botcap(c,t,dur,title,sub):
    k=fade(t,dur,0.4,0.25,0.3)
    if k<=0: return
    dy=int(12*(1-ease((t-0.25)/0.4)))
    def fn(d,col,m):
        al=int(255*k*m); d.text((70,1690+dy),title,font=f(54,'Bold'),fill=col+(al,),anchor='ls'); d.text((72,1742+dy),sub,font=f(30,'Regular'),fill=col+(al,),anchor='ls')
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); shadowed(L,fn); ImageDraw.Draw(L).rectangle([72,1622+dy,116,1626+dy],fill=RED+(int(255*k),)); c.alpha_composite(L)
def topcap(c,t,dur,title,sub):
    k=fade(t,dur,0.4,0.25,0.3)
    if k<=0: return
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L); al=int(255*k); dy=int(12*(1-ease((t-0.25)/0.4)))
    d.rectangle([72,250+dy,116,254+dy],fill=RED+(al,))
    d.text((70,318+dy),title,font=f(54,'Bold'),fill=INK+(al,),anchor='ls')
    d.text((72,370+dy),sub,font=f(30,'Regular'),fill=(50,48,45,al),anchor='ls')
    c.alpha_composite(L)
SEG6=[ # tipo, fuente, inicio, dur, z0, z1, extra
 ('v','c3439',0.0,3.0,1.0,1.045,'cover'),
 ('s','IMG_3436_60',0.3,2.4,1.02,1.02,0.5),
 ('s','c3437_60',0.6,2.4,1.0,1.0,1.0),
 ('v','c3443ds',0.0,3.2,1.0,1.03,('Dr. Juan Miraglia','RECIPROC® Mínima · Dentsply Sirona')),
 ('v','c3442',0.0,2.4,1.0,1.03,('B','Taller práctico','Con tecnología Dentsply Sirona')),
 ('p',None,None,3.6,1,1,None),
]
END=3.2; XF=14
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','15','-preset','medium','-pix_fmt','yuv420p',D+'raw6.mp4'],stdin=subprocess.PIPE)
mode=sys.argv[1] if len(sys.argv)>1 else 'render'
n=0; last=None
for k_,(typ,src,st,dur,z0,z1,ex) in enumerate(SEG6):
    N=int(round(dur*FPS))
    if typ=='v': clip=read_clip(src,st,dur); idx=list(range(N))
    if typ=='s': clip,idx=read60(src,st,dur,ex)
    for i in range(N):
        t=i/FPS
        if typ=='p': im=photo_card(t,dur)
        else:
            z=z0+(z1-z0)*eio(t/dur)
            im=zoomimg(Image.fromarray(clip[min(idx[i],len(clip)-1)]),z,0.6,0.5).convert('RGBA')
            if ex=='cover': logo_chip(im,t,dur); top_title(im,t,dur)
            elif isinstance(ex,tuple) and ex[0]=='B': botcap(im,t,dur,*ex[1:])
            elif isinstance(ex,tuple): topcap(im,t,dur,*ex)
        im=im.convert('RGB'); p.stdin.write(im.tobytes()); n+=1; last=im
        if mode=='stills' and i==int(N*0.6): im.save(D+'st6_%d.png'%k_)
    if typ in ('v','s'): del clip
NE=int(END*FPS)
for i in range(NE):
    im=closing3(i/FPS,END).convert('RGB')
    if i<XF: im=Image.blend(last,im,eio((i+1)/(XF+1)))
    p.stdin.write(im.tobytes()); n+=1
    if mode=='stills' and i==NE-5: im.save(D+'st6_9.png')
p.stdin.close(); p.wait(); print('frames',n,n/FPS)
