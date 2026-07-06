const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

// UI Elements
const toggleBtn = document.getElementById('toggleBtn');
const resetBtn = document.getElementById('resetBtn');
const catastropheBtn = document.getElementById('catastropheBtn');
const debugCheckbox = document.getElementById('debugCheckbox');

const mutRateSlider = document.getElementById('mutRateSlider');
const foodRateSlider = document.getElementById('foodRateSlider');
const poisonRateSlider = document.getElementById('poisonRateSlider');
const mutRateVal = document.getElementById('mutRateVal');
const foodRateVal = document.getElementById('foodRateVal');
const poisonRateVal = document.getElementById('poisonRateVal');

const popCountEl = document.getElementById('popCount');
const foodCountEl = document.getElementById('foodCount');
const poisonCountEl = document.getElementById('poisonCount');
const maxAgeEl = document.getElementById('maxAge');
const fpsCounter = document.getElementById('fpsCounter');

const avgFoodAttrBar = document.getElementById('avgFoodAttrBar');
const avgPoisonAttrBar = document.getElementById('avgPoisonAttrBar');
const avgFoodPercBar = document.getElementById('avgFoodPercBar');

const inspectorPanel = document.getElementById('inspectorPanel');
const inspectorData = document.querySelector('.inspector-data');
const insHint = document.querySelector('.hint');
const insAge = document.getElementById('insAge');
const insHealth = document.getElementById('insHealth');
const insFoodAttr = document.getElementById('insFoodAttr');
const insPoisonAttr = document.getElementById('insPoisonAttr');
const insFoodVis = document.getElementById('insFoodVis');
const insPoisonVis = document.getElementById('insPoisonVis');

const width = canvas.width;
const height = canvas.height;

let isRunning = true;
let debugMode = false;
let animationId;
let lastTime = 0;
let frameCount = 0;

let vehicles = [];
let food = [];
let poison = [];

let selectedVehicle = null;

// Config bounds
const MAX_SPEED = 4;
const MAX_FORCE = 0.2;
const FOOD_NUTRITION = 0.3;
const POISON_NUTRITION = -0.7;
const REPRODUCTION_THRESHOLD = 2.5;

// Helpers
function limit(vx, vy, max) {
    let m = Math.sqrt(vx*vx + vy*vy);
    if (m > max) {
        return {x: (vx/m) * max, y: (vy/m) * max};
    }
    return {x: vx, y: vy};
}

