#!/usr/bin/env python3
"""
Generate all textures for "Steal an AI" using Pillow.
Run: python generate_textures.py
Outputs to ./textures/
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math
import random

OUT = Path("textures")
OUT.mkdir(exist_ok=True)

# ===== Color Palette =====
BG_DARK = (13, 17, 23)
BG_ELEV = (22, 27, 34)
BORDER = (48, 54, 61)
TEXT = (230, 237, 243)
TEXT_MUTED = (139, 148, 158)

GPU_ORANGE = (255, 107, 53)
CPU_TEAL = (0, 212, 170)
RAM_PURPLE = (168, 85, 247)
GOLD = (255, 215, 0)

TIER_COLORS = {
    "common":  (107, 114, 128),
    "rare":    (59, 130, 246),
    "epic":    (168, 85, 247),
    "legendary": (245, 158, 11),
}

TIER_GLOWS = {
    "common":  (107, 114, 128, 80),
    "rare":    (59, 130, 246, 120),
    "epic":    (168, 85, 247, 160),
    "legendary": (245, 158, 11, 200),
}

# ===== Helpers =====
def new_img(w, h, bg=BG_DARK):
    return Image.new("RGBA", (w, h), bg)

def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def glow_layer(size, color, radius_frac=0.4, intensity=1.0):
    """Radial gradient glow."""
    w, h = size
    img = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    max_r = min(w, h) * radius_frac
    for r in range(int(max_r), 0, -1):
        alpha = int((1 - r/max_r) * 255 * intensity)
        draw.ellipse([w//2-r, h//2-r, w//2+r, h//2+r], fill=(*color[:3], alpha))
    return img.filter(ImageFilter.GaussianBlur(4))

def add_glow(base, glow_color, radius_frac=0.5, intensity=1.0):
    glow = glow_layer(base.size, glow_color, radius_frac, intensity)
    return Image.alpha_composite(glow, base)

def save(img, name):
    img.save(OUT / f"{name}.png")
    print(f"  ✓ {name}.png")

# ===== 1. Model Sprites (128x128) =====
MODEL_DEFS = [
    # Common
    ("nemotron-3b", "common", "N3B", "🤖"),
    ("phi-3-mini", "common", "Φ3", "🔮"),
    ("gemma-2b", "common", "G2", "💎"),
    ("qwen-1_5b", "common", "Q1.5", "🐉"),
    ("smollm-1_7b", "common", "SMOL", "🍪"),
    # Rare
    ("nemotron-7b", "rare", "N7B", "🦾"),
    ("llama-3-8b", "rare", "L8B", "🦙"),
    ("phi-3-medium", "rare", "Φ3M", "🧙"),
    ("qwen-2-7b", "rare", "Q2-7", "🀄"),
    ("mistral-7b", "rare", "M7B", "🌬️"),
    # Epic
    ("nemotron-ultra", "epic", "N-ULT", "👑"),
    ("llama-3-70b", "epic", "L70B", "🦙🦙"),
    ("command-r-plus", "epic", "CMD-R+", "⚡"),
    ("qwen-2-72b", "epic", "Q2-72", "🐲"),
    ("yi-34b", "epic", "YI34", "🎋"),
    # Legendary
    ("gpt-4o-mini", "legendary", "4o-M", "✨"),
    ("claude-3_5-sonnet", "legendary", "C3.5S", "🎭"),
    ("gemini-1_5-pro", "legendary", "G1.5P", "♊"),
    # OG Legends
    ("gpt-1o", "legendary", "GPT-1o", "🌟"),
    ("claude-fable-5", "legendary", "FABLE5", "📖"),
    ("opus-5", "legendary", "OPUS5", "🎼"),
]

def make_model_sprite(model_id, tier, label, emoji_char, size=128):
    img = new_img(size, size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = size//2, size//2
    r = size//2 - 4
    
    tier_rgb = TIER_COLORS[tier]
    tier_glow = TIER_GLOWS[tier]
    
    # Outer glow
    glow = glow_layer((size, size), tier_glow, 0.48, 0.8)
    img = Image.alpha_composite(glow, img)
    draw = ImageDraw.Draw(img)
    
    # Main circle background
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BG_ELEV, outline=tier_rgb, width=3)
    
    # Inner accent ring
    draw.ellipse([cx-r+6, cy-r+6, cx+r-6, cy+r-6], outline=(*tier_rgb, 100), width=2)
    
    # Tier-specific pattern
    if tier == "common":
        # Circuit lines
        for i in range(6):
            angle = i * math.pi / 3
            x1 = cx + int((r-20) * math.cos(angle))
            y1 = cy + int((r-20) * math.sin(angle))
            x2 = cx + int((r-8) * math.cos(angle))
            y2 = cy + int((r-8) * math.sin(angle))
            draw.line([x1, y1, x2, y2], fill=(*tier_rgb, 180), width=2)
            # Small nodes
            draw.ellipse([x2-3, y2-3, x2+3, y2+3], fill=tier_rgb)
    
    elif tier == "rare":
        # Hexagon mesh
        for ring in [r-15, r-30, r-45]:
            for i in range(6):
                angle = i * math.pi / 3
                x = cx + int(ring * math.cos(angle))
                y = cy + int(ring * math.sin(angle))
                draw.ellipse([x-4, y-4, x+4, y+4], fill=(*tier_rgb, 200))
                if i < 5:
                    nx = cx + int(ring * math.cos((i+1)*math.pi/3))
                    ny = cy + int(ring * math.sin((i+1)*math.pi/3))
                    draw.line([x, y, nx, ny], fill=(*tier_rgb, 120), width=1)
    
    elif tier == "epic":
        # Star burst
        for i in range(8):
            angle = i * math.pi / 4
            outer_r = r - 10
            inner_r = r - 35
            x1 = cx + int(outer_r * math.cos(angle))
            y1 = cy + int(outer_r * math.sin(angle))
            x2 = cx + int(inner_r * math.cos(angle))
            y2 = cy + int(inner_r * math.sin(angle))
            draw.line([cx, cy, x1, y1], fill=(*tier_rgb, 150), width=2)
            draw.line([cx, cy, x2, y2], fill=(*tier_rgb, 100), width=1)
        # Center core
        draw.ellipse([cx-12, cy-12, cx+12, cy+12], fill=tier_rgb)
    
    elif tier == "legendary":
        # Rotating squares / mandala
        for s in range(5, 0, -1):
            rot = s * 0.3
            sq_r = 15 + s * 12
            pts = []
            for corner in range(4):
                angle = rot + corner * math.pi / 2
                pts.append((cx + int(sq_r * math.cos(angle)), cy + int(sq_r * math.sin(angle))))
            draw.polygon(pts, outline=(*tier_rgb, 200 - s*30), width=2)
        # Central diamond
        draw.polygon([(cx, cy-10), (cx+10, cy), (cx, cy+10), (cx-10, cy)], fill=tier_rgb)
    
    # Label text (initials)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
    except:
        font = ImageFont.load_default()
    
    # Draw label with outline
    bbox = draw.textbbox((0,0), label, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    tx, ty = cx - tw//2, cy - th//2 + 2
    # Outline
    for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1),(-2,0),(2,0),(0,-2),(0,2)]:
        draw.text((tx+dx, ty+dy), label, font=font, fill=(0,0,0,200))
    draw.text((tx, ty), label, font=font, fill=TEXT)
    
    # Tier badge at bottom
    badge_r = 16
    by = cy + r - badge_r - 4
    draw.ellipse([cx-badge_r, by-badge_r, cx+badge_r, by+badge_r], fill=tier_rgb)
    tier_short = {"common":"C","rare":"R","epic":"E","legendary":"L"}[tier]
    bfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14) if Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf").exists() else ImageFont.load_default()
    bb = draw.textbbox((0,0), tier_short, font=bfont)
    draw.text((cx-(bb[2]-bb[0])//2, by-(bb[3]-bb[1])//2), tier_short, font=bfont, fill=(0,0,0))
    
    return img

print("Generating model sprites...")
for mid, tier, label, emoji in MODEL_DEFS:
    sprite = make_model_sprite(mid, tier, label, emoji)
    save(sprite, f"model_{mid}")

# ===== 2. Carpet Texture (512x128, tileable) =====
def make_carpet(w=512, h=128):
    img = new_img(w, h, (31, 19, 16))  # Dark red base
    draw = ImageDraw.Draw(img)
    
    # Vertical gold stripes (subtle)
    for x in range(0, w, 40):
        alpha = 25 if (x//40)%2==0 else 15
        draw.line([x, 0, x, h], fill=(255, 180, 0, alpha), width=2)
    
    # Horizontal threads
    for y in range(0, h, 4):
        alpha = 20 if y%8==0 else 10
        draw.line([0, y, w, y], fill=(200, 100, 20, alpha), width=1)
    
    # Gold trim top & bottom
    for y in [0, 1, h-2, h-1]:
        draw.line([0, y, w, y], fill=(255, 200, 50, 200), width=2)
    for y in [2, h-3]:
        draw.line([0, y, w, y], fill=(200, 140, 20, 150), width=1)
    
    # Subtle pattern: repeating diamonds
    for cx in range(-20, w+20, 80):
        for cy in range(-20, h+20, 60):
            pts = [(cx, cy-8), (cx+12, cy), (cx, cy+8), (cx-12, cy)]
            draw.polygon(pts, outline=(255, 180, 0, 30))
    
    return img

print("Generating carpet...")
save(make_carpet(), "carpet")

# Carpet end caps (left/right fade)
def make_carpet_cap(side="left", w=120, h=128):
    img = new_img(w, h, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    base = make_carpet(w, h)
    # Fade to transparent
    for x in range(w):
        alpha = 255 if side=="left" else 0
        if side == "left":
            alpha = int(255 * (1 - x/w))
        else:
            alpha = int(255 * (x/w))
        for y in range(h):
            r,g,b,_ = base.getpixel((x,y))
            img.putpixel((x,y), (r,g,b,alpha))
    return img

save(make_carpet_cap("left"), "carpet_cap_left")
save(make_carpet_cap("right"), "carpet_cap_right")

# ===== 3. Currency Icons (64x64) =====
def make_currency_icon(type_, size=64):
    img = new_img(size, size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = size//2, size//2
    r = size//2 - 4
    
    if type_ == "gpu":
        # GPU: stylized graphics card
        bg_col = GPU_ORANGE
        # Main board
        draw.rounded_rectangle([cx-22, cy-16, cx+22, cy+16], radius=6, fill=(30,30,30), outline=bg_col, width=2)
        # PCIe fingers
        for i in range(5):
            y = cy - 12 + i * 6
            draw.rectangle([cx-22, y, cx-16, y+3], fill=bg_col)
        # Chip
        draw.rounded_rectangle([cx-10, cy-10, cx+10, cy+10], radius=4, fill=bg_col)
        draw.rounded_rectangle([cx-6, cy-6, cx+6, cy+6], radius=2, fill=(255,200,100))
        # Memory chips
        for x in [-20, 20]:
            draw.rounded_rectangle([x-6, cy-8, x+6, cy+8], radius=3, fill=(40,40,40), outline=bg_col, width=1)
    
    elif type_ == "cpu":
        # CPU: square with pins
        bg_col = CPU_TEAL
        draw.rounded_rectangle([cx-18, cy-18, cx+18, cy+18], radius=4, fill=(30,30,30), outline=bg_col, width=2)
        # IHS
        draw.rounded_rectangle([cx-12, cy-12, cx+12, cy+12], radius=2, fill=bg_col)
        # Heatspreader texture
        for i in range(3):
            for j in range(3):
                x = cx - 8 + i*8
                y = cy - 8 + j*8
                draw.rectangle([x, y, x+4, y+4], fill=(*bg_col, 180))
        # Pins bottom
        for i in range(8):
            x = cx - 14 + i*4
            draw.line([x, cy+14, x, cy+18], fill=bg_col, width=1)
    
    elif type_ == "ram":
        # RAM: DIMM stick
        bg_col = RAM_PURPLE
        draw.rounded_rectangle([cx-12, cy-22, cx+12, cy+22], radius=4, fill=(20,20,30), outline=bg_col, width=2)
        # Notch
        draw.rectangle([cx-2, cy-22, cx+2, cy-18], fill=(20,20,30))
        # Gold fingers
        for i in range(10):
            y = cy - 16 + i*3
            draw.line([cx-12, y, cx+12, y], fill=GOLD, width=1)
        # Chips
        for y in [-16, 0, 16]:
            draw.rounded_rectangle([cx-10, y-6, cx+10, y+6], radius=2, fill=bg_col)
            draw.line([cx-6, y, cx+6, y], fill=(200,150,255), width=1)
    
    # Glow
    return add_glow(img, (*bg_col, 255), 0.45, 0.6)

for c in ["gpu", "cpu", "ram"]:
    save(make_currency_icon(c), f"icon_{c}")

# ===== 4. UI Elements =====
# Buttons
def make_button(base_color, label, w=160, h=48, variant="normal"):
    img = new_img(w, h, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    r = 10
    
    if variant == "normal":
        bg = (*base_color, 200)
        outline = (*base_color, 255)
        text_col = TEXT
    elif variant == "outline":
        bg = (0,0,0,0)
        outline = (*base_color, 200)
        text_col = base_color
    elif variant == "prestige":
        bg = (0,0,0,0)
        outline = None
        text_col = TEXT
    
    if variant == "prestige":
        # Gradient background
        for y in range(h):
            t = y / h
            r_ = int(168 * (1-t) + 124 * t)
            g_ = int(85 * (1-t) + 58 * t)
            b_ = int(247 * (1-t) + 200 * t)
            draw.line([r, y, w-r, y], fill=(r_, g_, b_, 255))
        # Rounded corners mask
        mask = new_img(w, h, (0,0,0,0))
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([0,0,w-1,h-1], radius=r, fill=(255,255,255,255))
        img = Image.composite(img, new_img(w,h,(0,0,0,0)), mask)
        draw = ImageDraw.Draw(img)
    else:
        draw.rounded_rectangle([0,0,w-1,h-1], radius=r, fill=bg, outline=outline, width=2)
    
    # Label
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), label, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((w//2 - tw//2, h//2 - th//2), label, font=font, fill=text_col)
    
    return img

print("Generating UI buttons...")
save(make_button(GPU_ORANGE, "RECRUIT", 140, 44), "btn_recruit")
save(make_button(CPU_TEAL, "CONVERT", 140, 44), "btn_convert")
save(make_button(RAM_PURPLE, "PRESTIGE", 160, 48, "prestige"), "btn_prestige")
save(make_button(GPU_ORANGE, "FORCE SPAWN", 160, 44, "outline"), "btn_forcespawn")
save(make_button((100,100,100), "1x SPEED", 120, 44, "outline"), "btn_speed")

# Tab icons
def make_tab_icon(symbol, active=False, size=40):
    img = new_img(size, size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    col = GPU_ORANGE if active else TEXT_MUTED
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), symbol, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((size//2 - tw//2, size//2 - th//2), symbol, font=font, fill=col)
    return img

for sym, name in [("📋","collection"), ("✨","legends"), ("🔄","prestige")]:
    save(make_tab_icon(sym, False), f"tab_{name}_inactive")
    save(make_tab_icon(sym, True), f"tab_{name}_active")

# Tier badges (small)
for tier in ["common", "rare", "epic", "legendary"]:
    img = new_img(60, 24, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    col = TIER_COLORS[tier]
    draw.rounded_rectangle([0,0,59,23], radius=12, fill=(*col, 200), outline=col, width=1)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
    except:
        font = ImageFont.load_default()
    label = TIER_LABELS = {"common":"COMMON","rare":"RARE","epic":"EPIC","legendary":"LEGENDARY"}[tier]
    bbox = draw.textbbox((0,0), label, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((30-tw//2, 12-th//2), label, font=font, fill=(0,0,0))
    save(img, f"badge_{tier}")

# ===== 5. Background Patterns =====
def make_bg_pattern(w=400, h=400):
    img = new_img(w, h, BG_DARK)
    draw = ImageDraw.Draw(img)
    # Subtle grid
    for x in range(0, w, 40):
        draw.line([x,0,x,h], fill=(*BORDER, 50))
    for y in range(0, h, 40):
        draw.line([0,y,w,y], fill=(*BORDER, 50))
    # Random noise
    for _ in range(2000):
        x, y = random.randint(0,w-1), random.randint(0,h-1)
        img.putpixel((x,y), (*TEXT, random.randint(5,15)))
    return img.filter(ImageFilter.GaussianBlur(0.5))

save(make_bg_pattern(), "bg_pattern")

# ===== 6. Particle Effects =====
def make_particle(type_, size=32):
    img = new_img(size, size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = size//2, size//2
    
    if type_ == "sparkle":
        col = GOLD
        for i in range(4):
            angle = i * math.pi/2
            r = 12
            x = cx + int(r * math.cos(angle))
            y = cy + int(r * math.sin(angle))
            draw.polygon([
                (cx, cy-10), (cx+2, cy-2), (cx+10, cy), (cx+2, cy+2),
                (cx, cy+10), (cx-2, cy+2), (cx-10, cy), (cx-2, cy-2)
            ], fill=(*col, 200))
    
    elif type_ == "cpu_particle":
        col = CPU_TEAL
        draw.rounded_rectangle([cx-6, cy-6, cx+6, cy+6], radius=2, fill=col)
        for i in range(4):
            draw.line([cx-8, cy-8+i*4, cx+8, cy-8+i*4], fill=(*col, 150), width=1)
    
    elif type_ == "ram_particle":
        col = RAM_PURPLE
        draw.rectangle([cx-8, cy-10, cx+8, cy+10], fill=(30,20,40), outline=col, width=1)
        for i in range(4):
            y = cy - 6 + i*3
            draw.line([cx-6, y, cx+6, y], fill=GOLD, width=1)
    
    return img

for p in ["sparkle", "cpu_particle", "ram_particle"]:
    save(make_particle(p), f"particle_{p}")

# ===== 7. Modal / Panel Backgrounds =====
def make_panel_bg(w=400, h=300):
    img = new_img(w, h, BG_ELEV)
    draw = ImageDraw.Draw(img)
    # Subtle corner accents
    corner = 20
    for cx, cy in [(corner,corner), (w-corner,corner), (corner,h-corner), (w-corner,h-corner)]:
        draw.arc([cx-15, cy-15, cx+15, cy+15], 0, 90, fill=GPU_ORANGE, width=2)
    return img

save(make_panel_bg(), "panel_bg")

# ===== 8. Prestige Symbol =====
def make_prestige_symbol(size=128):
    img = new_img(size, size, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    cx, cy = size//2, size//2
    
    # Outer ring
    for i in range(3):
        r = 50 - i*12
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=(*RAM_PURPLE, 200-i*50), width=3)
    
    # Brain silhouette (simplified)
    # Left hemisphere
    draw.ellipse([cx-35, cy-25, cx, cy+25], fill=(*RAM_PURPLE, 180))
    # Right hemisphere
    draw.ellipse([cx, cy-25, cx+35, cy+25], fill=(*RAM_PURPLE, 180))
    # Brainstem
    draw.rectangle([cx-4, cy+15, cx+4, cy+35], fill=(*RAM_PURPLE, 180))
    
    # Neural connections
    for _ in range(12):
        x1 = cx + random.randint(-30, 30)
        y1 = cy + random.randint(-20, 20)
        x2 = cx + random.randint(-30, 30)
        y2 = cy + random.randint(-20, 20)
        draw.line([x1, y1, x2, y2], fill=(*GOLD, 150), width=1)
    
    # Center glow
    glow = glow_layer((size, size), (*RAM_PURPLE, 255), 0.3, 0.8)
    img = Image.alpha_composite(glow, img)
    
    return img

save(make_prestige_symbol(), "prestige_symbol")

# ===== 9. Notification/Toast Icons =====
for name, col, sym in [("success", CPU_TEAL, "✓"), ("error", (239,68,68), "✕"), ("info", GPU_ORANGE, "ℹ"), ("ram", RAM_PURPLE, "✦")]:
    img = new_img(40, 40, (0,0,0,0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2,2,37,37], fill=(*col, 220))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), sym, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text((20-tw//2, 20-th//2), sym, font=font, fill=(0,0,0))
    save(img, f"toast_{name}")

print(f"\nAll textures saved to {OUT}/")
print("Count:", len(list(OUT.glob("*.png"))))