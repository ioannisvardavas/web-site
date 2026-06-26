from PIL import Image, ImageDraw, ImageFont
import numpy as np

SRC = 'My_Logo_5 (1).png'
PETROL = (15, 111, 106)   # #0f6f6a
INK     = (23, 32, 31)    # #17201f
PAPER   = (251, 250, 247) # #fbfaf7

orig = Image.open(SRC).convert('L')
g = np.asarray(orig).astype(float)
h, w = g.shape

# Alpha mask from luminance: dark textured bg -> 0, white strokes -> 1
a = np.clip((g - 55) / (255 - 55), 0, 1)

# Keep only signature + underline (everything above the old subtitle, y<470)
a[470:, :] = 0.0

def composite(bg_rgb, color, alpha):
    bg = np.zeros((h, w, 3), float)
    bg[:] = bg_rgb
    col = np.zeros((h, w, 3), float)
    col[:] = color
    al = alpha[:, :, None]
    return bg * (1 - al) + col * al

out = composite(PAPER, PETROL, a)
img = Image.fromarray(out.astype('uint8'), 'RGB')

# --- New subtitle ---
TEXT = 'Life, Health, P&C & Investment Architect'
# target span matches underline: x 118..1014, center ~566
cx = (118 + 1014) // 2
target_w = 1014 - 118
tracking = 4  # px between glyphs

def text_width(font, s, tr):
    d = ImageDraw.Draw(img)
    wsum = 0
    for ch in s:
        bb = d.textbbox((0, 0), ch, font=font)
        wsum += (bb[2] - bb[0]) + tr
    return wsum - tr

# find font size so text fits target width
size = 10
font = None
for s in range(10, 80):
    f = ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc', s)
    if text_width(f, TEXT, tracking) <= target_w:
        size, font = s, f
    else:
        break

draw = ImageDraw.Draw(img)
tw = text_width(font, TEXT, tracking)
x = cx - tw // 2
y = 487  # align with old subtitle band top
for ch in TEXT:
    draw.text((x, y), ch, font=font, fill=INK)
    bb = draw.textbbox((0, 0), ch, font=font)
    x += (bb[2] - bb[0]) + tracking

img.save('logo_site.png')

# Transparent version (petrol signature + ink subtitle, no bg)
rgba = Image.new('RGBA', (w, h), (0, 0, 0, 0))
# signature/underline -> petrol with alpha a
sig_alpha = (a * 255).astype('uint8')
sig = Image.new('RGBA', (w, h), PETROL + (0,))
sig.putalpha(Image.fromarray(sig_alpha, 'L'))
rgba = Image.alpha_composite(rgba, sig)
# subtitle text on transparent
sub = Image.new('RGBA', (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(sub)
x = cx - tw // 2
for ch in TEXT:
    sd.text((x, y), ch, font=font, fill=INK + (255,))
    bb = sd.textbbox((0, 0), ch, font=font)
    x += (bb[2] - bb[0]) + tracking
rgba = Image.alpha_composite(rgba, sub)
rgba.save('logo_site_transparent.png')
print('OK size', size)
