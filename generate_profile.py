from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import numpy as np

ROOT = Path(__file__).parent
SRC = ROOT / "profile-photo.png"
OUT = ROOT / "profile.png"

# Terminal/profile settings
W, H = 1700, 800
COLS, ROWS = 94, 66
CYAN = (66, 245, 255)
WHITE = (245, 245, 245)
DIM = (100, 112, 122)
PINK = (255, 93, 134)
GREEN = (57, 255, 20)
RED = (255, 77, 77)

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
if not Path(MONO).exists():
    MONO = "DejaVuSansMono.ttf"

im = Image.open(SRC).convert("RGB")
w, h = im.size
im = im.crop((120, 40, 1920, 1990))

arr = np.asarray(im).astype(float)
corners = np.concatenate([
    arr[:80, :80].reshape(-1,3),
    arr[:80, -80:].reshape(-1,3),
    arr[-80:, :80].reshape(-1,3),
    arr[-80:, -80:].reshape(-1,3)
])
background = corners.mean(axis=0)

# Remove the white studio background.
distance = np.linalg.norm(arr - background, axis=2)
mask = np.clip((distance - 10) / 30, 0, 1)
mask = Image.fromarray(np.uint8(mask*255)).filter(ImageFilter.GaussianBlur(2.2))
mask = np.asarray(mask) / 255

gray = ImageOps.grayscale(im).filter(ImageFilter.GaussianBlur(.25))
g = np.asarray(gray).astype(float)

# Combine absolute darkness with local contrast.
# This gives hair/eyes dense characters and skin subtle characters.
local_blur = np.asarray(gray.filter(ImageFilter.GaussianBlur(10))).astype(float)
dark = np.clip((255-g)/180, 0, 1)
local = np.clip(np.abs(g-local_blur)/40, 0, 1)
ink = np.clip((0.68*dark + 0.32*local)**0.82, 0, 1) * mask

density = np.asarray(
    Image.fromarray(np.uint8(ink*255)).resize((COLS, ROWS), Image.Resampling.LANCZOS)
) / 255

chars = " .,:;+=*#%@"
img = Image.new("RGB", (W,H), (13,16,21))
draw = ImageDraw.Draw(img)
draw.rounded_rectangle((35,35,W-35,H-35), radius=28, fill=(0,0,0))

font = ImageFont.truetype(MONO, 11)
px, py, pw, ph = 65, 65, 650, 665
cw, ch = pw/COLS, ph/ROWS

for yy in range(ROWS):
    for xx in range(COLS):
        v = float(density[yy,xx])
        if v < .055:
            continue
        c = chars[min(len(chars)-1, int(v*(len(chars)-1)+.5))]
        brightness = .45 + .55*v
        color = tuple(int(c0*brightness) for c0 in CYAN)
        draw.text((px+xx*cw, py+yy*ch), c, font=font, fill=color)

# Terminal text
x, y = 780, 72
f20 = ImageFont.truetype(MONO, 20)
f23 = ImageFont.truetype(MONO, 23)
def T(xx, yy, s, color=WHITE, f=f20):
    draw.text((xx,yy),s,font=f,fill=color)
def row(yy, label, value):
    T(x,yy,"•",DIM); T(x+24,yy,label,CYAN); T(x+285,yy,value)

T(x,y,"Ced1e@Neural-grid",CYAN,f23)
T(x+285,y,"────────────────────────────────────")
y += 31

for a,b in [
    ("Subject:","Karhl Cedric Ampo"),
    ("Role:","BSIT Student"),
    ("Origin:","Davao City, Philippines"),
    ("Status:","Building • Learning • Shipping"),
    ("ToolChain:","Java, Python, Git, VS Code, Linux"),
]:
    row(y,a,b); y += 30

y += 14
for a,b in [
    ("Core:","Java, Python, HTML/CSS, TypeScript"),
    ("Systems:","Linux, Networking, Arduino"),
    ("Frontend:","HTML/CSS, TypeScript"),
    ("Backend:","Java, Python"),
    ("Cloud:","Learning AWS / Cloud Engineering"),
]:
    row(y,a,b); y += 30

y += 15
T(x,y,"- Contact",PINK)
T(x+145,y,"────────────────────────────────────")
y += 30
for a,b in [
    ("Grid.Mail:","karhlced.a@gmail.com"),
    ("Grid.LinkedIn:","Karhl Cedric Ampo"),
    ("Grid.Github:","Ced1e"),
    ("Grid.Web:","karhl-cedric.vercel.app"),
]:
    row(y,a,b); y += 30

y += 15
T(x,y,"- GitHub Stats",PINK)
T(x+185,y,"────────────────────────────────")
y += 30
row(y,"Repos:","16")
T(x+450,y,"{"); T(x+475,y,"Contributed:",CYAN); T(x+635,y,"—")
T(x+700,y,"}"); T(x+730,y,"|"); T(x+755,y,"Stars:",CYAN); T(x+860,y,"0")
y += 30
row(y,"Commits:","—")
T(x+450,y,"|"); T(x+475,y,"Followers:",CYAN); T(x+620,y,"5")
y += 30
row(y,"Contributions:","110 (last year)")
T(x+475,y,"("); T(x+505,y,"—++",GREEN); T(x+570,y,","); T(x+600,y,"—--",RED); T(x+665,y,")")

img.save(OUT, optimize=True)
print(f"Generated {OUT}")
