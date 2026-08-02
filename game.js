// ===== GAME DATA =====
const MODEL_DEFS = [
  // Common Tier
  { id: 'nemotron-3b', name: 'Nemotron 3B', tier: 'common', emoji: '🤖', baseCost: 10, cpuPerSec: 0.5, desc: 'NVIDIA\'s compact workhorse. Efficient, reliable, gets the job done.' },
  { id: 'phi-3-mini', name: 'Phi-3 Mini', tier: 'common', emoji: '🔮', baseCost: 15, cpuPerSec: 0.7, desc: 'Microsoft\'s tiny but mighty. Punches above its weight class.' },
  { id: 'gemma-2b', name: 'Gemma 2B', tier: 'common', emoji: '💎', baseCost: 12, cpuPerSec: 0.6, desc: 'Google\'s open gem. Lightweight and surprisingly sharp.' },
  { id: 'qwen-1.5b', name: 'Qwen 1.5B', tier: 'common', emoji: '🐉', baseCost: 14, cpuPerSec: 0.65, desc: 'Alibaba\'s bilingual prodigy. Fluent in code and conversation.' },
  { id: 'smollm-1.7b', name: 'SmolLM 1.7B', tier: 'common', emoji: '🍪', baseCost: 11, cpuPerSec: 0.55, desc: 'HuggingFace\'s cookie-sized model. Smol but mighty.' },

  // Rare Tier
  { id: 'nemotron-7b', name: 'Nemotron 7B', tier: 'rare', emoji: '🦾', baseCost: 60, cpuPerSec: 3, desc: 'Bigger muscles, same NVIDIA DNA. Handles complex reasoning with ease.' },
  { id: 'llama-3-8b', name: 'Llama 3 8B', tier: 'rare', emoji: '🦙', baseCost: 75, cpuPerSec: 3.5, desc: 'Meta\'s open champion. The community\'s favorite workhorse.' },
  { id: 'phi-3-medium', name: 'Phi-3 Medium', tier: 'rare', emoji: '🧙', baseCost: 85, cpuPerSec: 4, desc: '14B parameters of distilled wisdom. Microsoft\'s secret sauce.' },
  { id: 'qwen-2-7b', name: 'Qwen 2 7B', tier: 'rare', emoji: '🀄', baseCost: 70, cpuPerSec: 3.2, desc: 'Multilingual maestro. Speaks 27 languages natively.' },
  { id: 'mistral-7b', name: 'Mistral 7B v0.3', tier: 'rare', emoji: '🌬️', baseCost: 80, cpuPerSec: 3.8, desc: 'French elegance meets raw performance. The open-source darling.' },

  // Epic Tier
  { id: 'nemotron-ultra', name: 'Nemotron 3 Ultra', tier: 'epic', emoji: '👑', baseCost: 300, cpuPerSec: 15, desc: 'The crown jewel of NVIDIA. 70B params of pure compute.' },
  { id: 'llama-3-70b', name: 'Llama 3 70B', tier: 'epic', emoji: '🦙🦙', baseCost: 400, cpuPerSec: 18, desc: 'Meta\'s flagship. Rivals proprietary giants. Fully open.' },
  { id: 'command-r-plus', name: 'Command R+', tier: 'epic', emoji: '⚡', baseCost: 350, cpuPerSec: 16, desc: 'Cohere\'s enterprise beast. RAG king with 128k context.' },
  { id: 'qwen-2-72b', name: 'Qwen 2 72B', tier: 'epic', emoji: '🐲', baseCost: 380, cpuPerSec: 17, desc: 'Alibaba\'s dragon. Tops benchmarks in Chinese & English.' },
  { id: 'yi-34b', name: 'Yi-34B', tier: 'epic', emoji: '🎋', baseCost: 320, cpuPerSec: 14, desc: '01.AI\'s bilingual prodigy. Exceptional reasoning depth.' },

  // Legendary Tier (bought with GPU, very expensive)
  { id: 'gpt-4o-mini', name: 'GPT-4o Mini', tier: 'legendary', emoji: '✨', baseCost: 1500, cpuPerSec: 50, desc: 'OpenAI\'s efficient multimodal. Sees, hears, reasons.' },
  { id: 'claude-3.5-sonnet', name: 'Claude 3.5 Sonnet', tier: 'legendary', emoji: '🎭', baseCost: 1800, cpuPerSec: 60, desc: 'Anthropic\'s coding champion. Thinks before it speaks.' },
  { id: 'gemini-1.5-pro', name: 'Gemini 1.5 Pro', tier: 'legendary', emoji: '♊', baseCost: 2000, cpuPerSec: 65, desc: 'Google\'s 2M context monster. Remembers everything.' },
];

