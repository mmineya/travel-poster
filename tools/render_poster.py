"""Development-only Pillow renderer; main.py has no third-party dependencies."""

from pathlib import Path
import math
import random

from PIL import Image, ImageDraw, ImageFont


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


# A warm paper border encloses a continuous image, like a screen-printed plate.
for y in range(33*S, 991*S):
    yy = y/S
    if yy < 552:
        color = blend((192, 85, 61), (241, 173, 98), (yy-33)/519)
    else:
        color = blend((32, 100, 100), (13, 49, 58), (yy-552)/439)
    d.line((33*S, y, 991*S, y), fill=color)

# Title is individually spaced and fitted to the sky, with no other lettering.
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 116*S)
title = 'PORT LUMEN'
spacing = 9*S
width = sum(font.getlength(c) for c in title) + spacing*(len(title)-1)
lettering = Image.new('RGBA', (math.ceil(width)+8, 155*S))
td = ImageDraw.Draw(lettering)
x = 0
for char in title:
    td.text((x, 0), char, font=font, fill=CREAM, stroke_width=0)
    x += font.getlength(char)+spacing
lettering = lettering.crop(lettering.getbbox())
lettering = lettering.resize((844*S, 101*S), Image.Resampling.LANCZOS)
im.paste(lettering, (90*S, 101*S), lettering)

# Wind-swept cloud bands: long, quiet shapes keep the title legible.
polygon([(34,281),(117,281),(150,265),(235,265),(262,279),(351,279),
         (380,290),(268,296),(199,288),(86,293),(34,289)], '#eeb37d')
polygon([(657,255),(717,246),(785,246),(808,232),(863,232),(891,247),
         (956,247),(990,263),(850,266),(815,259),(729,266)], '#edb17b')
polygon([(90,361),(170,355),(213,343),(283,346),(304,355),(364,359),
         (389,368),(238,371),(185,365)], '#f4c38a')
polygon([(740,335),(804,330),(827,317),(883,317),(909,328),(990,333),
         (990,343),(879,343),(850,337),(789,343)], '#efbd86')

# Low sun and distant headlands form the third stop in the composition.
ellipse((384,350,570,536), '#f7d590')
polygon([(33,468),(75,449),(105,457),(149,420),(176,434),(225,396),
         (275,436),(308,427),(359,470),(396,476),(437,498),(33,535)], '#687f76')
polygon([(33,503),(106,474),(149,483),(192,461),(228,471),(266,458),
         (320,483),(361,482),(404,510),(481,518),(33,555)], '#35646a')
polygon([(741,522),(794,500),(831,507),(875,479),(902,490),(943,468),
         (990,481),(990,563),(724,555)], '#456d6d')
line([(392,546),(645,546)], '#e8bd78', 2)
line([(445,556),(579,556)], '#a7c0a0', 1)

# The village hugs the left shore. Each roof is a separate printed shape.
polygon([(33,544),(114,528),(184,536),(267,560),(336,579),(411,605),
         (467,644),(401,682),(279,699),(142,694),(33,729)], TEAL)


def house(x, y, w, h, roof=ORANGE, wall=CREAM):
    rect((x,y-h,x+w,y), wall)
    polygon([(x-4,y-h),(x+w*.48,y-h-15),(x+w+4,y-h)], roof)
    rect((x+w*.71,y-h+5,x+w,y), '#c49a66')
    for wx in range(int(x+7), int(x+w-5), 14):
        rect((wx,y-h+10,wx+4,y-h+18), TEAL)
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
# Narrow lighthouse rays echo the diagonal coastline without overwhelming it.
polygon([(689,391),(569,372),(570,378),(689,396)], '#f6d392')
polygon([(719,391),(828,367),(825,374),(719,396)], '#f6d392')

# Currents draw the eye from the foreground toward the lighthouse and sun.
polygon([(990,700),(897,717),(838,742),(760,760),(660,770),(572,798),
         (536,826),(613,847),(726,853),(799,874),(816,902),(771,933),
         (665,958),(617,990),(469,990),(529,952),(661,919),(709,895),
         (687,879),(571,867),(484,846),(467,820),(497,792),(579,765),
         (706,748),(812,729),(901,701),(990,688)], '#237c79')
polygon([(990,713),(890,736),(802,766),(682,786),(578,815),(557,831),
         (581,842),(541,835),(535,822),(562,805),(666,776),(797,756),
         (889,728),(990,704)], '#3ba495')
polygon([(590,989),(649,955),(773,921),(799,899),(799,887),(814,904),
         (781,932),(661,966),(625,990)], '#4ba997')

# Flat wave marks vary in length and follow perspective.
for i in range(180):
    y = RNG.uniform(567,983)
    x = RNG.uniform(45,980)
    if x < 450 and y < 728:
        continue
    if 610 < x < 846 and y < 699:
        continue
    length = RNG.uniform(6,29)*(0.35+(y-560)/460)
    line([(x,y),(min(x+length,987),y-0.9)],
         RNG.choice(['#307477','#2a696d','#427e7b']), RNG.choice([0.7,1,1.4]))

# Bioluminescent flecks cluster along the curved tidal channel.
for i in range(700):
    t = RNG.random()
    y = 722+270*t
    center = (925-1120*t) if t < .34 else (558+170*math.sin((t-.34)*6.0))
    x = RNG.gauss(center, 15+29*t)
    if not 42 < x < 983:
        continue
    r = RNG.uniform(.4,1.3)*(0.6+t)
    color = RNG.choice([GOLD, '#8cd0b0', '#62bfa8', '#b9d5ad'])
    ellipse((x-r,y-r*.55,x+r,y+r*.55),color)
for x,y in [(584,818),(751,897),(867,746),(636,963),(792,767),(548,846)]:
    line([(x-3,y),(x+3,y)],CREAM,0.9)
    line([(x,y-3),(x,y+3)],CREAM,0.9)

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
        shade = 1-0.065*min(1,radius)
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
# An adaptive print palette keeps the detailed PNG comfortably under 1 MiB.
im = im.quantize(colors=192, method=Image.Quantize.MEDIANCUT,
                 dither=Image.Dither.NONE)
output = Path(__file__).resolve().parents[1] / 'entry.png'
im.save(output,optimize=True)
print(f'{output}: {output.stat().st_size} bytes')