class Vehicle {
    constructor(x, y, dna) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() * 2 - 1) * MAX_SPEED;
        this.vy = (Math.random() * 2 - 1) * MAX_SPEED;
        this.ax = 0;
        this.ay = 0;
        this.r = 5;
        this.health = 1.0;
        this.age = 0;

        // DNA:
        // 0: Food Attraction (-3 to 3)
        // 1: Poison Attraction (-3 to 3)
        // 2: Food Perception (10 to 150)
        // 3: Poison Perception (10 to 150)
        if (dna) {
            this.dna = dna;
        } else {
            this.dna = [
                (Math.random() * 6) - 3,
                (Math.random() * 6) - 3,
                (Math.random() * 140) + 10,
                (Math.random() * 140) + 10
            ];
        }
    }

    update() {
        this.vx += this.ax;
        this.vy += this.ay;
        let limited = limit(this.vx, this.vy, MAX_SPEED);
        this.vx = limited.x;
        this.vy = limited.y;

        this.x += this.vx;
        this.y += this.vy;

        this.ax = 0;
        this.ay = 0;

        this.x = (this.x + width) % width;
        this.y = (this.y + height) % height;

        this.health -= 0.003;
        this.age++;
    }

    applyForce(fx, fy) {
        this.ax += fx;
        this.ay += fy;
    }

    seek(targetX, targetY, weight) {
        let desiredX = targetX - this.x;
        let desiredY = targetY - this.y;

        if (desiredX > width/2) desiredX -= width;
        else if (desiredX < -width/2) desiredX += width;
        if (desiredY > height/2) desiredY -= height;
        else if (desiredY < -height/2) desiredY += height;

        let m = Math.sqrt(desiredX*desiredX + desiredY*desiredY);
        if (m === 0) return {x:0, y:0};

        desiredX = (desiredX/m) * MAX_SPEED;
        desiredY = (desiredY/m) * MAX_SPEED;

        let steerLim = limit(desiredX - this.vx, desiredY - this.vy, MAX_FORCE);
        return {x: steerLim.x * weight, y: steerLim.y * weight};
    }

    eat(list, nutrition, perceptionRadius) {
        let record = Infinity;
        let closest = -1;

        for (let i = list.length - 1; i >= 0; i--) {
            let item = list[i];

            let dx = this.x - item.x;
            let dy = this.y - item.y;
            if (dx > width/2) dx -= width;
            else if (dx < -width/2) dx += width;
            if (dy > height/2) dy -= height;
            else if (dy < -height/2) dy += height;

            let d = Math.sqrt(dx*dx + dy*dy);

            if (d < this.r + 2) {
                list.splice(i, 1);
                this.health += nutrition;
            } else if (d < record && d < perceptionRadius) {
                record = d;
                closest = i;
            }
        }

        if (closest > -1) {
            return this.seek(list[closest].x, list[closest].y, 1);
        }
        return {x:0, y:0};
    }

    behaviors(good, bad) {
        let steerG = this.eat(good, FOOD_NUTRITION, this.dna[2]);
        let steerB = this.eat(bad, POISON_NUTRITION, this.dna[3]);

        this.applyForce(steerG.x * this.dna[0], steerG.y * this.dna[0]);
        this.applyForce(steerB.x * this.dna[1], steerB.y * this.dna[1]);
    }

    reproduce() {
        if (Math.random() < 0.002 && this.health > REPRODUCTION_THRESHOLD) {
            let childDNA = [...this.dna];
            let mutationRate = parseInt(mutRateSlider.value) / 100;

            for (let i = 0; i < childDNA.length; i++) {
                if (Math.random() < mutationRate) {
                    if (i < 2) childDNA[i] += (Math.random() * 0.4 - 0.2);
                    else childDNA[i] += (Math.random() * 20 - 10);

                    if (i < 2) childDNA[i] = Math.max(-3, Math.min(3, childDNA[i]));
                    else childDNA[i] = Math.max(10, Math.min(150, childDNA[i]));
                }
            }

            this.health -= 1.0;
            return new Vehicle(this.x, this.y, childDNA);
        }
        return null;
    }

    draw(ctx) {
        let angle = Math.atan2(this.vy, this.vx);

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(angle);

        let isSelected = (this === selectedVehicle);

        if (debugMode || isSelected) {
            ctx.beginPath();
            ctx.arc(0, 0, this.dna[2], 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(34, 197, 94, 0.2)';
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(0, 0, this.dna[3], 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.2)';
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(this.dna[0] * 15, 0);
            ctx.strokeStyle = 'rgba(34, 197, 94, 0.8)';
            ctx.lineWidth = 2;
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(this.dna[1] * 15, 0);
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.8)';
            ctx.stroke();
        }

        // Color based on DNA
        // Green if likes food, Red if likes poison
        let rColor = Math.floor(Math.max(0, this.dna[1]) / 3 * 255);
        let gColor = Math.floor(Math.max(0, this.dna[0]) / 3 * 255);
        // Dim if low health
        let alpha = Math.max(0.2, Math.min(1, this.health));

        ctx.fillStyle = `rgba(${rColor + 50}, ${gColor + 50}, 50, ${alpha})`;

        if (isSelected) {
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
        } else {
            ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.lineWidth = 1;
        }

        ctx.beginPath();
        ctx.moveTo(this.r * 2, 0);
        ctx.lineTo(-this.r, -this.r);
        ctx.lineTo(-this.r, this.r);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        ctx.restore();

        // Draw selection ring
        if (isSelected) {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r * 3, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 0, 0.8)';
            ctx.setLineDash([4, 2]);
            ctx.stroke();
            ctx.setLineDash([]);
        }
    }

    dead() {
        return (this.health <= 0);
    }
}

function spawnItems(arr, count) {
    for (let i = 0; i < count; i++) {
        arr.push({ x: Math.random() * width, y: Math.random() * height });
    }
}

function init() {
    vehicles = [];
    food = [];
    poison = [];
    selectedVehicle = null;

    for (let i = 0; i < 60; i++) {
        vehicles.push(new Vehicle(Math.random() * width, Math.random() * height));
    }

    spawnItems(food, 120);
    spawnItems(poison, 40);
    updateInspector();
}

function updateGlobalStats() {
    if (vehicles.length === 0) return;

    let avgFoodAttr = 0;
    let avgPoisonAttr = 0;
    let avgFoodPerc = 0;

    for(let v of vehicles) {
        avgFoodAttr += v.dna[0];
        avgPoisonAttr += v.dna[1];
        avgFoodPerc += v.dna[2];
    }

    avgFoodAttr /= vehicles.length;
    avgPoisonAttr /= vehicles.length;
    avgFoodPerc /= vehicles.length;

    // Map -3 to 3 to 0% to 100%
    let faPercent = ((avgFoodAttr + 3) / 6) * 100;
    let paPercent = ((avgPoisonAttr + 3) / 6) * 100;
    // Map 10 to 150 to 0% to 100%
    let fpPercent = ((avgFoodPerc - 10) / 140) * 100;

    avgFoodAttrBar.style.width = `${Math.max(0, Math.min(100, faPercent))}%`;
    avgPoisonAttrBar.style.width = `${Math.max(0, Math.min(100, paPercent))}%`;
    avgFoodPercBar.style.width = `${Math.max(0, Math.min(100, fpPercent))}%`;
}