const LEGEND_DEFS = [
  { id: 'gpt-1o', name: 'GPT-1o', tier: 'legendary', emoji: '🌟', ramCost: 50, cpuPerSec: 200, desc: 'The hypothetical "omni" model. Sees all modalities at once. Pure speculation.' },
  { id: 'claude-fable-5', name: 'Claude Fable 5', tier: 'legendary', emoji: '📖', ramCost: 75, cpuPerSec: 300, desc: 'Anthropic\'s mythical storyteller. Writes novels in a single forward pass.' },
  { id: 'opus-5', name: 'Opus 5 by Claude', tier: 'legendary', emoji: '🎼', ramCost: 100, cpuPerSec: 500, desc: 'The magnum opus. 10M context. Self-improving. The final form.' },
];

const TIER_ORDER = { common: 0, rare: 1, epic: 2, legendary: 3 };
const TIER_COLORS = {
  common: { main: '#6b7280', bg: 'bg-common', border: '#6b7280' },
  rare: { main: '#3b82f6', bg: 'bg-rare', border: '#3b82f6' },
  epic: { main: '#a855f7', bg: 'bg-epic', border: '#a855f7' },
  legendary: { main: '#f59e0b', bg: 'bg-legendary', border: '#f59e0b' },
};
const TIER_LABELS = { common: 'COMMON', rare: 'RARE', epic: 'EPIC', legendary: 'LEGENDARY' };

// ===== GAME STATE =====
const state = {
  gpu: 0,
  cpu: 0,
  ram: 0,
  lifetimeGPU: 0,
  prestigeLevel: 0,
  ownedModels: {}, // modelId -> { count, level }
  gameSpeed: 1,
  nextSpawnAt: 0,
  walkingModels: [], // { id, modelDef, x, element, recruited }
  lastTick: performance.now(),
};

// ===== DOM ELEMENTS =====
const els = {
  gpuCoins: document.getElementById('gpu-coins'),
  cpuCoins: document.getElementById('cpu-coins'),
  ramCoins: document.getElementById('ram-coins'),
  spawnTimer: document.getElementById('spawn-timer'),
  carpetTrack: document.getElementById('carpet-track'),
  ownedCount: document.getElementById('owned-count'),
  cpuPerSec: document.getElementById('cpu-per-sec'),
  modelGrid: document.getElementById('model-grid'),
  legendGrid: document.getElementById('legend-grid'),
  speedBtn: document.getElementById('speed-btn'),
  forceSpawnBtn: document.getElementById('force-spawn-btn'),
  convertBtn: document.getElementById('convert-btn'),
  prestigeBtn: document.getElementById('prestige-btn'),
  lifetimeGPU: document.getElementById('lifetime-gpu'),
  ramGain: document.getElementByid('ram-gain'),
  prestigeLevel: document.getElementById('prestige-level'),
  prestigeReq: document.getElementById('prestige-req'),
  toastContainer: document.getElementById('toast-container'),
  modal: document.getElementById('model-modal'),
  modalClose: document.getElementById('modal-close'),
  tabBtns: document.querySelectorAll('.tab-btn'),
  tabPanels: document.querySelectorAll('.tab-panel'),
};

// ===== UTILITIES =====
function formatNum(num) {
  if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
  if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
  if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
  if (num >= 1e3) return (num / 1e3).toFixed(1) + 'K';
  return num.toFixed(num < 10 ? 1 : 0);
}

function getModelCost(modelDef, ownedCount) {
  // Exponential scaling: baseCost * 1.15^owned
  return Math.ceil(modelDef.baseCost * Math.pow(1.15, ownedCount));
}

