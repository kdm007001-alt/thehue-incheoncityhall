from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import math

ROOT = Path(__file__).parent
ASSETS = ROOT / 'assets'
FONT = ASSETS / 'NotoSansKR.ttf'
W = 1258
NAVY = '#0b2947'
BLUE = '#153b5c'
INK = '#182938'
MUTED = '#626b73'
GOLD = '#8c8175'
PAPER = '#ffffff'

def font(size, bold=False):
    f = ImageFont.truetype(str(FONT), size)
    if bold:
        try: f.set_variation_by_name('Bold')
        except OSError: pass
    return f

def canvas(h, color=PAPER):
    im = Image.new('RGB', (W, h), color)
    return im, ImageDraw.Draw(im)

def center(draw, y, value, size, fill=INK, bold=False):
    draw.text((W//2,y), value, font=font(size,bold), fill=fill, anchor='mt')

def txt(draw, xy, value, size=26, fill=INK, bold=False):
    draw.text(xy, value, font=font(size,bold), fill=fill)

def photo(im, path, box, pos=(0.5,0.5)):
    src = Image.open(ASSETS / path).convert('RGB')
    x0,y0,x1,y1 = box
    cropped = ImageOps.fit(src,(x1-x0,y1-y0),centering=pos,method=Image.Resampling.LANCZOS)
    im.paste(cropped,(x0,y0))

def footer_note(draw, y):
    txt(draw,(50,y),'※ 자료의 위치와 표시는 이해를 돕기 위한 것으로 실제 현황과 차이가 있을 수 있습니다.',19,MUTED)

def overview():
    im,d=canvas(1260)
    d.rectangle((0,0,W,650),fill=NAVY)
    d.rectangle((0,0,W,650),fill=NAVY)
    center(d,76,'인천 도심의 새로운 주거 중심',40,'#ffffff')
    center(d,154,'인천시청역 한신더휴',76,'#ffffff',True)
    d.line((625,268,625,360),fill='#afbac2',width=2)
    center(d,386,'THE HUE',52,'#ffffff')
    center(d,459,'총 469세대 · 인천 남동구 간석동',27,'#d8e2e9')
    center(d,545,'PROJECT OVERVIEW',21,'#adb9c5')
    fields=[('대지위치','인천광역시 남동구 간석동 514번지 일원'),('단지규모','지하 3층~지상 최고 25층 · 6개동'),('세대수','총 469세대'),('주택형','전용 46·52·59·74·84㎡'),('입주','2025년 12월 입주 안내'),('시공','한신공영㈜')]
    for n,(k,v) in enumerate(fields):
        x=50+(n%3)*408; y=714+(n//3)*215
        txt(d,(x,y),k,31,INK,True)
        d.line((x,y+65,x+360,y+65),fill='#4a5660',width=1)
        txt(d,(x,y+90),v,23,MUTED)
    txt(d,(50,1170),'인천시청역 한신더휴  |  인천광역시 남동구 석산로62번길 35',23,INK)
    footer_note(d,1215)
    im.save(ASSETS/'overview.png',optimize=True)

def schematic(d,ox,oy):
    d.rounded_rectangle((ox,oy,ox+1158,oy+710),radius=13,fill='#f8f9f9',outline='#d7dce0',width=2)
    for i in range(6):
        xx=ox+100+i*195
        d.line((xx,oy+25,xx-210,oy+685),fill='#dce0e2',width=11)
    for i in range(6):
        yy=oy+95+i*115
        d.line((ox+28,yy,ox+1130,yy-130),fill='#e0e4e6',width=10)
    d.line((ox+150,oy+560,ox+970,oy+85),fill='#236192',width=22)
    d.line((ox+80,oy+230,ox+1000,oy+480),fill='#d0a34a',width=19)
    for x,y,label in [(ox+710,oy+250,'인천시청역'),(ox+540,oy+340,'인천시청'),(ox+800,oy+454,'중앙공원'),(ox+340,oy+480,'상인천초'),(ox+440,oy+190,'석바위시장')]:
        d.ellipse((x-11,y-11,x+11,y+11),fill='#657887')
        txt(d,(x+18,y-20),label,25,INK,True)
    d.rounded_rectangle((ox+330,oy+340,ox+665,oy+410),radius=10,fill=NAVY)
    txt(d,(ox+357,oy+350),'인천시청역 한신더휴',27,'white',True)
    txt(d,(ox+66,oy+628),'인천 남동구 간석동 514번지 일원',23,INK,True)
    txt(d,(ox+855,oy+628),'위치 안내 개념도',19,MUTED)

def location():
    im,d=canvas(2840)
    center(d,66,'인천시청역 한신더휴  LOCATION',52,NAVY,True)
    center(d,154,'인천의 중심을 누리는 입지',34,GOLD)
    schematic(d,50,260)
    center(d,1020,'◎  크게보기',29,NAVY,True)
    rows=[
        ('두 노선이 만나는 교통 중심','인천 지하철 1·2호선 환승역인\n인천시청역 생활권', 'rendering.jpg'),
        ('도보권 교육 환경','상인천초·상인천여중·동인천중 등\n주변 학교와 교육시설', 'rendering.jpg'),
        ('도심 속 생활 인프라','인천시청과 구월동 상권,\n쇼핑·문화·의료시설 이용', 'rendering.jpg'),
        ('공원과 이어지는 일상','인천중앙공원 등 녹지와 함께하는\n도심 주거환경', 'rendering.jpg')]
    for i,(h,s,p) in enumerate(rows):
        y=1105+i*402
        left=i%2==0
        box=(50,y,665,y+355) if left else (645,y,1208,y+355)
        photo(im,p,box,pos=((0.25 if i==0 else 0.7),0.65))
        x=704 if left else 82
        d.rectangle((x,y+52,x+13,y+105),fill=NAVY)
        txt(d,(x+34,y+48),h,38,INK,True)
        for j,line in enumerate(s.split('\n')): txt(d,(x+34,y+132+j*44),line,27,MUTED)
        txt(d,(box[2]-98,y+318),'현장 이미지',16,'#ffffff')
    footer_note(d,2750)
    im.save(ASSETS/'location.png',optimize=True)

def premium():
    im,d=canvas(1340)
    center(d,48,'인천시청역 한신더휴  PREMIUM 6',56,NAVY,True)
    items=[
        ('01','인천시청역 생활권','인천 지하철 1·2호선 환승역을\n이용하는 도심 교통 입지'),
        ('02','469세대 주거 단지','지하 3층~지상 25층, 6개동\n총 469세대 규모'),
        ('03','가까운 교육시설','상인천초·상인천여중 등\n주변 교육시설'),
        ('04','편리한 중심 생활','인천시청과 구월동 상권의\n생활 편의시설'),
        ('05','다양한 주택형','전용 46㎡부터 84㎡까지\n여러 주택형 구성'),
        ('06','한신더휴 브랜드','한신공영이 시공한\n인천시청역 한신더휴')]
    for idx,(num,h,desc) in enumerate(items):
        c=idx%2;r=idx//2;x=50+c*579;y=215+r*345
        d.rounded_rectangle((x,y,x+565,y+315),radius=40,fill=BLUE if c==0 else NAVY)
        d.ellipse((x+24,y+75,x+147,y+198),fill='#ffffff')
        txt(d,(x+53,y+113),num,32,NAVY,True)
        txt(d,(x+170,y+69),h,29,'white',True)
        d.line((x+170,y+125,x+500,y+125),fill='#ffffff',width=2)
        for j,line in enumerate(desc.split('\n')): txt(d,(x+170,y+153+j*41),line,22,'#eef3f7')
    footer_note(d,1286)
    im.save(ASSETS/'premium.png',optimize=True)

def brand():
    im,d=canvas(2280)
    center(d,62,'HANSHIN  THE HUE',67,NAVY,True)
    center(d,156,'생활의 새로운 쉼표, 한신더휴',37,GOLD)
    photo(im,'rendering.jpg',(50,275,1208,855))
    d.rectangle((50,716,1208,855),fill=NAVY)
    center(d,748,'인천시청역 한신더휴',47,'white',True)
    center(d,905,'469세대 · 6개동 · 인천 도심 생활권',36,INK,True)
    d.line((150,991,1108,991),fill='#aab2b8',width=2)
    copy=[('URBAN LIFE','인천시청역을 중심으로','두 지하철 노선과 도심 생활을 가까이에서'),
          ('LIVING SPACE','일상에 맞춘 다양한 공간','전용 46·52·59·74·84㎡ 주택형 구성'),
          ('THE HUE','한신공영의 주거 브랜드','인천시청역 한신더휴에서 이어지는 일상')]
    for n,(eng,h,body) in enumerate(copy):
        y=1070+n*225
        txt(d,(85,y),eng,25,GOLD,True)
        txt(d,(85,y+42),h,41,INK,True)
        txt(d,(85,y+111),body,26,MUTED)
        d.line((85,y+176,1173,y+176),fill='#d5d9dd',width=2)
    photo(im,'rendering.jpg',(85,1830,1173,2180),pos=(0.5,0.6))
    footer_note(d,2240)
    im.save(ASSETS/'brand.png',optimize=True)

def directions():
    im,d=canvas(650)
    center(d,45,'오시는 길',55,NAVY,True)
    for i,(title,address) in enumerate([('현장','인천광역시 남동구 간석동 514번지 일원'),('도로명 주소','인천광역시 남동구 석산로62번길 35')]):
        x=50+i*604
        d.rectangle((x,147,x+575,460),fill='#f6f8f9',outline='#cfd6dc',width=2)
        d.line((x+30,385,x+535,196),fill='#b7c2c9',width=14)
        d.line((x+75,218,x+500,410),fill='#d6dce0',width=13)
        d.ellipse((x+251,269,x+321,339),fill=NAVY)
        d.ellipse((x+275,292,x+297,314),fill='white')
        txt(d,(x,480),title,32,INK,True)
        txt(d,(x,532),address,23,MUTED)
    im.save(ASSETS/'directions.png',optimize=True)

if __name__=='__main__':
    for f in [overview,location,premium,brand,directions]: f()
