import numpy as np, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
A='/mnt/user-data/attachments/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/'
D='/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/lunos/'
FP='/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf'
def f(px,w='Medium'): return ImageFont.truetype(FP%w,px)
RED=(210,18,43); CREAM=(236,232,226); INK=(31,31,31); GREY=(105,102,98); W=(255,255,255)
Wd,Hd,FPS=1080,1920,30
PRICE=sys.argv[1] if len(sys.argv)>1 else '3.970 €'
dev=Image.open(A+'5b314f5c-image.webp').convert('RGB')
cart=Image.open(D+'carro.png').convert('RGB')
logo=Image.open(A+'ec1b456c-100dental-logo.png').convert('RGBA')
def mult(im):  # fondo blanco -> crema, sin recortes
    a=np.asarray(im).astype(float)*np.array(CREAM)/255.
    return Image.fromarray(a.clip(0,255).astype('uint8'))
def feather(im,m=40):  # funde bordes a crema
    w,h=im.size; mk=Image.new('L',(w,h),0); ImageDraw.Draw(mk).rectangle([m,m,w-m,h-m],fill=255)
    mk=mk.filter(ImageFilter.GaussianBlur(m/2)); bg=Image.new('RGB',(w,h),CREAM); bg.paste(im,(0,0),mk); return bg
devc=feather(mult(dev)); cartc=feather(mult(cart.crop((100,0,1100,1200))))
def white(im):
    o=Image.new('RGBA',im.size,(255,255,255,0)); o.putalpha(im.split()[-1]); return Image.composite(Image.new('RGBA',im.size,W+(255,)),o,im.split()[-1])
logoW=white(logo)
def fitw(im,w): return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
def ease(x): x=min(max(x,0),1); return 1-(1-x)**3
def eio(x): x=min(max(x,0),1); return x*x*(3-2*x)
def place(canvas,im,cx,cy,scale=1.0,alpha=1.0):
    # transformación afín continua (subpíxel), sin saltos
    w,h=im.size; sw,sh=w*scale,h*scale
    x0,y0=cx-sw/2,cy-sh/2
    a=1/scale; t=im.convert('RGBA').transform((Wd,Hd),Image.AFFINE,(a,0,-x0*a,0,a,-y0*a),resample=Image.BICUBIC,fillcolor=(0,0,0,0))
    if alpha<1: t.putalpha(t.split()[-1].point(lambda v:int(v*alpha)))
    canvas.alpha_composite(t)
def text_layer(txt,fo,fill,anchor_xy,anchor='mm',alpha=1.0,dy=0):
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L)
    x,y=anchor_xy; d.text((x,y+dy),txt,font=fo,fill=fill+(int(255*alpha),),anchor=anchor); return L
