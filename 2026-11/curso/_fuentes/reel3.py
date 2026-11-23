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
    l=fitw(logo,360); ds=fitw(dsl,240)
    for im,x,y,dl in ((l,(Wd-l.width)//2,640,0.0),(ds,(Wd-ds.width)//2,820,0.15)):
        k=a(dl); im2=im.copy(); im2.putalpha(im2.split()[-1].point(lambda v:int(v*k))); L.alpha_composite(im2,(x,y))
    k=a(0.5); dd.rectangle([518,1040,562,1044],fill=RED+(int(255*k),))
    dd.text((540,1120),'Gracias por venir',font=f(50,'Bold'),fill=INK+(int(255*k),),anchor='ms')
    k=a(0.9); dd.text((540,1180),'¿Te avisamos del próximo curso?',font=f(32,'Regular'),fill=(70,68,64,int(255*k)),anchor='ms')
    k=a(1.2); dd.text((540,1250),'Escríbenos CURSO',font=f(38,'Bold'),fill=RED+(int(255*k),),anchor='ms')
    c.alpha_composite(L); return c

SEG3=[ # fuente, inicio, dur, z0, z1, ay, ax, texto
 ('IMG_3439',0.2,3.0,1.04,1.09,0.7,0.5,'cover'),
 ('IMG_3436_60',0.3,2.4,1.02,1.02,0.6,0.5,None),
 ('IMG_3437_60',0.4,2.4,1.02,1.02,0.6,0.5,None),
 ('IMG_3443',0.3,3.6,1.12,1.18,0.62,0.55,None),
 ('IMG_3444',0.5,3.0,1.04,1.08,0.7,0.55,None),
 ('IMG_3438',0.4,3.0,1.04,1.09,0.7,0.5,None),
]
END=3.0; XF=12
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','15','-preset','medium','-pix_fmt','yuv420p',D+'raw3.mp4'],stdin=subprocess.PIPE)
mode=sys.argv[1] if len(sys.argv)>1 else 'render'
n=0; last=None
for src,st,dur,z0,z1,ay,ax,txt in SEG3:
    clip=read_clip(src,st,dur/2 if src.endswith('_60') else dur); N=int(round(dur*FPS))
    for i in range(N):
        t=i/FPS; z=z0+(z1-z0)*eio(t/dur)
        im=zoomimg(Image.fromarray(clip[min(i,len(clip)-1)]),z,ay,ax).convert('RGBA')
        if txt=='cover':
            logo_chip(im,t,dur); top_title(im,t,dur)
        elif txt: lower(im,t,dur,*txt)
        im=im.convert('RGB'); p.stdin.write(im.tobytes()); n+=1; last=im
        if mode=='stills' and i==int(N*0.6): im.save(D+'st3_%02d.png'%SEG3.index((src,st,dur,z0,z1,ay,ax,txt)))
    del clip
NE=int(END*FPS)
for i in range(NE):
    im=closing3(i/FPS,END).convert('RGB')
    if i<XF: im=Image.blend(last,im,eio((i+1)/(XF+1)))
    p.stdin.write(im.tobytes()); n+=1
    if mode=='stills' and i==NE-5: im.save(D+'st3_99.png')
p.stdin.close(); p.wait(); print('frames',n,n/FPS)