function getTotalCPUPerSec() {
  let total = 0;
  for (const [modelId, data] of Object.entries(state.ownedModels)) {
    const def = MODEL_DEFS.find(m => m.id === modelId) || LEGEND_DEFS.find(m => m.id === modelId);
    if (def) total += def.cpuPerSec * data.count;
  }
  return total;
}

function getOwnedCount(modelId) {
  return state.ownedModels[modelId]?.count || 0;
}

function canAffordGPU(cost) { return state.gpu >= cost; }
function canAffordRAM(cost) { return state.ram >= cost; }

function spendGPU(amount) { state.gpu -= amount; state.lifetimeGPU += amount; }
function spendRAM(amount) { state.ram -= amount; }
function earnGPU(amount) { state.gpu += amount; state.lifetimeGPU += amount; }
function earnCPU(amount) { state.cpu += amount; }
function earnRAM(amount) { state.ram += amount; }

// ===== STORAGE =====
const SAVE_KEY = 'steal-an-ai-save-v1';
function saveGame() {
  const data = {
    gpu: state.gpu,
    cpu: state.cpu,
    ram: state.ram,
    lifetimeGPU: state.lifetimeGPU,
    prestigeLevel: state.prestigeLevel,
    ownedModels: state.ownedModels,
    gameSpeed: state.gameSpeed,
  };
  localStorage.setItem(SAVE_KEY, JSON.stringify(data));
}

function loadGame() {
  try {
    const data = JSON.parse(localStorage.getItem(SAVE_KEY));
    if (!data) return;
    Object.assign(state, data);
    // Ensure ownedModels exists
    state.ownedModels = state.ownedModels || {};
  } catch (e) {
    console.warn('Failed to load save:', e);
  }
}

function resetGame(keepPrestige = false) {
  state.gpu = 0;
  state.cpu = 0;
  state.ownedModels = {};
  state.nextSpawnAt = performance.now() + 5000;
  state.walkingModels = [];
  if (!keepPrestige) {
    state.ram = 0;
    state.lifetimeGPU = 0;
    state.prestigeLevel = 0;
  }
  clearCarpet();
  saveGame();
}

// ===== TOASTS =====
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  els.toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('removing');
    toast.addEventListener('animationend', () => toast.remove());
  }, 3000);
}

// ===== CARPET / WALKING MODELS =====
function clearCarpet() {
  els.carpetTrack.querySelectorAll('.walking-model').forEach(el => el.remove());
  state.walkingModels = [];
}

function spawnWalkingModel() {
  // Pick a random model weighted by tier (common more frequent)
  const weights = { common: 50, rare: 25, epic: 10, legendary: 3 };
  const pool = [];
  for (const def of MODEL_DEFS) {
    const w = weights[def.tier] || 1;
    for (let i = 0; i < w; i++) pool.push(def);
  }
  const modelDef = pool[Math.floor(Math.random() * pool.length)];
  const owned = getOwnedCount(modelDef.id);

  const el = document.createElement('div');
  el.className = 'walking-model';
  el.dataset.modelId = modelDef.id;
  
  const sprite = document.createElement('div');
  sprite.className = 'model-sprite';
  sprite.style.borderColor = TIER_COLORS[modelDef.tier].main;
  sprite.textContent = modelDef.emoji;
  
  const nameTag = document.createElement('div');
  nameTag.className = 'model-name-tag';
  nameTag.style.borderColor = TIER_COLORS[modelDef.tier].main;
  nameTag.textContent = modelDef.name;
  
  const tierTag = document.createElement('div');
  tierTag.className = `model-tier-tag tier-${modelDef.tier}`;
  tierTag.textContent = TIER_LABELS[modelDef.tier];
  
  const priceTag = document.createElement('div');
  priceTag.className = 'model-price';
  const cost = getModelCost(modelDef, owned);
  priceTag.textContent = owned > 0 ? `+1 copy (${cost} GPU)` : `${cost} GPU`;

  el.append(sprite, nameTag, tierTag, priceTag);
  
  // Start off-screen right
  const trackRect = els.carpetTrack.getBoundingClientRect();
  const startX = trackRect.width + 50;
  el.style.left = startX + 'px';
  
  els.carpetTrack.appendChild(el);
  
  const walkDuration = (8 + Math.random() * 4) * 1000 / state.gameSpeed; // 8-12 seconds at 1x
  const walkData = {
    id: Date.now() + Math.random(),
    modelDef,
    element: el,
    startX,
    startTime: performance.now(),
    duration: walkDuration,
    recruited: false,
  };
  state.walkingModels.push(walkData);
  
  // Click to recruit
  el.addEventListener('click', () => tryRecruit(walkData));
  
  // Also click opens modal for details
  el.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    openModal(modelDef);
  });
}