def pill(d,cx,cy,t,fo,bg,fg,padx=30,h=62,alpha=255):
    w=d.textlength(t,font=fo)+padx*2
    d.rounded_rectangle([cx-w/2,cy-h/2,cx+w/2,cy+h/2],radius=h//2,fill=bg+(alpha,)); d.text((cx,cy),t,font=fo,fill=fg+(alpha,),anchor='mm')
T_HEAD=1.9; T_A=7.4; T_B=99; T_C=12.4; END=18.9
dsc=1060/dev.width; csc=1180/cartc.height
def scene_product(c,t,im,base,t0,t1,lab,title,sub):
    k=(t-t0)/(t1-t0); s=base*(1.0+0.035*eio(k))
    place(c,im,540,1130,s)
    ap=ease((t-t0-0.25)/0.6)
    c.alpha_composite(text_layer(lab,f(28,'Medium'),GREY,(540,330),alpha=ap,dy=20*(1-ap)))
    c.alpha_composite(text_layer(title,f(66,'Bold'),INK,(540,410),alpha=ap,dy=26*(1-ap)))
    ap2=ease((t-t0-0.5)/0.6)
    c.alpha_composite(text_layer(sub,f(36,'Regular'),GREY,(540,490),alpha=ap2,dy=20*(1-ap2)))
def badge(c,t):
    if t<T_HEAD or t>T_C+0.3: return
    a=ease((t-T_HEAD-0.2)/0.4)
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); d=ImageDraw.Draw(L); pill(d,540,200,'BLACK FRIDAY',f(30,'Bold'),RED,W,34,66,int(255*a)); c.alpha_composite(L)
def head(t):
    c=Image.new('RGBA',(Wd,Hd),RED+(255,))
    a1=ease(t/0.6); a2=ease((t-0.25)/0.6); a3=ease((t-0.6)/0.6)
    c.alpha_composite(text_layer('BLACK',f(190,'Bold'),W,(540,760),alpha=a1,dy=60*(1-a1)))
    c.alpha_composite(text_layer('FRIDAY',f(190,'Bold'),W,(540,960),alpha=a2,dy=60*(1-a2)))
    c.alpha_composite(text_layer('MyLunos Duo + Carro',f(46,'Medium'),W,(540,1130),alpha=a3,dy=30*(1-a3)))
    L=fitw(logoW,330); lay=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); lay.paste(L,((Wd-L.width)//2,1640),L)
    lay.putalpha(lay.split()[-1].point(lambda v:int(v*a3))); c.alpha_composite(lay)
    return c
def endcard(t):
    t0=T_C; c=Image.new('RGBA',(Wd,Hd),RED+(255,)); d=ImageDraw.Draw(c)
    def a(dl): return ease((t-t0-dl)/0.5)
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); dd=ImageDraw.Draw(L); pill(dd,540,330,'BLACK FRIDAY',f(32,'Bold'),W,RED,36,70,int(255*a(0.1))); c.alpha_composite(L)
    c.alpha_composite(text_layer('MyLunos Duo + Carro',f(56,'Bold'),W,(540,470),alpha=a(0.2),dy=24*(1-a(0.2))))
    # miniaturas
    th=Image.new('RGBA',(Wd,Hd),(0,0,0,0))
    for im,cx in ((devc,370),(cartc,760)):
        tt=im.copy(); tt.thumbnail((330,300),Image.LANCZOS)
        card=Image.new('RGBA',(tt.width+0,tt.height+0),CREAM+(255,)); card.paste(tt,(0,0))
        mk=Image.new('L',card.size,0); ImageDraw.Draw(mk).rounded_rectangle([0,0,card.width-1,card.height-1],radius=26,fill=255)
        th.paste(card,(int(cx-card.width/2),int(700-card.height/2)),mk)
    th.putalpha(th.split()[-1].point(lambda v:int(v*a(0.35)))); c.alpha_composite(th)
    ap=a(0.6); sc=0.9+0.1*ap
    P=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); dp=ImageDraw.Draw(P)
    dp.text((540,1010),PRICE,font=f(int(190*sc),'Bold'),fill=W+(int(255*ap),),anchor='mm')
    dp.text((540,1135),'+ IVA',font=f(48,'Medium'),fill=W+(int(255*ap),),anchor='mm'); c.alpha_composite(P)
    L=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); dd=ImageDraw.Draw(L)
    pill(dd,540,1250,'ÚLTIMAS UNIDADES A ESTE PRECIO',f(32,'Bold'),(150,8,26),W,34,74,int(255*a(0.9)))
    pill(dd,540,1400,'Escríbenos LUNOS por mensaje',f(40,'Bold'),W,RED,44,96,int(255*a(1.2)))
    for txt,cx in (('Solo profesionales',540),):
        w=dd.textlength(txt,font=f(28))+56; al=int(255*a(1.4))
        dd.rounded_rectangle([cx-w/2,1510,cx+w/2,1566],radius=28,outline=W+(al,),width=2); dd.text((cx,1538),txt,font=f(28),fill=W+(al,),anchor='mm')
    c.alpha_composite(L)
    Lg=fitw(logoW,300); lay=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); lay.paste(Lg,((Wd-Lg.width)//2,1680),Lg)
    lay.putalpha(lay.split()[-1].point(lambda v:int(v*a(1.5)))); c.alpha_composite(lay)
    return c
def frame(t):
    if t<T_HEAD: return head(t)
    def shift(L,dx): return L.transform((Wd,Hd),Image.AFFINE,(1,0,-dx,0,1,0),resample=Image.BICUBIC,fillcolor=CREAM+(255,))
    c=Image.new('RGBA',(Wd,Hd),CREAM+(255,))
    k=eio((t-T_A)/0.7) if t>=T_A else 0
    if k<1:
        L=Image.new('RGBA',(Wd,Hd),CREAM+(255,)); scene_product(L,t,devc,dsc,T_HEAD,T_A+0.7,'DÜRR DENTAL · LUNOS','MyLunos Duo Pro','Ultrasonidos y pulido en un equipo')
        c=shift(L,-Wd*k) if k>0 else L
    if t>=T_A:
        B=Image.new('RGBA',(Wd,Hd),CREAM+(255,)); scene_product(B,t,cartc,csc,T_A,T_C+0.6,'Y ADEMÁS','+ Carro MyLunos Cart','Todo ordenado y a mano')
        B=shift(B,Wd*(1-k)); 
        if k<1:
            mk=Image.new('L',(Wd,Hd),0); ImageDraw.Draw(mk).rectangle([int(Wd*(1-k)),0,Wd,Hd],fill=255); c.paste(B,(0,0),mk)
        else: c=B
    badge(c,t)
    # cortinilla roja de entrada
    if t<T_HEAD+0.55:
        k=eio((t-T_HEAD)/0.55); h=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); hh=head(T_HEAD)
        c.alpha_composite(hh.transform((Wd,Hd),Image.AFFINE,(1,0,0,0,1,Hd*k),resample=Image.BICUBIC))
    if t>=T_C:
        e=endcard(t); k=eio((t-T_C)/0.55)
        sl=Image.new('RGBA',(Wd,Hd),(0,0,0,0)); sl.alpha_composite(e.transform((Wd,Hd),Image.AFFINE,(1,0,0,0,1,-Hd*(1-k)),resample=Image.BICUBIC))
        c.alpha_composite(sl)
    return c
if __name__=='__main__':
    mode=sys.argv[2] if len(sys.argv)>2 else 'render'
    if mode=='stills':
        for t in (7.5,7.75,7.9,12.0): frame(t).convert('RGB').resize((360,640)).save(D+'v/s_%05.2f.png'%t)
    else:
        p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r','30','-i','-','-c:v','libx264','-crf','14','-preset','slow','-pix_fmt','yuv420p',D+'raw.mp4'],stdin=subprocess.PIPE)
        n=int(END*FPS)
        for i in range(n): p.stdin.write(frame(i/FPS).convert('RGB').tobytes())
        p.stdin.close(); p.wait()
