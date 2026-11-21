"""Development-only Pillow renderer; main.py has no third-party dependencies."""

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


S = 2
SIZE = 1024
RNG = random.Random(1957)
CREAM = '#f6e6bb'
GOLD = '#e8b75d'
ORANGE = '#d56b42'
TEAL = '#123f46'
DARK = '#102f36'
SEA = '#17545a'
GLOW = '#51b4a0'
im = Image.new('RGB', (SIZE*S, SIZE*S), CREAM)
d = ImageDraw.Draw(im)


def polygon(points, fill):
    d.polygon([(round(x*S), round(y*S)) for x, y in points], fill=fill)


def line(points, fill, width=1):
    d.line([(round(x*S), round(y*S)) for x, y in points], fill=fill,
           width=max(1, round(width*S)), joint='curve')


def ellipse(box, fill):
    d.ellipse(tuple(round(v*S) for v in box), fill=fill)


def rect(box, fill):
    d.rectangle(tuple(round(v*S) for v in box), fill=fill)


def blend(a, b, t):
    return tuple(round(x+(y-x)*t) for x, y in zip(a, b))


def composite(layer, blur=0):
    global im, d
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(blur*S))
    im = Image.alpha_composite(im.convert('RGBA'), layer).convert('RGB')
    d = ImageDraw.Draw(im)


def haze(box, color, opacity, blur):
    layer = Image.new('RGBA', im.size)
    ImageDraw.Draw(layer).ellipse(tuple(round(v*S) for v in box),
                                  fill=(*color, opacity))
    composite(layer, blur)


# Five dusk pigments merge into a broad radial sun halo. Sea color shifts
# from brass on the horizon to midnight teal in the near water.
stops = [(0,(39,35,69)),(190,(86,44,85)),(315,(159,64,99)),
         (425,(222,111,79)),(552,(247,192,111)),(660,(29,91,92)),
         (1024,(9,37,49))]
field = Image.new('RGB',(512,512))
px = field.load()
for yy in range(512):
    y = yy*2
    for j in range(len(stops)-1):
        a, ca = stops[j]
        b, cb = stops[j+1]
        if a <= y <= b:
            base = blend(ca, cb, (y-a)/(b-a))
            break
    for xx in range(512):
        x = xx*2
        if y < 552:
            strength = .44*math.exp(-(((x-477)/235)**2+((y-446)/181)**2))
            color = blend(base,(255,210,143),strength)
        else:
            strength = .70*math.exp(-(((x-479)/(52+(y-552)*.20))**2+((y-552)/176)**2))
            color = blend(base,(232,173,92),strength)
        px[xx,yy] = color
im = field.resize(im.size,Image.Resampling.BICUBIC)
d = ImageDraw.Draw(im)
haze((266,266,684,640),(255,198,123),44,65)

# Title is individually spaced and fitted to the sky, with no other lettering.
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 116*S)
title = 'PORT LUMEN'
spacing = 14*S
width = sum(font.getlength(c) for c in title) + spacing*(len(title)-1)
lettering = Image.new('RGBA', (math.ceil(width)+8, 155*S))
td = ImageDraw.Draw(lettering)
x = 0
for char in title:
    td.text((x, 0), char, font=font, fill=CREAM, stroke_width=0)
    x += font.getlength(char)+spacing
