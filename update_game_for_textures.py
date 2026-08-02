#!/usr/bin/env python3
"""
Patch the HTML/CSS/JS to use generated textures instead of emojis.
Run after generate_textures.py
"""
from pathlib import Path

# Read existing files
html = Path("index.html").read_text()
css = Path("style.css").read_text()
js = Path("game.js").read_text()

# ===== Update HTML: add texture preload & change sprite rendering =====
# Add preload links in head
preloads = '''
  <!-- Texture preloads -->
  <link rel="preload" as="image" href="textures/carpet.png">
  <link rel="preload" as="image" href="textures/carpet_cap_left.png">
  <link rel="preload" as="image" href="textures/carpet_cap_right.png">
  <link rel="preload" as="image" href="textures/icon_gpu.png">
  <link rel="preload" as="image" href="textures/icon_cpu.png">
  <link rel="preload" as="image" href="textures/icon_ram.png">
  <link rel="preload" as="image" href="textures/bg_pattern.png">
  <link rel="preload" as="image" href="textures/panel_bg.png">
  <link rel="preload" as="image" href="textures/prestige_symbol.png">
'''
html = html.replace('<link rel="stylesheet" href="style.css">', 
                    '<link rel="stylesheet" href="style.css">\n' + preloads)

# Replace carpet track inner HTML to use image
html = html.replace(
    '<div class="carpet-decoration"></div>',
    '''<div class="carpet-decoration"></div>
        <img class="carpet-bg" src="textures/carpet.png" alt="">
        <img class="carpet-cap-left" src="textures/carpet_cap_left.png" alt="">
        <img class="carpet-cap-right" src="textures/carpet_cap_right.png" alt="">'''
)

# Update currency icons to use images
html = html.replace(
    '''<span class="currency-icon">🎮</span>''',
    '''<img class="currency-icon" src="textures/icon_gpu.png" alt="GPU">'''
)
html = html.replace(
    '''<span class="currency-icon">🖥️</span>''',
    '''<img class="currency-icon" src="textures/icon_cpu.png" alt="CPU">'''
)
html = html.replace(
    '''<span class="currency-icon">🧠</span>''',
    '''<img class="currency-icon" src="textures/icon_ram.png" alt="RAM">'''
)

# Update tab buttons to use image icons
tab_replacements = {
    '<button class="tab-btn active" data-tab="collection">📋 Collection</button>':
    '<button class="tab-btn active" data-tab="collection"><img src="textures/tab_collection_active.png" alt=""> Collection</button>',
    '<button class="tab-btn" data-tab="legends">✨ Legends</button>':
    '<button class="tab-btn" data-tab="legends"><img src="textures/tab_legends_inactive.png" alt=""> Legends</button>',
    '<button class="tab-btn" data-tab="prestige">🔄 Prestige</button>':
    '<button class="tab-btn" data-tab="prestige"><img src="textures/tab_prestige_inactive.png" alt=""> Prestige</button>',
}
for old, new in tab_replacements.items():
    html = html.replace(old, new)

# Update modal close button
html = html.replace(
    '<button class="modal-close" id="modal-close">&times;</button>',
    '<button class="modal-close" id="modal-close"><img src="textures/toast_error.png" alt="Close" style="width:20px;height:20px;"></button>'
)

# Update prestige card to show symbol
html = html.replace(
    '<div class="prestige-card">',
    '''<div class="prestige-card">
            <img class="prestige-symbol" src="textures/prestige_symbol.png" alt="">'''
)

Path("index.html").write_text(html)
print("✓ index.html updated")

