exec(open('fl.py').read().split('def flyer(')[0])
def pattern(H):
    L=Image.new('RGBA',(2000,2400),(0,0,0,0)); d=ImageDraw.Draw(L); fo=f(110,'Bold')
    for r in range(0,24):
        y=r*120; x=-((r*170)%700)
        while x<2000:
            d.text((x,y),'CYBER MONDAY',font=fo,fill=(0,0,0,0),stroke_width=2,stroke_fill=(255,255,255,30)); x+=d.textlength('CYBER MONDAY',font=fo)+60
    L=L.rotate(-14,resample=Image.BICUBIC); return L.crop((460,500,460+1080,500+H))
def seal(d,cx,cy,R):
    d.ellipse([cx-R-10,cy-R-10,cx+R+10,cy+R+10],fill=RED)
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=W)
    d.ellipse([cx-R+14,cy-R+14,cx+R-14,cy+R-14],outline=RED,width=3)
    d.text((cx,cy-92),'RENTING',font=f(24,'Bold'),fill=RED,anchor='mm'); d.text((cx,cy-62),'Scan Edition',font=f(19,'Medium'),fill=GREY,anchor='mm')
    d.text((cx,cy+2),'159 €',font=f(78,'Bold'),fill=RED,anchor='mm')
    d.text((cx,cy+60),'/mes + IVA',font=f(26,'Bold'),fill=INK,anchor='mm')
    fo=f(20,'Medium'); t='PVP 7.518 €'; tw=d.textlength(t,font=fo)
    d.text((cx,cy+94),t,font=fo,fill=GREY,anchor='mm'); d.line([cx-tw/2-4,cy+99,cx+tw/2+4,cy+90],fill=GREY,width=2)
def build(story=False):
    H=1920 if story else 1350; oy=250 if story else 0
    c=Image.new('RGBA',(1080,H),RED+(255,)); c.alpha_composite(pattern(H)); c=c.convert('RGB'); d=ImageDraw.Draw(c)
    wl=fitw(whl,150); c.paste(wl,(64,oy+48),wl)
    d.text((58,oy+100),'CYBER',font=f(140,'Bold'),fill=W)
    d.text((58,oy+228),'MONDAY',font=f(140,'Bold'),fill=W)
    d.text((66,oy+400),'Ofertas W&H · hasta el 4 de diciembre',font=f(26,'Medium'),fill=W,anchor='lm')
    # escenario crema con el producto
    y0=oy+445; d.rounded_rectangle([50,y0,1030,y0+400],radius=44,fill=CREAM)
    p=fit(SYS,880,300); c.paste(p,((1080-p.width)//2-40,y0+40))
    d.text((70+20,y0+360),'Implantmed Plus II + módulo Piezomed Plus II',font=f(24,'Medium'),fill=INK,anchor='lm')
    seal(d,880,oy+330,140)
    # tres precios
    cw=(980-2*14)//3; y1=y0+425; h=300
    wcard(d,50,y1,cw,h,'Módulo','Piezomed Plus II',['Se acopla sin cables','Anillo LED+ · 24 W','Reconoce el inserto'],'3.800 €','4.225 €')
    wcard(d,50+cw+14,y1,cw,h,'Implantmed Plus II','Pedal con cable',['Micromotor con luz','C.A. WS-75 L'],'4.395 €','4.688 €')
    wcard(d,50+2*(cw+14),y1,cw,h,'Implantmed Plus II','Pedal inalámbrico',['Micromotor con luz','C.A. WS-75 L'],'4.396 €','4.698 €')
    fy=y1+h+22
    d.text((540,fy+12),'3 años de garantía*  ·  Revisión anual gratuita de por vida*',font=f(24,'Bold'),fill=W,anchor='mm')
    l=fitw(logo,190); ch=Image.new('RGBA',(l.width+56,l.height+32),(0,0,0,0)); ImageDraw.Draw(ch).rounded_rectangle([0,0,ch.width-1,ch.height-1],radius=ch.height//2,fill=CREAM+(255,)); ch.alpha_composite(l,(28,16))
    c.paste(ch,(50,fy+44),ch)
    pill(d,1030,fy+48,'Escríbenos IMPLANT',f(30,'Bold'),W,RED,64,32,anchor='r') if False else None
    fo=f(30,'Bold'); w=d.textlength('Escríbenos IMPLANT',font=fo)+64
    d.rounded_rectangle([1030-w,fy+46,1030,fy+110],radius=32,fill=W); d.text((1030-w/2,fy+78),'Escríbenos IMPLANT',font=fo,fill=RED,anchor='mm')
    if story:
        pill(d,540,fy+190,'¡¡OFERTA EN EL FEED!!',f(46,'Bold'),W,RED,96,50,anchor='c')
        d.text((540,fy+330),'Solo profesionales · Precios + IVA · *Consulta condiciones',font=f(20,'Medium'),fill=(255,215,220),anchor='mm')
    else:
        d.text((540,1330),'Solo profesionales · Precios + IVA · *Consulta condiciones con tu comercial',font=f(18,'Medium'),fill=(255,215,220),anchor='mm')
    return c
build().save(OUT+'2026-11-30-cyber-monday-wh-folleto.png')
build(True).save(OUT+'2026-11-30-historia-cyber-monday-wh-folleto.png')