lettering = lettering.crop(lettering.getbbox())
lettering = lettering.resize((844*S, 101*S), Image.Resampling.LANCZOS)
shadow = Image.new('RGBA',im.size)
shadow_text = Image.new('RGBA',lettering.size,(10,23,39,0))
shadow_text.putalpha(lettering.getchannel('A').point(lambda a: a*95//255))
shadow.paste(shadow_text,(92*S,105*S),shadow_text)
composite(shadow,3)
im.paste(lettering, (90*S, 101*S), lettering)
line([(94,225),(930,225)], '#d9ae6a', 1)

# Sculpted cloud banks have plum shadows, rose mids, and incandescent rims.
polygon([(33,276),(86,267),(117,246),(173,244),(204,260),(245,255),
         (280,272),(327,279),(370,301),(291,312),(203,304),(115,313),(33,300)], '#74435d')
polygon([(33,285),(115,287),(173,278),(223,286),(280,283),(326,297),
         (370,301),(291,309),(202,300),(116,309),(33,296)], '#bb6b80')
line([(34,300),(116,311),(202,302),(291,311),(370,302)], '#f0ae8b',2)
polygon([(615,293),(681,279),(726,253),(779,250),(807,270),(852,261),
         (890,280),(946,277),(991,297),(991,327),(910,316),(835,327),
         (756,309),(680,317)], '#78445f')
polygon([(615,293),(696,298),(756,289),(808,300),(869,294),(924,306),
         (991,309),(991,327),(909,315),(835,325),(756,307),(680,315)], '#c97789')
line([(617,295),(680,316),(756,309),(835,327),(910,317),(990,328)], '#ffc18e',2.2)
polygon([(79,367),(140,360),(184,340),(228,343),(249,354),(303,352),
         (348,369),(386,375),(309,382),(249,374),(175,381)], '#b77185')
line([(81,368),(175,381),(249,375),(309,383),(386,376)], '#ffd099',2)
polygon([(775,399),(826,387),(867,368),(905,369),(938,385),(991,390),
         (991,407),(912,400),(847,409)], '#bc7887')
line([(779,401),(847,409),(912,402),(990,408)], '#f4bd92',1.6)

# Low sun and distant headlands form the third stop in the composition.
ellipse((384,350,570,536), '#f7d590')
haze((386,352,568,534),(255,229,164),85,23)
polygon([(33,479),(119,443),(176,453),(234,421),(291,447),
         (344,437),(414,479),(487,510),(33,542)], '#c3a49a')
haze((-40,474,615,555),(250,190,142),67,17)
polygon([(33,468),(75,449),(105,457),(149,420),(176,434),(225,396),
         (275,436),(308,427),(359,470),(396,476),(437,498),(33,535)], '#8d9291')
haze((-80,501,490,549),(246,190,147),64,12)
polygon([(33,503),(106,474),(149,483),(192,461),(228,471),(266,458),
         (320,483),(361,482),(404,510),(481,518),(33,555)], '#35646a')
polygon([(741,522),(794,500),(831,507),(875,479),(902,490),(943,468),
         (990,481),(990,563),(724,555)], '#728b90')
haze((729,529,1136,579),(235,188,151),65,12)
line([(392,546),(645,546)], '#e8bd78', 2)
line([(445,556),(579,556)], '#a7c0a0', 1)

# Hundreds of broken highlights widen with perspective into a glitter path.
for _ in range(1600):
    y = RNG.uniform(551,933)
    t = (y-551)/382
    x = RNG.gauss(477+12*math.sin(t*8),14+87*t)
    if x < 450 and y < 725:
        continue
    length = RNG.uniform(1,8)*(0.25+1.5*t)
    col = RNG.choice(['#f3c47f','#e0ad68','#ad975e','#ffe4a4','#7a987c'])
    line([(x,y),(x+length,y)],col,RNG.uniform(.35,1.2))

# The village hugs the left shore. Each roof is a separate printed shape.
polygon([(33,544),(114,528),(184,536),(267,560),(336,579),(411,605),
         (467,644),(401,682),(279,699),(142,694),(33,729)], TEAL)


def house(x, y, w, h, roof='#a95549', wall='#c4b698'):
    rect((x,y-h,x+w,y), wall)
    polygon([(x-4,y-h),(x+w*.48,y-h-15),(x+w+4,y-h)], roof)
    rect((x+w*.71,y-h+5,x+w,y), '#7d857c')
    line([(x-3,y-h),(x+w*.48,y-h-15)],'#efbd80',1)
    line([(x+2,y-h+2),(x+w-2,y-h+2)],'#e5d2a5',1)
    for wx in range(int(x+7), int(x+w-5), 14):
        rect((wx-1,y-h+9,wx+5,y-h+19), DARK)
        rect((wx,y-h+10,wx+4,y-h+18), '#ffd186')
        line([(wx-1,y-h+19),(wx+5,y-h+19)],'#edd29a',.7)
        if h > 43:
            rect((wx,y-h+28,wx+4,y-h+33),'#edaf68')
    if h > 39:
        rect((x+w*.36,y-18,x+w*.36+8,y), TEAL)


for args in [(42,565,46,43),(93,563,39,55),(143,573,51,39),
             (202,588,42,43),(250,604,49,48),(306,621,43,38),
             (64,610,56,41),(126,627,48,55),(181,639,61,37),
             (251,658,55,39),(319,665,38,30),(43,654,47,30)]:
    house(*args)
# A modest clockless bell tower adds a distinctive village silhouette.
rect((158,497,177,558), CREAM)
polygon([(153,497),(168,473),(183,497)], ORANGE)
rect((164,505,171,519), TEAL)
line([(168,472),(168,463)], TEAL, 2)

# Quay and piles cast deliberate diagonal accents across the bay.
polygon([(33,682),(210,681),(388,653),(430,663),(227,702),(33,704)], '#b98653')
polygon([(33,704),(227,702),(430,663),(430,671),(229,713),(33,716)], DARK)
for xx, yy in [(244,703),(285,695),(326,687),(368,679),(414,670)]:
    line([(xx,yy),(xx,yy+23)], DARK, 4)
polygon([(316,663),(452,704),(441,711),(306,672)], GOLD)
line([(446,710),(446,732)], DARK, 3)

# Lighthouse on a rocky spur: warm face, deep teal shadow, brass lantern.
polygon([(651,633),(681,607),(732,609),(755,628),(789,641),(824,664),
         (762,683),(669,679),(616,667)], '#ad8656')
polygon([(616,667),(692,651),(746,660),(789,641),(824,664),(849,681),
         (779,700),(693,693),(629,681)], DARK)
polygon([(674,634),(688,425),(716,425),(733,634)], CREAM)
polygon([(705,428),(716,425),(733,634),(711,634)], '#c8ac79')
polygon([(684,483),(720,483),(722,509),(682,509)], ORANGE)
rect((683,409,722,426), DARK)
rect((690,381,716,409), GOLD)
rect((700,381,705,410), CREAM)
rect((688,383,691,410), DARK)
rect((715,383,718,410), DARK)
polygon([(681,381),(702,363),(725,381)], DARK)
ellipse((700,357,705,363), GOLD)
line([(678,414),(727,414)], DARK, 3)
for xx in [681,692,714,725]:
    line([(xx,402),(xx,417)], DARK, 1.6)
rect((696,548,703,566), TEAL)
rect((696,597,708,634), TEAL)
# Light passes through airborne salt: broad transparent beams with soft edges.
beam = Image.new('RGBA',im.size)
bd = ImageDraw.Draw(beam)
bd.polygon([(719*S,391*S),(990*S,307*S),(990*S,418*S)], fill=(255,223,161,64))
bd.polygon([(689*S,391*S),(355*S,336*S),(355*S,420*S)], fill=(255,220,156,43))
composite(beam,6)
haze((677,371,728,417),(255,206,108),110,14)
rect((696,548,703,564),'#f5c37b')
for y in range(447,625,21):
    line([(710,y),(719+(y-447)*.06,y)],'#b5a27e',.65)
line([(681,632),(687,542),(691,433)],'#fff0c8',1)

# Wide translucent phosphorescence replaces the hard ribbon of the first pass.
def current(t):
    return (795-144*math.sin(t*6.2)-145*t, 709+300*t)

for width, alpha, blur in [(110,28,28),(54,35,13),(18,31,6)]:
    layer = Image.new('RGBA',im.size)
    ld = ImageDraw.Draw(layer)
    points = [(round(x*S),round(y*S)) for x,y in
              (current(i/220) for i in range(221))]
    ld.line(points,fill=(63,204,182,alpha),width=width*S,joint='curve')
    composite(layer,blur)

# Flat wave marks vary in length and follow perspective.
for i in range(600):
    y = RNG.uniform(567,983)
    x = RNG.uniform(45,980)
    if x < 450 and y < 728:
        continue
    if 610 < x < 846 and y < 699:
        continue
    length = RNG.uniform(6,29)*(0.35+(y-560)/460)
    line([(x,y),(min(x+length,987),y-0.9)],
         RNG.choice(['#286269','#245860','#397573']), RNG.choice([0.5,.7,1]))

# Bioluminescent flecks cluster along the curved tidal channel.
for i in range(2200):
    t = RNG.random()
    center,y = current(t)
    x = RNG.gauss(center, 23+40*t)
    if not 42 < x < 983:
        continue
    r = RNG.uniform(.25,.85)*(0.6+t)
    color = RNG.choice(['#a3d7b2','#62bba7','#398e89','#4eaa9d','#78b9a4'])
    ellipse((x-r,y-r*.55,x+r,y+r*.55),color)
for x,y in [(643,818),(751,897),(779,746),(636,963),(692,767),(648,846)]:
    line([(x-3,y),(x+3,y)],CREAM,0.9)
    line([(x,y-3),(x,y+3)],CREAM,0.9)

# Quayside lamps and reflected amber pinpoints make the town feel inhabited.
for x,y in [(83,681),(161,681),(246,678),(320,665),(389,661),(446,703)]:
    line([(x,y),(x,y-15)],DARK,1)
    haze((x-6,y-22,x+6,y-9),(255,179,78),110,5)
    ellipse((x-1.6,y-17,x+1.6,y-14),'#ffe7af')
    for j in range(8):
        yy = y+19+j*3.7
        xx = x+RNG.uniform(-5,5)
        line([(xx,yy),(xx+RNG.uniform(2,6),yy)],'#b28c54',.7)

# Salt haze joins the sun, water and distant architecture with a soft warm veil.
haze((340,488,635,610),(255,206,148),30,30)

# Small sailing boat provides a human scale and a quiet cream counterpoint.
polygon([(490,698),(529,698),(520,706),(497,706)], DARK)
line([(511,651),(511,699)], CREAM, 1.5)
polygon([(507,656),(484,691),(507,691)], CREAM)
polygon([(515,665),(515,691),(532,691)], '#d4ad69')
line([(495,714),(524,714)], '#45908a', 1.5)

# Foreground promontory and botanical cutouts frame the luminous water.
polygon([(33,790),(82,799),(122,825),(168,843),(190,875),(241,898),
         (264,925),(314,954),(364,991),(33,991)], DARK)
polygon([(33,832),(109,848),(153,876),(198,912),(225,955),(266,991),
         (33,991)], '#19454a')
for x,y,h in [(70,896,100),(118,949,105),(194,984,79),(51,977,80)]:
    line([(x,y),(x+2,y-h)], DARK, 4)
    for direction in [-1,1]:
        for k in range(4):
            yy = y-h+12+k*17
            polygon([(x,yy+22),(x+direction*(24+k*4),yy-7),
                     (x+direction*9,yy+29),(x,yy+37)], DARK)

# Restrained deterministic film grain, computed at the oversampled resolution.
pixels = bytearray(im.tobytes())
for y in range(33*S,991*S):
    for x in range(33*S,991*S):
        i = (y*SIZE*S+x)*3
        grain = RNG.choice([-3,-2,-1,0,0,0,1,2,3])
        radius = ((x/S-512)/680)**2+((y/S-512)/680)**2
        shade = 1-0.12*min(1,radius)
        for c in range(3):
            pixels[i+c] = max(0,min(255,round(pixels[i+c]*shade)+grain))
im = Image.frombytes('RGB',im.size,bytes(pixels))
# Trim botanical silhouettes to the same print plate as the rest of the scene.
d = ImageDraw.Draw(im)
rect((0,0,1024,32.5), CREAM)
rect((0,991.5,1024,1024), CREAM)
rect((0,0,32.5,1024), CREAM)
rect((991.5,0,1024,1024), CREAM)
im = im.resize((SIZE,SIZE),Image.Resampling.LANCZOS)
# Preserve continuous-color dusk and light scattering in the shipped PNG.
output = Path(__file__).resolve().parents[1] / 'entry.png'
im.save(output,optimize=True,compress_level=9)
assert output.stat().st_size <= 1024*1024, 'Poster exceeds the 1 MiB limit'
print(f'{output}: {output.stat().st_size} bytes')