function updateInspector() {
    if (selectedVehicle && !selectedVehicle.dead()) {
        insHint.style.display = 'none';
        inspectorData.style.display = 'block';

        insAge.textContent = selectedVehicle.age;
        insHealth.textContent = selectedVehicle.health.toFixed(2);
        insFoodAttr.textContent = selectedVehicle.dna[0].toFixed(2);
        insPoisonAttr.textContent = selectedVehicle.dna[1].toFixed(2);
        insFoodVis.textContent = selectedVehicle.dna[2].toFixed(0);
        insPoisonVis.textContent = selectedVehicle.dna[3].toFixed(0);
    } else {
        selectedVehicle = null;
        insHint.style.display = 'block';
        inspectorData.style.display = 'none';
    }
}

function loop(timestamp) {
    if (!isRunning) {
        lastTime = timestamp;
        animationId = requestAnimationFrame(loop);
        return;
    }

    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, width, height);

    // Spawning based on sliders
    let fRate = parseInt(foodRateSlider.value) / 100;
    let pRate = parseInt(poisonRateSlider.value) / 100;

    if (Math.random() < fRate) food.push({ x: Math.random() * width, y: Math.random() * height });
    if (Math.random() < pRate) poison.push({ x: Math.random() * width, y: Math.random() * height });

    ctx.fillStyle = '#22c55e';
    for (let f of food) {
        ctx.beginPath(); ctx.arc(f.x, f.y, 2, 0, Math.PI * 2); ctx.fill();
    }

    ctx.fillStyle = '#ef4444';
    for (let p of poison) {
        ctx.beginPath(); ctx.arc(p.x, p.y, 2, 0, Math.PI * 2); ctx.fill();
    }

    let highestAge = 0;

    for (let i = vehicles.length - 1; i >= 0; i--) {
        let v = vehicles[i];
        v.behaviors(food, poison);
        v.update();
        v.draw(ctx);

        if (v.age > highestAge) highestAge = v.age;

        let child = v.reproduce();
        if (child != null) vehicles.push(child);

        if (v.dead()) {
            food.push({x: v.x, y: v.y}); // drops food on death
            vehicles.splice(i, 1);
        }
    }

    if (vehicles.length === 0) init();

    // UI Updates
    popCountEl.textContent = vehicles.length;
    foodCountEl.textContent = food.length;
    poisonCountEl.textContent = poison.length;
    maxAgeEl.textContent = highestAge;

    if (frameCount % 10 === 0) {
        updateGlobalStats();
        updateInspector();
    }

    // FPS
    frameCount++;
    if (timestamp - lastTime >= 1000) {
        fpsCounter.textContent = `FPS: ${frameCount}`;
        frameCount = 0;
        lastTime = timestamp;
    }

    animationId = requestAnimationFrame(loop);
}

// Events
toggleBtn.addEventListener('click', () => {
    isRunning = !isRunning;
    toggleBtn.textContent = isRunning ? "Pause" : "Start";
});

resetBtn.addEventListener('click', init);

catastropheBtn.addEventListener('click', () => {
    // Kill 50% randomly
    vehicles = vehicles.filter(() => Math.random() > 0.5);
    updateInspector();
});

debugCheckbox.addEventListener('change', (e) => { debugMode = e.target.checked; });

mutRateSlider.addEventListener('input', (e) => mutRateVal.textContent = e.target.value + '%');
foodRateSlider.addEventListener('input', (e) => foodRateVal.textContent = e.target.value + '%');
poisonRateSlider.addEventListener('input', (e) => poisonRateVal.textContent = e.target.value + '%');

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Check if clicked on a vehicle
    let clickedVehicle = null;
    let minDist = Infinity;

    for(let v of vehicles) {
        let dx = v.x - x;
        let dy = v.y - y;
        let d = Math.sqrt(dx*dx + dy*dy);
        if(d < v.r * 3 && d < minDist) {
            minDist = d;
            clickedVehicle = v;
        }
    }

    if (clickedVehicle) {
        selectedVehicle = clickedVehicle;
        updateInspector();
    } else {
        // Spawn food
        for (let i = 0; i < 5; i++) {
            food.push({ x: x + (Math.random()*20-10), y: y + (Math.random()*20-10) });
        }
    }
});

// Boot
init();
requestAnimationFrame(loop);