# ===== Update CSS: add texture-related styles =====
css_additions = '''

/* ===== Texture-based Elements ===== */
.carpet-track {
  position: relative;
}
.carpet-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.9;
}
.carpet-cap-left {
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 120px;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}
.carpet-cap-right {
  position: absolute;
  right: 0; top: 0; bottom: 0;
  width: 120px;
  height: 100%;
  object-fit: cover;
  pointer-events: none;
}

.currency-icon {
  width: 22px;
  height: 22px;
  image-rendering: pixelated;
}

.tab-btn img {
  width: 20px;
  height: 20px;
  vertical-align: middle;
  margin-right: 6px;
  image-rendering: pixelated;
  opacity: 0.8;
}
.tab-btn.active img {
  opacity: 1;
  filter: drop-shadow(0 0 4px var(--accent-gpu));
}

.modal-close img {
  width: 20px;
  height: 20px;
  opacity: 0.7;
}
.modal-close:hover img { opacity: 1; }

.prestige-symbol {
  width: 80px;
  height: 80px;
  margin-bottom: 12px;
  filter: drop-shadow(0 0 16px var(--accent-ram));
  animation: prestige-pulse 3s ease-in-out infinite;
}
@keyframes prestige-pulse {
  0%, 100% { transform: scale(1); filter: drop-shadow(0 0 16px var(--accent-ram)); }
  50% { transform: scale(1.05); filter: drop-shadow(0 0 24px var(--accent-ram)); }
}

/* Model sprites now use images */
.walking-model .model-sprite {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--bg-elevated);
  border: 3px solid;
  box-shadow: 0 4px 16px var(--shadow);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.walking-model .model-sprite img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  image-rendering: crisp-edges;
}

.model-card-sprite {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--bg-elevated);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border: 2px solid var(--border);
}
.model-card-sprite img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  image-rendering: crisp-edges;
}

.modal-sprite {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: var(--bg);
  border: 4px solid;
  box-shadow: 0 8px 32px var(--shadow);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.modal-sprite img {
  width: 92px;
  height: 92px;
  border-radius: 50%;
  image-rendering: crisp-edges;
}

/* Tier badges */
.tier-badge {
  display: inline-block;
  width: 50px;
  height: 20px;
  image-rendering: pixelated;
}

/* Background pattern */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url('textures/bg_pattern.png');
  background-repeat: repeat;
  opacity: 0.3;
  pointer-events: none;
  z-index: -1;
}

/* Panel backgrounds */
.base-section, .carpet-section, .modal-content {
  background-image: url('textures/panel_bg.png');
  background-size: cover;
  background-position: center;
}

/* Particle effects (for JS) */
.particle {
  position: absolute;
  pointer-events: none;
  image-rendering: pixelated;
  animation: particle-fade 0.8s ease-out forwards;
}
@keyframes particle-fade {
  0% { opacity: 1; transform: scale(1) translateY(0); }
  100% { opacity: 0; transform: scale(0.5) translateY(-40px); }
}

/* Toast icons */
.toast::before {
  content: '';
  width: 24px;
  height: 24px;
  background-size: contain;
  background-repeat: no-repeat;
  flex-shrink: 0;
}
.toast.success::before { background-image: url('textures/toast_success.png'); }
.toast.error::before   { background-image: url('textures/toast_error.png'); }
.toast.info::before    { background-image: url('textures/toast_info.png'); }
.toast.ram::before     { background-image: url('textures/toast_ram.png'); }
.toast { padding-left: 14px; }

/* Button backgrounds (optional enhancement) */
.btn-recruit { background-image: url('textures/btn_recruit.png'); background-size: cover; border: none; }
.btn-convert { background-image: url('textures/btn_convert.png'); background-size: cover; border: none; }
.btn-prestige { background-image: url('textures/btn_prestige.png'); background-size: cover; border: none; }
.btn-forcespawn { background-image: url('textures/btn_forcespawn.png'); background-size: cover; border: none; }
.btn-speed { background-image: url('textures/btn_speed.png'); background-size: cover; border: none; }
'''

css += css_additions
Path("style.css").write_text(css)
print("✓ style.css updated")

# ===== Update JS: use texture images for model sprites =====
# Add texture mapping to MODEL_DEFS
js = js.replace(
    'const MODEL_DEFS = [',
    '''// Texture mapping
const MODEL_TEXTURES = {};
MODEL_DEFS.forEach(m => {
  MODEL_TEXTURES[m.id] = `textures/model_${m.id}.png`;
});
LEGEND_DEFS.forEach(m => {
  MODEL_TEXTURES[m.id] = `textures/model_${m.id}.png`;
});

const MODEL_DEFS = ['''
)

# Update spawnWalkingModel to use image sprites
old_spawn = '''  const el = document.createElement('div');
  el.className = 'walking-model';
  el.dataset.modelId = modelDef.id;
  
  const sprite = document.createElement('div');
  sprite.className = 'model-sprite';
  sprite.style.borderColor = TIER_COLORS[modelDef.tier].main;
  sprite.textContent = modelDef.emoji;'''

new_spawn = '''  const el = document.createElement('div');
  el.className = 'walking-model';
  el.dataset.modelId = modelDef.id;
  
  const sprite = document.createElement('div');
  sprite.className = 'model-sprite';
  sprite.style.borderColor = TIER_COLORS[modelDef.tier].main;
  const img = document.createElement('img');
  img.src = MODEL_TEXTURES[modelDef.id] || `textures/model_${modelDef.id}.png`;
  img.alt = modelDef.name;
  img.loading = 'lazy';
  sprite.appendChild(img);'''

js = js.replace(old_spawn, new_spawn)

