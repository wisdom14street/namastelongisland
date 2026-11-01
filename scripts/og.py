from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
W,H=1200,630
F='/usr/share/fonts/truetype/sand-box/google/'
yes=ImageFont.truetype(F+'Yeseva One/YesevaOne-Regular.ttf',96)
yes2=ImageFont.truetype(F+'Yeseva One/YesevaOne-Regular.ttf',64)
sub=ImageFont.truetype(F+'Poppins/Poppins-SemiBold.ttf',34)
sm=ImageFont.truetype(F+'Poppins/Poppins-Medium.ttf',26)
im=Image.new('RGB',(W,H),'#FFF1D6');d=ImageDraw.Draw(im)
# warm gradient
for y in range(H):
    t=y/H; d.line([(0,y),(W,y)],fill=(255,int(241-20*t),int(214+20*t)))
# rangoli on the right
cx,cy=1100,370
lay=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(lay)
cols=['#C2185B','#F2A007','#0E6B6B','#E8630A','#C2185B']
for ring,(r,n,c) in enumerate([(220,24,cols[0]),(175,16,cols[1]),(130,12,cols[2]),(88,8,cols[3]),(48,8,cols[1])]):
    for i in range(n):
        a=2*math.pi*i/n; x=cx+r*math.cos(a); y=cy+r*math.sin(a); s=r*0.18+8
        ld.ellipse([x-s,y-s*0.6,x+s,y+s*0.6] if ring%2 else [x-s*0.6,y-s,x+s*0.6,y+s],fill=c)
ld.ellipse([cx-30,cy-30,cx+30,cy+30],fill='#FFF7EC')
lay=lay.filter(ImageFilter.GaussianBlur(0.6))
im.paste(lay,(0,0),lay)
d=ImageDraw.Draw(im)
# toran
d.rectangle([0,0,W,30],fill='#C2185B')
for i,x in enumerate(range(0,W,30)):
    d.polygon([(x,30),(x+26,30),(x+13,30+(26 if i%2 else 40))],fill=['#F2A007','#2E7D32','#E8630A','#2E7D32'][i%4])
# diya
dx,dy=70,170
d.ellipse([dx+28,dy-60,dx+62,dy+6],fill='#F2A007');d.ellipse([dx+37,dy-38,dx+53,dy],fill='#FFE08A')
d.chord([dx,dy-20,dx+90,dy+60],0,180,fill='#C2185B')
d.text((70,250),'Namaste',font=yes,fill='#2A1712')
d.text((70,350),'Long Island',font=yes,fill='#C2185B')
d.text((72,480),'Weddings · Festivals · Food · Community',font=sub,fill='#0E6B6B')
d.text((72,540),'namastelongisland.com  ·  free listings for local businesses',font=sm,fill='#6B4E43')
im.save('dist/og.jpg',quality=88,optimize=True)
print('ok')