function tryRecruit(walkData) {
  if (walkData.recruited) return;
  const { modelDef } = walkData;
  const owned = getOwnedCount(modelDef.id);
  const cost = getModelCost(modelDef, owned);
  
  if (!canAffordGPU(cost)) {
    showToast(`Need ${formatNum(cost)} GPU Coins!`, 'error');
    // Shake animation
    walkData.element.style.animation = 'shake 0.3s';
    setTimeout(() => walkData.element.style.animation = '', 300);
    return;
  }
  
  spendGPU(cost);
  walkData.recruited = true;
  walkData.element.classList.add('recruited');
  
  // Add to owned
  if (!state.ownedModels[modelDef.id]) {
    state.ownedModels[modelDef.id] = { count: 0, level: 1 };
  }
  state.ownedModels[modelDef.id].count++;
  
  showToast(`Recruited ${modelDef.name}!`, 'success');
  updateUI();
  
  // Remove after animation
  setTimeout(() => {
    walkData.element.remove();
    state.walkingModels = state.walkingModels.filter(w => w.id !== walkData.id);
  }, 400);
}

function updateWalkingModels(now) {
  const trackRect = els.carpetTrack.getBoundingClientRect();
  const trackWidth = trackRect.width;
  
  for (const walkData of state.walkingModels) {
    if (walkData.recruited) continue;
    
    const elapsed = (now - walkData.startTime) * state.gameSpeed;
    const progress = Math.min(elapsed / walkData.duration, 1);
    const x = walkData.startX - progress * (trackWidth + 100);
    
    walkData.element.style.left = x + 'px';
    
    // Remove if off-screen left
    if (progress >= 1) {
      walkData.element.remove();
    }
  }
  // Clean up finished
  state.walkingModels = state.walkingModels.filter(w => !w.recruited && w.element.parentNode);
}

function forceSpawn() {
  if (!canAffordGPU(5)) {
    showToast('Need 5 GPU Coins!', 'error');
    return;
  }
  spendGPU(5);
  spawnWalkingModel();
  updateUI();
}

// ===== UI UPDATES =====
function updateUI() {
  // Currencies
  els.gpuCoins.textContent = formatNum(state.gpu);
  els.cpuCoins.textContent = formatNum(state.cpu);
  els.ramCoins.textContent = formatNum(state.ram);
  
  // Spawn timer
  const now = performance.now();
  const timeLeft = Math.max(0, (state.nextSpawnAt - now) / 1000);
  els.spawnTimer.textContent = timeLeft.toFixed(1);
  
  // Base stats
  const totalModels = Object.values(state.ownedModels).reduce((sum, m) => sum + m.count, 0);
  const cpuSec = getTotalCPUPerSec();
  els.ownedCount.textContent = totalModels;
  els.cpuPerSec.textContent = formatNum(cpuSec);
  
  // Model grids
  renderModelGrid();
  renderLegendGrid();
  
  // Prestige
  els.lifetimeGPU.textContent = formatNum(state.lifetimeGPU);
  const ramGain = calculateRAMGain();
  els.ramGain.textContent = formatNum(ramGain);
  els.prestigeLevel.textContent = state.prestigeLevel;
  const canPrestige = state.lifetimeGPU >= 1000;
  els.prestigeBtn.disabled = !canPrestige;
  els.prestigeReq.textContent = canPrestige ? 'Ready to prestige!' : `Need ${formatNum(1000 - state.lifetimeGPU)} more lifetime GPU`;
  els.prestigeReq.style.color = canPrestige ? 'var(--accent-ram)' : 'var(--text-muted)';
  
  // Force spawn button
  els.forceSpawnBtn.disabled = !canAffordGPU(5);
}

