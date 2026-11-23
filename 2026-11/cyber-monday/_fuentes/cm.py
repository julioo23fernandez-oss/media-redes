from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math, os
A='/mnt/user-data/attachments/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/'
K='/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/kit/'
OUT='/home/claude/out/noviembre/'
FP='/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf'
def f(px,w='Medium'): return ImageFont.truetype(FP%w,px)
RED=(210,18,43); DRED=(150,8,26); CREAM=(236,232,226); INK=(31,31,31); GREY=(105,102,98); W=(255,255,255); LINE=(214,207,198)

def prep(path,th=246,pad=40):
    im=Image.open(path).convert('RGB'); a=np.asarray(im)
    m=(a<th).any(2); ys,xs=np.where(m)
    im=im.crop((max(xs.min()-pad,0),max(ys.min()-pad,0),min(xs.max()+pad,im.width),min(ys.max()+pad,im.height)))
    a=np.asarray(im).astype(float)*np.array(CREAM)/255.
    im=Image.fromarray(a.clip(0,255).astype('uint8'))
    w,h=im.size; mg=pad; mk=Image.new('L',(w,h),0); ImageDraw.Draw(mk).rectangle([mg,mg,w-mg,h-mg],fill=255); mk=mk.filter(ImageFilter.GaussianBlur(mg/2))
    bg=Image.new('RGB',(w,h),CREAM); bg.paste(im,(0,0),mk); return bg
SYS=prep(A+'fc30434f-image.jpg')
CA=prep(A+'a1303a11-64_Retusche.tif')
whl=Image.open(K+'wh_logo.png').convert('RGBA'); whl=whl.crop(whl.getbbox())
logo=Image.open(A+'ec1b456c-100dental-logo.png').convert('RGBA')
def fitw(im,w): return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
def fit(im,mw,mh):
    s=min(mw/im.width,mh/im.height); return im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)

