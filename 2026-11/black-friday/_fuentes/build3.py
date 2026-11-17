import numpy as np, subprocess, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
exec(open('/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/lunos/build.py').read().split('T_HEAD=1.9')[0])
_d=Image.open(D+'of/pack2.png').convert('RGB')
devc=feather(mult(_d),30); cartc=feather(mult(Image.open(D+'of/cart3.png').convert('RGB')),30); dev=devc
B=60/124
def back(x,s=1.7):  # ease-out con rebote corto
    x=min(max(x,0),1); x-=1; return x*x*((s+1)*x+s)+1
def slam(c,txt,fo,fill,cy,t0,t,big=1.5,dur=0.28):
    if t<t0: return
    k=back((t-t0)/dur); sc=big-(big-1)*k; a=min(1,(t-t0)/0.08)
    L=text_layer(txt,fo,fill,(540,cy),alpha=a)
    if abs(sc-1)>1e-3:
        L=L.transform((Wd,Hd),Image.AFFINE,(1/sc,0,540-540/sc,0,1/sc,cy-cy/sc),resample=Image.BICUBIC)
    c.alpha_composite(L)
def flash(c,t,t0,st=0.45,dur=0.16):
    if t0<=t<t0+dur:
        a=st*(1-(t-t0)/dur); c.alpha_composite(Image.new('RGBA',(Wd,Hd),(255,255,255,int(255*a))))
_fo=f(34,'Bold'); _tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
_items=[('BLACK FRIDAY',40),('•',40),('ÚLTIMAS UNIDADES',40),('•',40)]
U=int(sum(_tmp.textlength(x,font=_fo)+g for x,g in _items))
unit=Image.new('RGBA',(U,70),RED+(255,)); du=ImageDraw.Draw(unit); x=0
for txt,g in _items: du.text((x,35),txt,font=_fo,fill=W,anchor='lm'); x+=_tmp.textlength(txt,font=_fo)+g
reps=Wd//U+2; TK=Image.new('RGBA',(U*reps,70)); [TK.paste(unit,(i*U,0)) for i in range(reps)]
def ticker(c,t,y=1700,inv=False):
    off=(t*160)%U; strip=TK.crop((int(off),0,int(off)+Wd,70))
    if inv:
        a=np.asarray(strip).copy(); m=(a[...,0]>200)&(a[...,1]>200); a[...,:3]=np.where(m[...,None],np.array(RED),np.array(W)); strip=Image.fromarray(a)
    c.alpha_composite(strip,(0,y))
def callout(c,t,t0,px,py,lx,ly,txt):
    if t<t0: return
    k=ease((t-t0)/0.35); L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L)
    ex=px+(lx-px)*k; ey=py+(ly-py)*k
    d.line([px,py,ex,ey],fill=RED+(255,),width=4)
    r=9+3*math.sin(min(1,(t-t0)/0.3)*math.pi); d.ellipse([px-r,py-r,px+r,py+r],fill=RED+(255,)); d.ellipse([px-r-7,py-r-7,px+r+7,py+r+7],outline=RED+(120,),width=3)
    if k>0.6:
        a=int(255*min(1,(k-0.6)/0.4)); fo=f(34,'Bold'); w=d.textlength(txt,font=fo)+48
        x0=lx-w/2 if abs(lx-540)<200 else (lx if lx>px else lx-w); x0=max(40,min(x0,1040-w))
        d.rounded_rectangle([x0,ly-32,x0+w,ly+32],radius=32,fill=W+(a,),outline=RED+(a,),width=3); d.text((x0+w/2,ly),txt,font=fo,fill=INK+(a,),anchor='mm')
    c.alpha_composite(L)