function renderModelGrid() {
  els.modelGrid.innerHTML = '';
  for (const def of MODEL_DEFS) {
    const owned = getOwnedCount(def.id);
    const cost = getModelCost(def, owned);
    const canBuy = canAffordGPU(cost);
    const colors = TIER_COLORS[def.tier];
    
    const card = document.createElement('div');
    card.className = `model-card ${owned > 0 ? 'owned' : ''} ${colors.bg} tier-${def.tier}`;
    card.dataset.modelId = def.id;
    
    const sprite = document.createElement('div');
    sprite.className = 'model-card-sprite';
    sprite.textContent = def.emoji;
    
    const info = document.createElement('div');
    info.className = 'model-card-info';
    
    const name = document.createElement('div');
    name.className = 'model-card-name';
    name.textContent = def.name;
    
    const tier = document.createElement('div');
    tier.className = `model-card-tier tier-${def.tier}`;
    tier.textContent = TIER_LABELS[def.tier];
    
    const yieldEl = document.createElement('div');
    yieldEl.className = 'model-card-yield';
    yieldEl.textContent = `${formatNum(def.cpuPerSec)}/s`;
    
    const priceEl = document.createElement('div');
    priceEl.className = 'model-card-price';
    priceEl.textContent = owned > 0 ? `Next: ${formatNum(cost)}` : `${formatNum(cost)} GPU`;
    if (!canBuy && owned === 0) priceEl.style.color = 'var(--text-muted)';
    
    info.append(name, tier, yieldEl, priceEl);
    card.append(sprite, info);
    
    card.addEventListener('click', () => openModal(def));
    els.modelGrid.appendChild(card);
  }
}

function renderLegendGrid() {
  els.legendGrid.innerHTML = '';
  for (const def of LEGEND_DEFS) {
    const owned = getOwnedCount(def.id);
    const canBuy = canAffordRAM(def.ramCost);
    const colors = TIER_COLORS[def.tier];
    
    const card = document.createElement('div');
    card.className = `model-card ${owned > 0 ? 'owned' : ''} ${colors.bg} tier-${def.tier}`;
    card.dataset.modelId = def.id;
    
    const sprite = document.createElement('div');
    sprite.className = 'model-card-sprite';
    sprite.textContent = def.emoji;
    
    const info = document.createElement('div');
    info.className = 'model-card-info';
    
    const name = document.createElement('div');
    name.className = 'model-card-name';
    name.textContent = def.name;
    
    const tier = document.createElement('div');
    tier.className = `model-card-tier tier-${def.tier}`;
    tier.textContent = 'OG LEGEND';
    
    const yieldEl = document.createElement('div');
    yieldEl.className = 'model-card-yield';
    yieldEl.textContent = `${formatNum(def.cpuPerSec)}/s`;
    yieldEl.style.color = 'var(--accent-ram)';
    yieldEl.innerHTML = `<span style="color:var(--accent-ram)">🧠</span> ${formatNum(def.cpuPerSec)}/s`;
    
    const priceEl = document.createElement('div');
    priceEl.className = 'model-card-price';
    priceEl.style.color = 'var(--accent-ram)';
    priceEl.innerHTML = owned > 0 ? `Owned` : `${formatNum(def.ramCost)} RAM`;
    if (!canBuy && owned === 0) priceEl.style.opacity = '0.5';
    
    info.append(name, tier, yieldEl, priceEl);
    card.append(sprite, info);
    
    card.addEventListener('click', () => openModal(def, true));
    els.legendGrid.appendChild(card);
  }
}

