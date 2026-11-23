exec(open('cm.py').read().split('def s1(')[0])
def wcard(d,x,y,w,h,l1,l2,feats,price,old):
    d.rounded_rectangle([x,y,x+w,y+h],radius=24,fill=W)
    d.text((x+22,y+24),l1,font=f(23,'Bold'),fill=INK); d.text((x+22,y+54),l2,font=f(23,'Bold'),fill=RED)
    for i,t in enumerate(feats): d.text((x+22,y+100+i*30),'• '+t,font=f(19,'Medium'),fill=GREY)
    d.text((x+20,y+h-50),price,font=f(52,'Bold'),fill=RED,anchor='ls')
    fo=f(19,'Medium'); d.text((x+22,y+h-16),'+ IVA',font=fo,fill=GREY,anchor='ls')
    pw=d.textlength('+ IVA  ',font=fo); t='antes '+old; tw=d.textlength(t,font=fo)
    d.text((x+22+pw,y+h-16),t,font=fo,fill=GREY,anchor='ls'); d.line([x+20+pw,y+h-22,x+24+pw+tw,y+h-26],fill=GREY,width=2)
def flyer():
    c=Image.new('RGB',(1080,1350),CREAM); d=ImageDraw.Draw(c)
    d.polygon([(0,0),(1080,0),(1080,300),(0,268)],fill=RED)
    wl=fitw(whl,150); c.paste(wl,(70,42),wl)
    d.text((64,100),'CYBER MONDAY',font=f(84,'Bold'),fill=W)
    d.text((70,232),'Ofertas W&H válidas hasta el 4 de diciembre',font=f(28,'Medium'),fill=W,anchor='lm')
    b=burst(220); bd=ImageDraw.Draw(b)
    bd.text((110,78),'3 AÑOS',font=f(36,'Bold'),fill=RED,anchor='mm'); bd.text((110,115),'DE',font=f(22,'Bold'),fill=RED,anchor='mm'); bd.text((110,147),'GARANTÍA*',font=f(24,'Bold'),fill=RED,anchor='mm')
    b=b.rotate(10,resample=Image.BICUBIC,expand=True); c.paste(b,(1080-b.width-8,24),b)
    d.text((70,322),'Implantmed Plus II',font=f(54,'Bold'),fill=INK)
    d.text((70,392),'Su nuevo asistente inteligente en cirugía oral.',font=f(30,'Medium'),fill=INK)
    d.text((70,436),'Revisión anual gratuita de por vida*',font=f(26,'Bold'),fill=RED)
    # renting
    y0=492; d.rounded_rectangle([70,y0,1010,y0+225],radius=30,fill=RED)
    d.text((104,y0+30),'Implantmed Plus II',font=f(24,'Medium'),fill=W)
    d.text((104,y0+60),'SCAN EDITION · RENTING',font=f(32,'Bold'),fill=W)
    cx,cy=104,y0+118
    for t in ['Pedal inalámbrico','Función de escaneo','Micromotor con luz','C.A. WS-75 L']:
        fo=f(20,'Medium'); w=d.textlength(t,font=fo)+36
        if cx+w>620: cx=104; cy+=48
        d.rounded_rectangle([cx,cy,cx+w,cy+38],radius=19,outline=W,width=2); d.text((cx+w/2,cy+19),t,font=fo,fill=W,anchor='mm'); cx+=w+10
    d.text((975,y0+105),'159 €',font=f(110,'Bold'),fill=W,anchor='rm')
    d.text((975,y0+172),'/mes + IVA',font=f(32,'Bold'),fill=W,anchor='rm')
    fo=f(22,'Medium'); t='PVP 7.518 €'; tw=d.textlength(t,font=fo)
    d.text((975,y0+205),t,font=fo,fill=(255,205,212),anchor='rm'); d.line([975-tw-4,y0+209,979,y0+201],fill=W,width=3)
    # producto
    p=fit(SYS,1000,200); c.paste(p,((1080-p.width)//2,726))
    # tres ofertas
    cw=(940-2*16)//3; y1=936; h=306
    wcard(d,70,y1,cw,h,'Módulo','Piezomed Plus II',['Se acopla sin cables','Anillo LED+ · 24 W','Reconoce el inserto'],'3.800 €','4.225 €')
    wcard(d,70+cw+16,y1,cw,h,'Implantmed Plus II','Pedal con cable',['Micromotor con luz','C.A. WS-75 L'],'4.395 €','4.688 €')
    wcard(d,70+2*(cw+16),y1,cw,h,'Implantmed Plus II','Pedal inalámbrico',['Micromotor con luz','C.A. WS-75 L'],'4.396 €','4.698 €')
    # pie
    fy=1262; l=fitw(logo,190); c.paste(l,(70,fy+2),l)
    x=pill(d,290,fy,'Escríbenos IMPLANT',f(28,'Bold'),RED,W,58,28)
    d.text((1010,fy+16),'Solo profesionales · Precios + IVA',font=f(19,'Medium'),fill=INK,anchor='rm')
    d.text((1010,fy+44),'*Consulta condiciones con tu comercial',font=f(17,'Medium'),fill=GREY,anchor='rm')
    return c
F=flyer(); F.save(OUT+'2026-11-30-cyber-monday-wh-folleto.png')
S=Image.new('RGB',(1080,1920),CREAM); ImageDraw.Draw(S).rectangle([0,0,1080,260],fill=RED); S.paste(F,(0,250))
d=ImageDraw.Draw(S); pill(d,540,1690,'¡¡OFERTA EN EL FEED!!',f(46,'Bold'),RED,W,96,50,anchor='c')
S.save(OUT+'2026-11-30-historia-cyber-monday-wh-folleto.png')