def pill(d,x,y,t,fo,bg,fg,h=56,pad=26,outline=None,anchor='l'):
    w=d.textlength(t,font=fo)+2*pad
    if anchor=='c': x=x-w/2
    d.rounded_rectangle([x,y,x+w,y+h],radius=h//2,fill=bg,outline=outline,width=2 if outline else 0); d.text((x+w/2,y+h/2),t,font=fo,fill=fg,anchor='mm'); return x+w
def burst(size,n=18,r1=1.0,r2=0.86):
    im=Image.new('RGBA',(size,size),(0,0,0,0)); d=ImageDraw.Draw(im); c=size/2; R=size/2-2; pts=[]
    for k in range(n*2):
        a=math.pi*k/n; r=R*(r1 if k%2==0 else r2); pts.append((c+r*math.cos(a),c+r*math.sin(a)))
    d.polygon(pts,fill=W); return im
def band(c,y,items=('CYBER MONDAY','•','OFERTAS W&H','•'),rot=-3,x0=-200):
    b=Image.new('RGBA',(1500,74),W+(255,)); bd=ImageDraw.Draw(b); x=10
    while x<1500:
        for t in items: bd.text((x,37),t,font=f(32,'Bold'),fill=RED,anchor='lm'); x+=bd.textlength(t,font=f(32,'Bold'))+26
    b=b.rotate(rot,resample=Image.BICUBIC,expand=True); c.paste(b,(x0,y),b)
def strike(d,xy,t,fo,fill,lw=4):
    d.text(xy,t,font=fo,fill=fill,anchor='lm'); w=d.textlength(t,font=fo); x,y=xy
    d.line([x-4,y+4,x+w+4,y-2],fill=fill,width=lw); return w
def header(c,d,sub,top=250):
    # cabecera roja corta para las slides interiores
    d.polygon([(0,0),(1080,0),(1080,top+40),(0,top)],fill=RED)
    wl=fitw(whl,150); c.paste(wl,(70,58),wl)
    d.text((1010,95),'CYBER MONDAY',font=f(34,'Bold'),fill=W,anchor='rm')
    d.text((70,150),sub,font=f(64,'Bold'),fill=W)
def footer(c,d,y=1240,cta=True,num=None):
    l=fitw(logo,200); c.paste(l,(70,y+12),l)
    if num: d.text((1010,y+45),num,font=f(26,'Medium'),fill=GREY,anchor='rm')
def pricebox(d,x,y,w,label,price,old,h=250):
    d.rounded_rectangle([x,y,x+w,y+h],radius=28,fill=W)
    d.text((x+30,y+38),label,font=f(28,'Bold'),fill=INK,anchor='lm')
    d.text((x+28,y+125),price,font=f(84,'Bold'),fill=RED,anchor='lm')
    d.text((x+30,y+200),'+ IVA',font=f(26,'Medium'),fill=GREY,anchor='lm')
    pw=d.textlength('+ IVA',font=f(26,'Medium'))
    strike(d,(x+30+pw+30,y+200),'antes '+old,f(26,'Medium'),GREY,3)
def chips(d,x,y,items,maxw=940,fo=None):
    fo=fo or f(26,'Medium'); cx,cy=x,y
    for t in items:
        w=d.textlength(t,font=fo)+52
        if cx+w>x+maxw: cx=x; cy+=66
        pill(d,cx,cy,t,fo,CREAM,INK,52,26,outline=INK); cx+=w+12
    return cy+52

def s1(H=1350,story=False):
    c=Image.new('RGB',(1080,H),CREAM); d=ImageDraw.Draw(c)
    oy=0 if not story else 170; top=oy+520
    d.polygon([(0,0),(1080,0),(1080,top+57),(0,top)],fill=RED)
    wl=fitw(whl,190); c.paste(wl,(70,oy+60),wl)
    d.text((64,oy+122),'CYBER',font=f(138,'Bold'),fill=W)
    d.text((64,oy+250),'MONDAY',font=f(138,'Bold'),fill=W)
    b=burst(270); bd=ImageDraw.Draw(b)
    bd.text((135,104),'HASTA',font=f(40,'Bold'),fill=RED,anchor='mm'); bd.text((135,156),'EL 4/12',font=f(50,'Bold'),fill=RED,anchor='mm')
    b=b.rotate(12,resample=Image.BICUBIC,expand=True); c.paste(b,(1080-b.width-6,oy+40),b)
    d.text((70,oy+432),'Ofertas W&H en cirugía e implantología',font=f(40,'Bold'),fill=W)
    band(c,top-46)
    g0=top+100
    if not story:
        p=fit(SYS,1000,470); c.paste(p,((1080-p.width)//2,g0+10))
        d.text((540,g0+p.height+40),'Implantmed Plus II + módulo Piezomed Plus II',font=f(28,'Medium'),fill=INK,anchor='mm')
        fy=1180
        x=pill(d,70,fy,'Desliza y mira los precios',f(30,'Bold'),RED,W,66,32)
        l=fitw(logo,220); c.paste(l,(1010-l.width,fy+2),l)
    else:
        p=fit(SYS,1000,520); c.paste(p,((1080-p.width)//2,g0+10))
        y=g0+p.height+40
        d.text((540,y),'Implantmed Plus II + módulo Piezomed Plus II',font=f(30,'Medium'),fill=INK,anchor='mm')
        d.text((540,y+110),'Desde 159 €/mes',font=f(84,'Bold'),fill=RED,anchor='mm')
        d.text((540,y+180),'Renting Implantmed Plus II Scan Edition · + IVA',font=f(28,'Medium'),fill=GREY,anchor='mm')
        pill(d,540,y+260,'¡¡OFERTA EN EL FEED!!',f(46,'Bold'),RED,W,96,50,anchor='c')
        l=fitw(logo,260); c.paste(l,((1080-l.width)//2,y+420),l)
    return c

def s2():
    c=Image.new('RGB',(1080,1350),CREAM); d=ImageDraw.Draw(c); header(c,d,'Implantmed Plus II')
    d.text((70,340),'Motor de implantología con micromotor con luz',font=f(32,'Medium'),fill=INK)
    p=fit(CA,300,560); c.paste(p,(1000-p.width,380))
    d.text((1000-p.width//2,380+p.height+18),'Contraángulo WS-75 L',font=f(22,'Medium'),fill=GREY,anchor='mt')
    pricebox(d,70,420,610,'Con pedal con cable','4.395 €','4.688 €')
    pricebox(d,70,700,610,'Con pedal inalámbrico','4.396 €','4.698 €')
    chips(d,70,1000,['Micromotor con luz','Contraángulo WS-75 L','3 años de garantía*'],maxw=940)
    d.text((70,1150),'*Consulta condiciones con tu comercial.',font=f(22,'Medium'),fill=GREY)
    footer(c,d,1220,num='2/5'); return c

def s3():
    c=Image.new('RGB',(1080,1350),CREAM); d=ImageDraw.Draw(c); header(c,d,'Módulo Piezomed Plus II')
    d.text((70,340),'Cirugía piezoeléctrica, acoplada al Implantmed Plus II',font=f(32,'Medium'),fill=INK)
    p=fit(SYS,940,360); c.paste(p,((1080-p.width)//2,400))
    y=400+p.height+20
    pricebox(d,70,y,940,'Módulo Piezomed Plus II','3.800 €','4.225 €',h=250)
    chips(d,70,y+290,['Se engancha sin cables ni fuente extra','Anillo LED+','24 W','Reconoce el inserto'])
    footer(c,d,1220,num='3/5'); return c

def s4():
    c=Image.new('RGB',(1080,1350),RED); d=ImageDraw.Draw(c)
    wl=fitw(whl,150); c.paste(wl,(70,58),wl); d.text((1010,95),'CYBER MONDAY',font=f(34,'Bold'),fill=W,anchor='rm')
    d.text((70,190),'Implantmed Plus II',font=f(64,'Bold'),fill=W)
    d.text((70,275),'SCAN EDITION · en renting',font=f(40,'Medium'),fill=W)
    d.text((540,560),'159 €',font=f(250,'Bold'),fill=W,anchor='mm')
    d.text((540,730),'/mes + IVA',font=f(60,'Bold'),fill=W,anchor='mm')
    fo=f(32,'Medium'); t='PVP 7.518 €'; tw=d.textlength(t,font=fo)
    d.text((540,820),t,font=fo,fill=(255,205,212),anchor='mm'); d.line([540-tw/2-6,826,540+tw/2+6,814],fill=W,width=4)
    y=900; cx=70
    for t in ['Pedal inalámbrico','Función de escaneo','Micromotor con luz','Contraángulo WS-75 L']:
        fo=f(28,'Medium'); w=d.textlength(t,font=fo)+56
        if cx+w>1010: cx=70; y+=72
        d.rounded_rectangle([cx,y,cx+w,y+56],radius=28,outline=W,width=2); d.text((cx+w/2,y+28),t,font=fo,fill=W,anchor='mm'); cx+=w+12
    d.text((70,y+100),'Condiciones del renting según estudio. Te las explica tu comercial.',font=f(24,'Medium'),fill=(255,215,220))
    L=Image.new('RGBA',logo.size,(0,0,0,0))
    l=fitw(logo,200); ch=Image.new('RGBA',(l.width+60,l.height+36),(0,0,0,0)); ImageDraw.Draw(ch).rounded_rectangle([0,0,ch.width-1,ch.height-1],radius=ch.height//2,fill=CREAM+(255,)); ch.alpha_composite(l,(30,18))
    c.paste(ch,(70,1222),ch); d.text((1010,1265),'4/5',font=f(26,'Medium'),fill=(255,205,212),anchor='rm')
    return c

def s5():
    c=Image.new('RGB',(1080,1350),CREAM); d=ImageDraw.Draw(c); header(c,d,'¿Lo hablamos?')
    d.text((70,330),'Las ofertas Cyber Monday de W&H',font=f(40,'Bold'),fill=INK)
    d.text((70,385),'son válidas hasta el 4 de diciembre.',font=f(40,'Bold'),fill=INK)
    rows=[('Implantmed Plus II','desde 4.395 € + IVA'),('Módulo Piezomed Plus II','3.800 € + IVA'),('Implantmed Plus II Scan Edition','159 €/mes + IVA')]
    y=490
    for a,b in rows:
        d.text((70,y),a,font=f(32,'Medium'),fill=INK,anchor='lm'); d.text((1010,y),b,font=f(32,'Bold'),fill=RED,anchor='rm')
        d.line([70,y+45,1010,y+45],fill=LINE,width=2); y+=95
    d.text((70,y+20),'Somos distribuidor oficial de W&H.',font=f(30,'Medium'),fill=INK)
    d.text((70,y+65),'Tu comercial te prepara la oferta y nuestro',font=f(30,'Medium'),fill=INK)
    d.text((70,y+110),'servicio técnico se encarga de la instalación.',font=f(30,'Medium'),fill=INK)
    fy=y+200
    pill(d,70,fy,'Escríbenos IMPLANT por mensaje',f(38,'Bold'),RED,W,84,40)
    x=pill(d,70,fy+110,'Hasta el 4/12',f(26,'Medium'),CREAM,INK,56,24,outline=INK)
    pill(d,x+12,fy+110,'Solo profesionales',f(26,'Medium'),CREAM,INK,56,24,outline=INK)
    footer(c,d,1220,num='5/5'); return c

os.makedirs(OUT,exist_ok=True)
for i,fn in enumerate((s1,s2,s3,s4,s5),1):
    fn().save(OUT+'2026-11-30-cyber-monday-wh-%d.png'%i)
s1(1920,True).save(OUT+'2026-11-30-historia-cyber-monday-wh.png')
