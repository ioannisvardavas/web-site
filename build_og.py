"""Regenerates og-image.png (social share / Viber-WhatsApp preview card).
Clean rebuild — fixes the garbled glyph line that the lost original produced.
Run:  python3 build_og.py   (outputs og-image.png in root + deploy/)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PETROL      = (15, 111, 106)
PETROL_DEEP = (10, 76, 73)
GOLD        = (182, 145, 82)
WHITE       = (255, 255, 255)
SOFT        = (224, 238, 235)

ARIAL   = '/System/Library/Fonts/Supplemental/Arial.ttf'
ARIALBD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

# --- background: vertical petrol gradient ---
img = Image.new('RGB', (W, H), PETROL)
px = img.load()
for y in range(H):
    t = y / (H - 1)
    r = round(PETROL[0] + (PETROL_DEEP[0] - PETROL[0]) * t)
    g = round(PETROL[1] + (PETROL_DEEP[1] - PETROL[1]) * t)
    b = round(PETROL[2] + (PETROL_DEEP[2] - PETROL[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)

draw = ImageDraw.Draw(img)

# left gold accent bar
draw.rectangle([0, 0, 7, H], fill=GOLD)

X0 = 72
CIRCLE_CX, CIRCLE_CY, R = 955, 250, 192
text_limit = CIRCLE_CX - R - 40  # don't collide with photo


def tracked(draw, xy, s, font, fill, tr):
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=font, fill=fill)
        bb = draw.textbbox((0, 0), ch, font=font)
        x += (bb[2] - bb[0]) + tr
    return x


def tracked_width(draw, s, font, tr):
    w = 0
    for ch in s:
        bb = draw.textbbox((0, 0), ch, font=font)
        w += (bb[2] - bb[0]) + tr
    return w - tr if s else 0

# --- eyebrow ---
eyebrow = 'FINANCIAL PLANNING   ·   BUSINESS RISK MANAGEMENT'
ef = ImageFont.truetype(ARIALBD, 21)
tracked(draw, (X0, 84), eyebrow, ef, GOLD, 2)

# --- name (auto-fit so it never reaches the photo) ---
name = 'Γιάννης Βαρδαβάς'
nsize = 78
while nsize > 40:
    nf = ImageFont.truetype(ARIALBD, nsize)
    if draw.textlength(name, font=nf) <= (text_limit - X0):
        break
    nsize -= 2
nf = ImageFont.truetype(ARIALBD, nsize)
draw.text((X0, 132), name, font=nf, fill=WHITE)

# gold underline under the name
draw.rectangle([X0, 238, X0 + 70, 242], fill=GOLD)

# --- role ---
rf = ImageFont.truetype(ARIAL, 29)
draw.text((X0, 272), 'Life, Health, P&C & Investment Architect', font=rf, fill=GOLD)

# --- subtitle (two lines) ---
sf = ImageFont.truetype(ARIAL, 27)
draw.text((X0, 344), 'Συμβουλευτική με αφετηρία τις δικές σας ανάγκες —', font=sf, fill=SOFT)
draw.text((X0, 384), 'όχι ένα έτοιμο πακέτο.', font=sf, fill=SOFT)

# --- url (single clean line, bottom) ---
uf = ImageFont.truetype(ARIAL, 25)
draw.text((X0, 560), 'vardavas.ioannis-vardavas.workers.dev', font=uf, fill=(150, 196, 190))

# --- circular photo with gold ring ---
photo = Image.open('My pro pic.png').convert('RGB')
pw, ph = photo.size
side = pw                      # full width square
top = 70                       # bias toward the head
crop = photo.crop((0, top, side, top + side))
D = R * 2
crop = crop.resize((D, D), Image.LANCZOS)
mask = Image.new('L', (D, D), 0)
ImageDraw.Draw(mask).ellipse([0, 0, D, D], fill=255)
img.paste(crop, (CIRCLE_CX - R, CIRCLE_CY - R), mask)
# gold ring
draw.ellipse([CIRCLE_CX - R, CIRCLE_CY - R, CIRCLE_CX + R, CIRCLE_CY + R],
             outline=GOLD, width=6)

img.save('og-image.png')
img.save('deploy/og-image.png')
print('OK  name size', nsize)