DEV_C=(540,1130); DSC=1040/devc.width; CART_C=(540,1110); CSC=1100/cartc.height
def devpt(x,y,s): return DEV_C[0]+(x-dev.width/2)*s, DEV_C[1]+(y-dev.height/2)*s
def cartpt(x,y,s): return CART_C[0]+(x-cartc.width/2)*s, CART_C[1]+(y-cartc.height/2)*s
T1=4*B; T2=14*B; T3=16*B; T4=24*B; T5=26*B; END=40*B
def titles(c,t,t0,lab,title,sub):
    ap=ease((t-t0-0.15)/0.45)
    c.alpha_composite(text_layer(lab,f(28,'Medium'),GREY,(540,330),alpha=ap,dy=20*(1-ap)))
    c.alpha_composite(text_layer(title,f(66,'Bold'),INK,(540,410),alpha=ap,dy=26*(1-ap)))
    ap2=ease((t-t0-0.35)/0.45); c.alpha_composite(text_layer(sub,f(36,'Regular'),GREY,(540,490),alpha=ap2,dy=20*(1-ap2)))
def badge2(c,t):
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L); pill(d,540,200,'BLACK FRIDAY',f(30,'Bold'),RED,W,34,66); c.alpha_composite(L)
def red_bg(): return Image.new('RGBA',(Wd,Hd),RED+(255,))
def frame(t):
    if t<T1:
        c=red_bg()
        slam(c,'BLACK',f(200,'Bold'),W,760,0.0,t); flash(c,t,0.05)
        slam(c,'FRIDAY',f(200,'Bold'),W,970,B,t); flash(c,t,B+0.05)
        if t>=2*B:
            a=ease((t-2*B)/0.4); c.alpha_composite(text_layer('MyLunos Duo + Carro',f(50,'Medium'),W,(540,1150),alpha=a,dy=30*(1-a)))
        if t>=3*B:
            L=fitw(logoW,320); lay=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); lay.paste(L,((Wd-L.width)//2,1600),L)
            lay.putalpha(lay.split()[-1].point(lambda v:int(v*ease((t-3*B)/0.3)))); c.alpha_composite(lay)
        ticker(c,t,1780,inv=True)
        return c
    if t<T2:
        c=Image.new('RGBA',(Wd,Hd),CREAM+(255,)); k=(t-T1)
        s=DSC*(1.12-0.12*ease(k/0.6))*(1+0.025*eio((t-T1)/(T2-T1)))
        place(c,devc,DEV_C[0],DEV_C[1],s)
        titles(c,t,T1,'DÜRR DENTAL · LUNOS','MyLunos Duo Pro','Ultrasonidos y pulido en un equipo')
        for i,(x,y,lx,ly,txt) in enumerate(((831,209,250,640,'Ultrasonidos'),(1633,320,880,640,'Pulido'))):
            px,py=devpt(x,y,s); callout(c,t,T1+(6+2*i)*B-T1+T1-6*B+6*B if False else T1+(3+2*i)*B,px,py,lx,ly,txt)
        badge2(c,t); ticker(c,t,1720)
        if t<T1+0.45:
            k=eio((t-T1)/0.45); h=frame(T1-0.001); c.alpha_composite(h.transform((Wd,Hd),Image.AFFINE,(1,0,0,0,1,Hd*k),resample=Image.BICUBIC))
        return c
    if t<T3:
        c=red_bg(); slam(c,'+ CARRO',f(170,'Bold'),W,900,T2,t); flash(c,t,T2+0.03)
        if t>=T2+B:
            a=ease((t-T2-B)/0.3); c.alpha_composite(text_layer('MyLunos Cart',f(60,'Medium'),W,(540,1060),alpha=a,dy=20*(1-a)))
        ticker(c,t,1780,inv=True); return c
    if t<T4:
        c=Image.new('RGBA',(Wd,Hd),CREAM+(255,))
        s=CSC*(1.12-0.12*ease((t-T3)/0.6))*(1+0.025*eio((t-T3)/(T4-T3)))
        place(c,cartc,CART_C[0],CART_C[1],s)
        titles(c,t,T3,'Y ADEMÁS','+ Carro MyLunos Cart','Todo montado y a mano')
        for i,(x,y,lx,ly,txt) in enumerate(((800,770,930,770,'Cajón'),(850,1220,930,1010,'2 baldas'),(330,2080,170,1450,'Con ruedas'))):
            px,py=cartpt(x,y,s); callout(c,t,T3+(2+2*i)*B,px,py,lx,ly,txt)
        badge2(c,t); ticker(c,t,1720)
        if t<T3+0.4:
            k=eio((t-T3)/0.4); h=frame(T3-0.001); c.alpha_composite(h.transform((Wd,Hd),Image.AFFINE,(1,0,0,0,1,-Hd*k),resample=Image.BICUBIC))
        return c
    if t<T5:
        c=red_bg(); slam(c,'ÚLTIMAS',f(170,'Bold'),W,830,T4,t); flash(c,t,T4+0.03)
        slam(c,'UNIDADES',f(150,'Bold'),W,1010,T4+B,t); flash(c,t,T4+B+0.03)
        ticker(c,t,1780,inv=True); return c
    # cierre
    c=red_bg(); d=ImageDraw.Draw(c); t0=T5
    def a(dl): return ease((t-t0-dl)/0.35)
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); dd=ImageDraw.Draw(L); pill(dd,540,300,'BLACK FRIDAY',f(32,'Bold'),W,RED,36,70,int(255*a(0))); c.alpha_composite(L)
    c.alpha_composite(text_layer('MyLunos Duo + Carro',f(56,'Bold'),W,(540,430),alpha=a(0.1),dy=24*(1-a(0.1))))
    th=Image.new('RGBA',(Wd,Hd),(0,0,0,0))
    for im,cx in ((devc,370),(cartc,760)):
        tt=im.copy(); tt.thumbnail((330,300),Image.LANCZOS); mk=Image.new('L',tt.size,0); ImageDraw.Draw(mk).rounded_rectangle([0,0,tt.width-1,tt.height-1],radius=26,fill=255)
        th.paste(tt,(int(cx-tt.width/2),int(660-tt.height/2)),mk)
    th.putalpha(th.split()[-1].point(lambda v:int(v*a(0.2)))); c.alpha_composite(th)
    slam(c,PRICE,f(200,'Bold'),W,990,t0+2*B,t,big=1.8,dur=0.32); flash(c,t,t0+2*B+0.04,0.5)
    if t>=t0+2*B: c.alpha_composite(text_layer('+ IVA',f(50,'Medium'),W,(540,1120),alpha=ease((t-t0-2*B-0.2)/0.3)))
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); dd=ImageDraw.Draw(L)
    if t>=t0+4*B:
        pul=1+0.04*max(0,math.sin((t-t0)*2*math.pi/(2*B)))
        P=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); pill(ImageDraw.Draw(P),540,1235,'ÚLTIMAS UNIDADES A ESTE PRECIO',f(32,'Bold'),(150,8,26),W,34,74,int(255*a(4*B)))
        P=P.transform((Wd,Hd),Image.AFFINE,(1/pul,0,540-540/pul,0,1/pul,1235-1235/pul),resample=Image.BICUBIC); c.alpha_composite(P)
    pill(dd,540,1380,'Escríbenos LUNOS por mensaje',f(40,'Bold'),W,RED,44,96,int(255*a(5*B)))
    w=dd.textlength('Solo profesionales',font=f(28))+56; al=int(255*a(6*B))
    dd.rounded_rectangle([540-w/2,1475,540+w/2,1531],radius=28,outline=W+(al,),width=2); dd.text((540,1503),'Solo profesionales',font=f(28),fill=W+(al,),anchor='mm')
    c.alpha_composite(L)
    Lg=fitw(logoW,290); lay=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); lay.paste(Lg,((Wd-Lg.width)//2,1600),Lg)
    lay.putalpha(lay.split()[-1].point(lambda v:int(v*a(6*B)))); c.alpha_composite(lay)
    ticker(c,t,1780,inv=True)
    return c
if __name__=='__main__':
    mode=sys.argv[2] if len(sys.argv)>2 else 'render'
    if mode=='stills':
        ts=[float(x) for x in sys.argv[3].split(',')]
        for i,t in enumerate(ts): frame(t).convert('RGB').resize((360,640)).save(D+'v/o_%02d.png'%i)
    else:
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','14','-preset','slow','-pix_fmt','yuv420p',D+'raw3.mp4'],stdin=subprocess.PIPE)
        for i in range(int(END*30)): p.stdin.write(frame(i/30).convert('RGB').tobytes())
        p.stdin.close(); p.wait()
