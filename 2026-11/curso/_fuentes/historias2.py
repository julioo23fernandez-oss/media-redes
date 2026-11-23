exec(open('historias.py').read().split('# Historia 1')[0])
D='/tmp/claude-0/-home-claude/4e2a7adb-d9d1-55f9-8098-6e0e73499dc0/scratchpad/curso/'
def topimg(c,path,h=1000,ay=0.4,ax=0.5):
    p=Image.open(path).convert('RGB'); s=max(1080/p.width,h/p.height); p=p.resize((int(p.width*s),int(p.height*s)),Image.LANCZOS)
    x=int((p.width-1080)*ax); y=int((p.height-h)*ay); c.paste(p.crop((x,y,x+1080,y+h)),(0,0))
def head(d,y,kick,title):
    d.rectangle([70,y-30,114,y-26],fill=RED); d.text((70,y+20),kick,font=f(26,'Medium'),fill=RED,anchor='ls'); d.text((66,y+100),title,font=f(60,'Bold'),fill=INK,anchor='ls')
def mentions(d,y): d.text((70,y),'Con @dentsplysirona.iberia y @rosario.alberto_prof',font=f(30,'Bold'),fill=RED,anchor='ls')

# Historia 3: taller práctico
c=Image.new('RGBA',(1080,1920),CREAM+(255,)); d=ImageDraw.Draw(c)
topimg(c,D+'taller4k.png',1000,0.5)
y=1080; head(d,y,'ENDODONCIA 2026 · TALLER PRÁCTICO','De la teoría a la práctica')
yy=y+190
for n,a in [('01','Configuración del motor X-Smart Pro+'),('02','Instrumentación con RECIPROC® Mínima'),('03','Obturación con ProRoot® BioSealer')]:
    d.text((70,yy+22),n,font=f(44,'Bold'),fill=RED,anchor='ls'); d.text((160,yy+18),a,font=f(32,'Bold'),fill=INK,anchor='ls'); yy+=86
d.text((70,yy+40),'Un tratamiento completo, paso a paso.',font=f(30,'Regular'),fill=GREY,anchor='ls')
mentions(d,yy+110); logos(c,1790,70,200,130)
c.convert('RGB').save(O+'historia-curso-3-taller.png')

# Historia 4: ponente
c=Image.new('RGBA',(1080,1920),CREAM+(255,)); d=ImageDraw.Draw(c)
topimg(c,A+'1b9b1f60-image.jpg',1000,0.0,0.62)
y=1080; head(d,y,'PONENTE · ENDODONCIA 2026','Dr. Juan Miraglia')
yy=y+170
for t in ['Práctica exclusiva en endodoncia microscópica y microcirugía apical','Director clínico de Miraglia Endodoncia Costa del Sol','Profesor del Máster de Endodoncia Avanzada (URJC)','Profesor invitado del Máster de Endodoncia de la Universidad de Granada']:
    d.ellipse([72,yy-14,84,yy-2],fill=RED)
    # wrap
    words=t.split(); line=''; lines=[]
    for w in words:
        if d.textlength(line+' '+w,font=f(29,'Regular'))>880: lines.append(line); line=w
        else: line=(line+' '+w).strip()
    lines.append(line)
    for L in lines: d.text((104,yy),L,font=f(29,'Regular'),fill=INK,anchor='ls'); yy+=40
    yy+=22
mentions(d,yy+50); logos(c,1790,70,200,130)
c.convert('RGB').save(O+'historia-curso-4-ponente.png')