// ===== MODAL =====
function openModal(def, isLegend = false) {
  const owned = getOwnedCount(def.id);
  const cost = isLegend ? def.ramCost : getModelCost(def, owned);
  const canBuy = isLegend ? canAffordRAM(cost) : canAffordGPU(cost);
  const colors = TIER_COLORS[def.tier];
  
  document.getElementById('modal-tier').textContent = TIER_LABELS[def.tier];
  document.getElementById('modal-tier').className = `modal-tier tier-${def.tier}`;
  document.getElementById('modal-name').textContent = def.name;
  document.getElementById('modal-sprite').textContent = def.emoji;
  document.getElementById('modal-sprite').style.borderColor = colors.main;
  document.getElementById('modal-desc').textContent = def.desc;
  
  const stats = document.getElementById('modal-stats');
  stats.innerHTML = `
    <div class="modal-stat-row"><span>Tier</span><span class="tier-${def.tier}">${TIER_LABELS[def.tier]}</span></div>
    <div class="modal-stat-row"><span>CPU Yield</span><span style="color:var(--accent-cpu)">${formatNum(def.cpuPerSec)}/s</span></div>
    <div class="modal-stat-row"><span>Owned</span><span>${owned}</span></div>
    <div class="modal-stat-row"><span>Cost</span><span style="color:${isLegend ? 'var(--accent-ram)' : 'var(--accent-gpu)'}">${formatNum(cost)} ${isLegend ? 'RAM' : 'GPU'}</span></div>
  `;
  
  const actions = document.getElementById('modal-actions');
  actions.innerHTML = '';
  
  if (owned === 0) {
    const buyBtn = document.createElement('button');
    buyBtn.className = `btn ${isLegend ? 'btn-ram' : ''}`;
    buyBtn.style.background = isLegend ? 'linear-gradient(135deg, var(--accent-ram), #7c3aed)' : 'linear-gradient(135deg, var(--accent-gpu), #e85d2d)';
    buyBtn.textContent = `Buy for ${formatNum(cost)} ${isLegend ? 'RAM' : 'GPU'}`;
    buyBtn.disabled = !canBuy;
    buyBtn.addEventListener('click', () => buyModel(def, isLegend));
    actions.appendChild(buyBtn);
  } else {
    const sellBtn = document.createElement('button');
    sellBtn.className = 'btn';
    sellBtn.style.background = 'linear-gradient(135deg, #6b7280, #4b5563)';
    sellBtn.textContent = `Sell 1 (${formatNum(Math.floor(cost * 0.5))} ${isLegend ? 'RAM' : 'GPU'})`;
    sellBtn.addEventListener('click', () => sellModel(def, isLegend));
    actions.appendChild(sellBtn);
  }
  
  const closeBtn = document.createElement('button');
  closeBtn.className = 'btn';
  closeBtn.style.background = 'var(--border)';
  closeBtn.textContent = 'Close';
  closeBtn.addEventListener('click', () => els.modal.close());
  actions.appendChild(closeBtn);
  
  els.modal.showModal();
}

function buyModel(def, isLegend) {
  const owned = getOwnedCount(def.id);
  const cost = isLegend ? def.ramCost : getModelCost(def, owned);
  
  if (isLegend) {
    if (!canAffordRAM(cost)) return;
    spendRAM(cost);
  } else {
    if (!canAffordGPU(cost)) return;
    spendGPU(cost);
  }
  
  if (!state.ownedModels[def.id]) {
    state.ownedModels[def.id] = { count: 0, level: 1 };
  }
  state.ownedModels[def.id].count++;
  
  showToast(`Acquired ${def.name}!`, isLegend ? 'ram' : 'success');
  els.modal.close();
  updateUI();
}

function sellModel(def, isLegend) {
  const owned = getOwnedCount(def.id);
  if (owned <= 0) return;
  
  const cost = isLegend ? def.ramCost : getModelCost(def, owned - 1);
  const refund = Math.floor(cost * 0.5);
  
  if (isLegend) earnRAM(refund); else earnGPU(refund);
  
  state.ownedModels[def.id].count--;
  if (state.ownedModels[def.id].count === 0) {
    delete state.ownedModels[def.id];
  }
  
  showToast(`Sold ${def.name} for ${formatNum(refund)} ${isLegend ? 'RAM' : 'GPU'}`, 'info');
  els.modal.close();
  updateUI();
}

// ===== PRESTIGE =====
function calculateRAMGain() {
  // Base: sqrt(lifetimeGPU / 1000) * prestigeMultiplier
  const base = Math.sqrt(state.lifetimeGPU / 1000);
  const multiplier = 1 + state.prestigeLevel * 0.5;
  return Math.floor(base * multiplier);
}

