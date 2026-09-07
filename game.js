class Game {
    constructor() {
        this.ram = 0;
        this.totalRamGenerated = 0;
        this.prestigeLevel = 0;
        this.prestigeMultiplier = 1;
        this.prestigeCost = 1000000;
        
        this.models = [
            { id: 'phi-3-mini', name: 'Phi-3 Mini', baseCost: 10, ramPerSec: 1, count: 0, cost: 10 },
            { id: 'gemma-2b', name: 'Gemma 2B', baseCost: 100, ramPerSec: 5, count: 0, cost: 100 },
            { id: 'llama-3-8b', name: 'Llama-3 8B', baseCost: 1000, ramPerSec: 25, count: 0, cost: 1000 },
            { id: 'mistral-7b', name: 'Mistral 7B', baseCost: 10000, ramPerSec: 100, count: 0, cost: 10000 },
            { id: 'qwen-2-7b', name: 'Qwen-2 7B', baseCost: 50000, ramPerSec: 500, count: 0, cost: 50000 },
            { id: 'nemotron-3b', name: 'Nemotron 3B', baseCost: 250000, ramPerSec: 2000, count: 0, cost: 250000 },
            { id: 'phi-3-medium', name: 'Phi-3 Medium', baseCost: 1000000, ramPerSec: 10000, count: 0, cost: 1000000 },
            { id: 'llama-3-70b', name: 'Llama-3 70B', baseCost: 5000000, ramPerSec: 50000, count: 0, cost: 5000000 },
            { id: 'gemini-1_5-pro', name: 'Gemini 1.5 Pro', baseCost: 25000000, ramPerSec: 200000, count: 0, cost: 25000000 },
            { id: 'gpt-4o-mini', name: 'GPT-4o Mini', baseCost: 100000000, ramPerSec: 1000000, count: 0, cost: 100000000 },
            { id: 'claude-3_5-sonnet', name: 'Claude 3.5 Sonnet', baseCost: 500000000, ramPerSec: 5000000, count: 0, cost: 500000000 },
            { id: 'gpt-1o', name: 'GPT-1o', baseCost: 2000000000, ramPerSec: 20000000, count: 0, cost: 2000000000 },
            { id: 'opus-5', name: 'Opus 5', baseCost: 10000000000, ramPerSec: 100000000, count: 0, cost: 10000000000 }
        ];

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.gameLoop();
        this.updateUI();
    }

    setupEventListeners() {
        this.models.forEach(model => {
            const btn = document.getElementById(`btn-${model.id}`);
            if (btn) {
                btn.onclick = () => this.buyModel(model);
            }
        });

        const prestigeBtn = document.getElementById('btn-prestige');
        if (prestigeBtn) {
            prestigeBtn.onclick = () => this.prestige();
        }

        const clickBtn = document.getElementById('btn-main-click');
        if (clickBtn) {
            clickBtn.onclick = (e) => this.manualClick(e);
        }
    }

    manualClick(e) {
        const amount = 1 * this.prestigeMultiplier;
        this.ram += amount;
        this.totalRamGenerated += amount;
        this.createParticle(e.clientX, e.clientY, 'ram');
        this.updateUI();
    }

    buyModel(model) {
        if (this.ram >= model.cost) {
            this.ram -= model.cost;
            model.count++;
            model.cost = isNaN(model.baseCost) ? 10 : Math.floor(model.baseCost * Math.pow(1.2, model.count || 0));
            this.updateUI();
            this.showToast(`Acquired ${model.name}!`);
        } else {
            this.showToast("Not enough RAM!", "error");
        }
    }

    prestige() {
        if (this.ram < this.prestigeCost) {
            this.showToast("Not enough RAM to prestige!", "error");
            return;
        }
        
        this.ram -= this.prestigeCost;
        this.prestigeLevel++;
        this.prestigeMultiplier = 1 + (this.prestigeLevel * 0.15);
        
        this.models.forEach(model => {
            model.count = 0;
            model.cost = model.baseCost;
        });
        
        this.totalRamGenerated = 0;
        this.updateUI();
        this.showToast(`Prestiged! Multiplier is now x${this.prestigeMultiplier.toFixed(2)}`, "success");
    }

    gameLoop() {
        setInterval(() => {
            let totalRamPerSec = 0;
            this.models.forEach(model => {
                totalRamPerSec += model.count * model.ramPerSec;
            });

            const gain = (totalRamPerSec * this.prestigeMultiplier) / 10;
            this.ram += gain;
            this.totalRamGenerated += gain;
            this.updateUI();
        }, 100);
    }

    updateModelVisibility() {
        this.models.forEach((model, index) => {
            const modelRow = document.getElementById(`model-row-${model.id}`);
            if (modelRow) {
                const prevModel = this.models[index - 1];
                const shouldBeVisible = index === 0 || 
                                      (prevModel && prevModel.count > 0) || 
                                      (this.ram >= model.baseCost * 0.5);

                modelRow.style.display = shouldBeVisible ? 'flex' : 'none';
            }
        });
    }

    updateUI() {
        this.updateModelVisibility();
        
        const ramDisplay = document.getElementById('ram-display');
        const totalRamDisplay = document.getElementById('total-ram');
        const prestigeLevelDisplay = document.getElementById('prestige-level');
        const multiplierDisplay = document.getElementById('multiplier-display');

        if (ramDisplay) ramDisplay.innerText = Math.floor(this.ram || 0).toLocaleString();
        if (totalRamDisplay) totalRamDisplay.innerText = Math.floor(this.totalRamGenerated || 0).toLocaleString();
        if (prestigeLevelDisplay) prestigeLevelDisplay.innerText = this.prestigeLevel || 0;
        if (multiplierDisplay) multiplierDisplay.innerText = (this.prestigeMultiplier || 1).toFixed(2);
        
        this.models.forEach((model) => {
            const costElement = document.getElementById(`cost-${model.id}`);
            if (costElement) {
                costElement.innerText = Math.floor(model.cost || 0).toLocaleString();
            }
            const countElement = document.getElementById(`count-${model.id}`);
            if (countElement) {
                countElement.innerText = model.count || 0;
            }
        });
    }

    createParticle(x, y, type) {
        const particle = document.createElement('div');
        particle.className = `particle particle-${type}`;
        particle.style.left = `${x}px`;
        particle.style.top = `${y}px`;
        particle.style.pointerEvents = 'none';
        document.body.appendChild(particle);

        setTimeout(() => {
            if (particle && particle.parentNode) {
                particle.remove();
            }
        }, 1000);
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }
}

window.onload = () => {
    window.game = new Game();
};