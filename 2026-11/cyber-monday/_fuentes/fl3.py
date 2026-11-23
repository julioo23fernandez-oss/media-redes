exec(open('fl2.py').read().split('def build(')[0])

SS=4
def aa(size,fn):
    m=Image.new('L',(size[0]*SS,size[1]*SS),0); fn(ImageDraw.Draw(m),SS); return m.resize(size,Image.LANCZOS)
def aafill(img,size_xy,fn,color):
    m=aa(img.size,fn); img.paste(color,(0,0),m) if img.mode=='RGB' else img.paste(color+(255,),(0,0),m); return m
def tag(name1,name2,feats,price,old,w=300,h=280,bg=W,ink=INK,acc=RED,sub=GREY):
    T=Image.new('RGBA',(w+40,h+40),(0,0,0,0)); d=ImageDraw.Draw(T); o=20
    pts=[(o+46,o),(o+w,o),(o+w,o+h),(o+46,o+h),(o,o+h-46),(o,o+46)]
    sh=Image.new('RGBA',T.size,(0,0,0,0)); ImageDraw.Draw(sh).polygon([(x+6,y+10) for x,y in pts],fill=(60,0,8,90)); sh=sh.filter(ImageFilter.GaussianBlur(9)); T.alpha_composite(sh)
    aafill(T,None,lambda dd,k:dd.polygon([(x*k,y*k) for x,y in pts],fill=255),bg); d=ImageDraw.Draw(T)
    hc=(o+31,o+h/2); aafill(T,None,lambda dd,k:dd.ellipse([(hc[0]-11)*k,(hc[1]-11)*k,(hc[0]+11)*k,(hc[1]+11)*k],fill=255),(205,200,192) if bg==W else (90,90,90)); aafill(T,None,lambda dd,k:dd.ellipse([(hc[0]-8)*k,(hc[1]-8)*k,(hc[0]+8)*k,(hc[1]+8)*k],fill=255),RED); d=ImageDraw.Draw(T)
    dc=(222,216,208) if bg==W else (80,80,80); ip=[(o+54,o+9),(o+w-9,o+9),(o+w-9,o+h-9),(o+54,o+h-9),(o+12,o+h-50),(o+12,o+50),(o+54,o+9)]
    for (x1,y1),(x2,y2) in zip(ip,ip[1:]):
        L=math.hypot(x2-x1,y2-y1); n=int(L//14)
        for k in range(n):
            if k%2==0:
                a,b=k/n,min((k+1)/n,1); d.line([x1+(x2-x1)*a,y1+(y2-y1)*a,x1+(x2-x1)*b,y1+(y2-y1)*b],fill=dc,width=2)
    x=o+64
    d.text((x,o+30),name1,font=f(20,'Bold'),fill=ink); d.text((x,o+58),name2,font=f(23,'Bold'),fill=acc)
    for i,t in enumerate(feats): d.text((x,o+104+i*27),t,font=f(18,'Medium'),fill=sub)
    num=price.replace(' €',''); fo1=f(60,'Bold'); d.text((x-2,o+h-56),num,font=fo1,fill=acc,anchor='ls')
    d.text((x+d.textlength(num,font=fo1)+4,o+h-88),'€',font=f(30,'Bold'),fill=acc,anchor='ls')
    fo=f(18,'Medium'); d.text((x,o+h-24),'+ IVA',font=fo,fill=sub,anchor='ls'); pw=d.textlength('+ IVA   ',font=fo)
    t='antes '+old; tw=d.textlength(t,font=fo); d.text((x+pw,o+h-24),t,font=fo,fill=sub,anchor='ls'); d.line([x+pw-2,o+h-29,x+pw+tw+2,o+h-33],fill=sub,width=2)
    return T
def sealimg(R=138):
    S=Image.new('RGBA',(2*R+40,2*R+40),(0,0,0,0)); d=ImageDraw.Draw(S); cx=cy=R+20
    sh=Image.new('RGBA',S.size,(0,0,0,0)); ImageDraw.Draw(sh).ellipse([cx-R+6,cy-R+12,cx+R+6,cy+R+12],fill=(60,0,8,100)); sh=sh.filter(ImageFilter.GaussianBlur(10)); S.alpha_composite(sh)
    aafill(S,None,lambda dd,k:dd.ellipse([(cx-R)*k,(cy-R)*k,(cx+R)*k,(cy+R)*k],fill=255),W)
    aafill(S,None,lambda dd,k:dd.ellipse([(cx-R+12)*k,(cy-R+12)*k,(cx+R-12)*k,(cy+R-12)*k],outline=255,width=3*k),RED); d=ImageDraw.Draw(S)
    d.text((cx,cy-90),'RENTING',font=f(24,'Bold'),fill=RED,anchor='mm'); d.text((cx,cy-60),'Scan Edition',font=f(19,'Medium'),fill=GREY,anchor='mm')
    fo1=f(84,'Bold'); nw=d.textlength('159',font=fo1); d.text((cx-14,cy+4),'159',font=fo1,fill=RED,anchor='mm'); d.text((cx-14+nw/2+4,cy-16),'€',font=f(38,'Bold'),fill=RED,anchor='lm'); d.text((cx,cy+58),'/mes + IVA',font=f(26,'Bold'),fill=INK,anchor='mm')
    fo=f(19,'Medium'); t='PVP 7.518 €'; tw=d.textlength(t,font=fo); d.text((cx,cy+92),t,font=fo,fill=GREY,anchor='mm'); d.line([cx-tw/2-4,cy+97,cx+tw/2+4,cy+88],fill=GREY,width=2)
    return S.rotate(9,resample=Image.BICUBIC,expand=True)
def build(story=False):
    H=1920 if story else 1350; oy=250 if story else 0
    c=Image.new('RGBA',(1080,H),RED+(255,)); c.alpha_composite(pattern(H)); d=ImageDraw.Draw(c)
    # cabecera: logos
    l=fitw(logo,200); ch=Image.new('RGBA',(l.width+52,l.height+30),(0,0,0,0)); ImageDraw.Draw(ch).rounded_rectangle([0,0,ch.width-1,ch.height-1],radius=ch.height//2,fill=CREAM+(255,)); ch.alpha_composite(l,(26,15))
    c.alpha_composite(ch,(50,oy+40)); xw=50+ch.width+24
    d.text((xw,oy+40+ch.height/2),'×',font=f(40,'Medium'),fill=W,anchor='lm')
    wl=fitw(whl,140); c.alpha_composite(wl,(xw+44,oy+40+(ch.height-wl.height)//2))
    # titular
    d.text((50,oy+128),'CYBER',font=f(150,'Bold'),fill=W)
    from PIL import ImageChops
    m1=Image.new('L',(1080,H),0); ImageDraw.Draw(m1).text((50,oy+262),'MONDAY',font=f(150,'Bold'),fill=255,stroke_width=3,stroke_fill=255)
    m0=Image.new('L',(1080,H),0); ImageDraw.Draw(m0).text((50,oy+262),'MONDAY',font=f(150,'Bold'),fill=255)
    c.paste(W+(255,),(0,0),ImageChops.subtract(m1,m0))
    d.text((56,oy+452),'Ofertas W&H · hasta el 4 de diciembre',font=f(28,'Bold'),fill=W,anchor='lm')
    # banda crema inclinada con el producto
    b0=oy+500; bp=[(-2,b0+30),(1082,b0-25),(1082,b0+330),(-2,b0+380)]
    bm=aafill(c,None,lambda dd,k:dd.polygon([(x*k,y*k) for x,y in bp],fill=255),CREAM); d=ImageDraw.Draw(c)
    p=fit(SYS,900,300).convert('RGB'); px,py=(1080-p.width)//2-20,b0+18
    c.paste(p,(px,py),bm.crop((px,py,px+p.width,py+p.height)))
    s=sealimg(); c.alpha_composite(s,(1080-s.width+18,oy+200))
    # etiquetas de precio
    tags=[(tag('MÓDULO','Piezomed Plus II',['Se acopla sin cables','Anillo LED+ · 24 W'],'3.800 €','4.225 €'),-5,40,b0+305),
          (tag('IMPLANTMED PLUS II','Pedal con cable',['Micromotor con luz','C.A. WS-75 L'],'4.395 €','4.688 €'),3,378,b0+330),
          (tag('IMPLANTMED PLUS II','Pedal inalámbrico',['Micromotor con luz','C.A. WS-75 L'],'4.396 €','4.698 €',bg=INK,ink=W,acc=W,sub=(200,196,190)),-4,700,b0+300)]
    for T,r,x,y in tags:
        T=T.rotate(r,resample=Image.BICUBIC,expand=True); c.alpha_composite(T,(x,y))
    c=c.convert('RGB'); d=ImageDraw.Draw(c)
    fy=b0+668
    d.text((540,fy),'3 años de garantía*  ·  Revisión anual gratuita de por vida*',font=f(24,'Bold'),fill=W,anchor='mm')
    fo=f(32,'Bold'); t='Escríbenos W&H por mensaje'; w=d.textlength(t,font=fo)+70
    d.rounded_rectangle([540-w/2,fy+30,540+w/2,fy+100],radius=35,fill=W); d.text((540,fy+65),t,font=fo,fill=RED,anchor='mm')
    if story:
        fo=f(44,'Bold'); t='¡¡OFERTA EN EL FEED!!'; w=d.textlength(t,font=fo)+90
        d.rounded_rectangle([540-w/2,fy+170,540+w/2,fy+262],radius=46,outline=W,width=4); d.text((540,fy+216),t,font=fo,fill=W,anchor='mm')
        d.text((540,fy+330),'Solo profesionales · Precios + IVA · *Consulta condiciones',font=f(20,'Medium'),fill=(255,215,220),anchor='mm')
    else:
        d.text((540,fy+135),'Solo profesionales · Precios + IVA · *Consulta condiciones con tu comercial',font=f(18,'Medium'),fill=(255,215,220),anchor='mm')
    return c
build().save(OUT+'2026-11-30-cyber-monday-wh-folleto.png')
build(True).save(OUT+'2026-11-30-historia-cyber-monday-wh-folleto.png')