function doPrestige() {
  if (state.lifetimeGPU < 1000) return;
  
  const ramGain = calculateRAMGain();
  const oldPrestige = state.prestigeLevel;
  
  resetGame(true); // keep prestige
  state.prestigeLevel = oldPrestige + 1;
  state.ram += ramGain;
  
  showToast(`Prestige ${state.prestigeLevel} reached! Gained ${formatNum(ramGain)} RAM Coins!`, 'ram');
  updateUI();
}

// ===== CONVERT CPU -> GPU =====
function convertCPUtoGPU() {
  const rate = 10; // 10 CPU = 1 GPU
  const amount = Math.floor(state.cpu / rate);
  if (amount <= 0) {
    showToast(`Need at least ${rate} CPU Coins!`, 'error');
    return;
  }
  state.cpu -= amount * rate;
  earnGPU(amount);
  showToast(`Converted ${formatNum(amount * rate)} CPU → ${formatNum(amount)} GPU`, 'success');
  updateUI();
}

// ===== GAME LOOP =====
function gameLoop(now) {
  const dt = (now - state.lastTick) / 1000 * state.gameSpeed;
  state.lastTick = now;
  
  // Passive CPU income
  const cpuSec = getTotalCPUPerSec();
  if (cpuSec > 0) {
    earnCPU(cpuSec * dt);
  }
  
  // Spawn logic
  if (now >= state.nextSpawnAt) {
    spawnWalkingModel();
    // Next spawn: 5-15 seconds, faster with more models
    const ownedTotal = Object.values(state.ownedModels).reduce((s, m) => s + m.count, 0);
    const interval = Math.max(3, 15 - ownedTotal * 0.5) * 1000;
    state.nextSpawnAt = now + interval;
  }
  
  // Update walking models
  updateWalkingModels(now);
  
  // UI update (throttled to ~10fps for performance)
  if (Math.floor(now / 100) !== Math.floor((now - dt * 1000) / 100)) {
    updateUI();
  }
  
  requestAnimationFrame(gameLoop);
}

// ===== EVENT LISTENERS =====
els.speedBtn.addEventListener('click', () => {
  const speeds = [1, 2, 5, 10];
  const idx = speeds.indexOf(state.gameSpeed);
  state.gameSpeed = speeds[(idx + 1) % speeds.length];
  els.speedBtn.textContent = `⏩ ${state.gameSpeed}x`;
});

els.forceSpawnBtn.addEventListener('click', forceSpawn);
els.convertBtn.addEventListener('click', convertCPUtoGPU);
els.prestigeBtn.addEventListener('click', doPrestige);

els.modalClose.addEventListener('click', () => els.modal.close());
els.modal.addEventListener('click', (e) => { if (e.target === els.modal) els.modal.close(); });

// Tabs
els.tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const tab = btn.dataset.tab;
    els.tabBtns.forEach(b => b.classList.toggle('active', b === btn));
    els.tabPanels.forEach(p => p.classList.toggle('active', p.id === `tab-${tab}`));
  });
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT') return;
  switch (e.key.toLowerCase()) {
    case 'c': convertCPUtoGPU(); break;
    case 'f': forceSpawn(); break;
    case 's': els.speedBtn.click(); break;
    case 'p': if (!els.prestigeBtn.disabled) doPrestige(); break;
    case 'escape': if (els.modal.open) els.modal.close(); break;
  }
});

// ===== INIT =====
loadGame();
// Ensure nextSpawnAt is set
if (!state.nextSpawnAt || state.nextSpawnAt < performance.now()) {
  state.nextSpawnAt = performance.now() + 5000;
}
updateUI();
requestAnimationFrame(gameLoop);

// Auto-save every 10 seconds
setInterval(saveGame, 10000);
// Save on visibility change
document.addEventListener('visibilitychange', () => {
  if (document.hidden) saveGame();
});

console.log('🎮 Steal an AI loaded! Press C to convert CPU→GPU, F to force spawn, S for speed, P to prestige.');