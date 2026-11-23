from PIL import Image, ImageDraw, ImageFont, ImageFilter
A='/mnt/user-data/attachments/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/'
DS='/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/ds/'
O='/home/claude/out/curso/'
FP='/usr/share/fonts/truetype/google-fonts/Poppins-%s.ttf'
def f(px,w='Medium'): return ImageFont.truetype(FP%w,px)
RED=(210,18,43); CREAM=(236,232,226); INK=(31,31,31); GREY=(70,68,64); W=(255,255,255)
logo=Image.open(A+'ec1b456c-100dental-logo.png').convert('RGBA'); dsl=Image.open(DS+'im-003_a.png').convert('RGBA')
def fitw(im,w): return im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
def logos(c,y,x=70,lw=230,dw=150):
    l=fitw(logo,lw); ds=fitw(dsl,dw); c.alpha_composite(l,(x,y)); c.alpha_composite(ds,(x+l.width+34,y+(l.height-ds.height)//2))
def cta(d,y):
    fo=f(40,'Bold'); s='Síguenos para no perderte más'; w=d.textlength(s,font=fo)+90
    d.rounded_rectangle([540-w/2,y,540+w/2,y+90],radius=45,fill=RED); d.text((540,y+45),s,font=fo,fill=W,anchor='mm')

# Historia 1: foto de grupo
c=Image.new('RGBA',(1080,1920),CREAM+(255,)); d=ImageDraw.Draw(c)
logos(c,230)
d.rectangle([70,400,114,404],fill=RED)
d.text((70,456),'CURSO · 20.11.2026 · GRANADA',font=f(26,'Medium'),fill=RED,anchor='ls')
d.text((66,540),'Gracias a todos',font=f(76,'Bold'),fill=INK,anchor='ls')
d.text((66,628),'los que vinisteis',font=f(76,'Bold'),fill=INK,anchor='ls')
g=fitw(Image.open(A+'6256e1da-image.jpg').convert('RGB'),1080); c.paste(g,(0,700))
y=700+g.height
d.text((70,y+80),'Y a @dentsplysirona.iberia y al Dr. Juan Miraglia',font=f(32,'Regular'),fill=GREY,anchor='ls')
d.text((70,y+124),'por hacerlo posible.',font=f(32,'Regular'),fill=GREY,anchor='ls')
cta(d,y+250)
c.convert('RGB').save(O+'historia-curso-1-gracias.png')

# Historia 2: lo que vimos
c=Image.new('RGBA',(1080,1920),CREAM+(255,)); d=ImageDraw.Draw(c)
p=Image.open(A+'80177d22-image.jpg').convert('RGB'); p=fitw(p,1080); ph=1000
top=max(0,int((p.height-ph)*0.35)); c.paste(p.crop((0,top,1080,top+ph)),(0,0))
y=ph+80
d.rectangle([70,y-30,114,y-26],fill=RED)
d.text((70,y+20),'ENDODONCIA 2026 · DR. JUAN MIRAGLIA',font=f(26,'Medium'),fill=RED,anchor='ls')
d.text((66,y+100),'Lo que vimos en el curso',font=f(60,'Bold'),fill=INK,anchor='ls')
items=[('01','Instrumentación mínimamente invasiva','con RECIPROC® Mínima'),('02','Nuevos motores de endodoncia','X-Smart Pro+ y cómo configurarlos'),('03','Obturación biocerámica','con ProRoot® BioSealer')]
yy=y+190
for n,a,b in items:
    d.text((70,yy+40),n,font=f(44,'Bold'),fill=RED,anchor='ls')
    d.text((160,yy+18),a,font=f(32,'Bold'),fill=INK,anchor='ls'); d.text((160,yy+58),b,font=f(28,'Regular'),fill=GREY,anchor='ls')
    yy+=110
d.text((70,yy+30),'Y por la tarde, taller práctico.',font=f(30,'Medium'),fill=INK,anchor='ls')
d.text((70,yy+90),'Con @dentsplysirona.iberia',font=f(30,'Bold'),fill=RED,anchor='ls')
logos(c,1790,70,200,130)
c.convert('RGB').save(O+'historia-curso-2-contenido.png')