# Update renderModelGrid to use images
old_grid_sprite = '''    const sprite = document.createElement('div');
    sprite.className = 'model-card-sprite';
    sprite.textContent = def.emoji;'''

new_grid_sprite = '''    const sprite = document.createElement('div');
    sprite.className = 'model-card-sprite';
    const img = document.createElement('img');
    img.src = MODEL_TEXTURES[def.id] || `textures/model_${def.id}.png`;
    img.alt = def.name;
    img.loading = 'lazy';
    sprite.appendChild(img);'''

js = js.replace(old_grid_sprite, new_grid_sprite)

# Update renderLegendGrid similarly
old_legend_sprite = '''    const sprite = document.createElement('div');
    sprite.className = 'model-card-sprite';
    sprite.textContent = def.emoji;'''

new_legend_sprite = '''    const sprite = document.createElement('div');
    sprite.className = 'model-card-sprite';
    const img = document.createElement('img');
    img.src = MODEL_TEXTURES[def.id] || `textures/model_${def.id}.png`;
    img.alt = def.name;
    img.loading = 'lazy';
    sprite.appendChild(img);'''

js = js.replace(old_legend_sprite, new_legend_sprite)

# Update openModal to use image
old_modal_sprite = '''  document.getElementById('modal-sprite').textContent = def.emoji;
  document.getElementById('modal-sprite').style.borderColor = colors.main;'''

new_modal_sprite = '''  const modalSprite = document.getElementById('modal-sprite');
  modalSprite.innerHTML = '';
  const img = document.createElement('img');
  img.src = MODEL_TEXTURES[def.id] || `textures/model_${def.id}.png`;
  img.alt = def.name;
  modalSprite.appendChild(img);
  modalSprite.style.borderColor = colors.main;'''

js = js.replace(old_modal_sprite, new_modal_sprite)

# Add particle effect function
particle_js = '''

// ===== Particle Effects =====
function spawnParticles(x, y, type, count = 8) {
  const container = document.getElementById('carpet-track');
  const rect = container.getBoundingClientRect();
  const textures = {
    sparkle: 'textures/particle_sparkle.png',
    cpu_particle: 'textures/particle_cpu_particle.png',
    ram_particle: 'textures/particle_ram_particle.png',
  };
  const tex = textures[type] || textures.sparkle;
  
  for (let i = 0; i < count; i++) {
    const p = document.createElement('img');
    p.className = 'particle';
    p.src = tex;
    p.style.left = (x - rect.left + (Math.random()-0.5)*30) + 'px';
    p.style.top = (y - rect.top + (Math.random()-0.5)*30) + 'px';
    p.style.width = '24px';
    p.style.height = '24px';
    p.style.setProperty('--delay', `${Math.random()*0.2}s`);
    container.appendChild(p);
    setTimeout(() => p.remove(), 800);
  }
}'''

js = js.replace('// ===== GAME LOOP =====', particle_js + '\n// ===== GAME LOOP =====')

# Trigger particles on recruit
js = js.replace(
    'showToast(`Recruited ${modelDef.name}!`, \'success\');',
    '''showToast(`Recruited ${modelDef.name}!`, 'success');
  const rect = walkData.element.getBoundingClientRect();
  const trackRect = els.carpetTrack.getBoundingClientRect();
  spawnParticles(rect.left + 36, rect.top + 36, 'sparkle', 12);'''
)

# Trigger particles on prestige
js = js.replace(
    'showToast(`Prestige ${state.prestigeLevel} reached! Gained ${formatNum(ramGain)} RAM Coins!`, \'ram\');',
    '''showToast(`Prestige ${state.prestigeLevel} reached! Gained ${formatNum(ramGain)} RAM Coins!`, 'ram');
  const prestigeBtn = els.prestigeBtn;
  const rect = prestigeBtn.getBoundingClientRect();
  spawnParticles(rect.left + rect.width/2, rect.top + rect.height/2, 'ram_particle', 20);'''
)

# Trigger particles on convert
js = js.replace(
    'showToast(`Converted ${formatNum(amount * rate)} CPU → ${formatNum(amount)} GPU`, \'success\');',
    '''showToast(`Converted ${formatNum(amount * rate)} CPU → ${formatNum(amount)} GPU`, 'success');
  const convertBtn = els.convertBtn;
  const rect = convertBtn.getBoundingClientRect();
  spawnParticles(rect.left + rect.width/2, rect.top + rect.height/2, 'cpu_particle', 10);'''
)

Path("game.js").write_text(js)
print("✓ game.js updated")

print("\nAll files updated! Run the game by opening index.html")