const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

const toggleBtn = document.getElementById('toggleBtn');
const resetBtn = document.getElementById('resetBtn');
const debugCheckbox = document.getElementById('debugCheckbox');

const popCountEl = document.getElementById('popCount');
const foodCountEl = document.getElementById('foodCount');
const poisonCountEl = document.getElementById('poisonCount');
const maxAgeEl = document.getElementById('maxAge');
const fpsCounter = document.getElementById('fpsCounter');

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

// Evolution configuration
const MUTATION_RATE = 0.05;
const MAX_SPEED = 4;
const MAX_FORCE = 0.2;
const FOOD_NUTRITION = 0.3;
const POISON_NUTRITION = -0.7;
const REPRODUCTION_THRESHOLD = 2.5; // Health needed to reproduce

// Helper vector functions
function magnitude(vx, vy) { return Math.sqrt(vx*vx + vy*vy); }
function normalize(vx, vy) {
    let m = magnitude(vx, vy);
    if (m > 0) return {x: vx/m, y: vy/m};
    return {x: vx, y: vy};
}
function distance(x1, y1, x2, y2) {
    let dx = x1 - x2; let dy = y1 - y2;
    return Math.sqrt(dx*dx + dy*dy);
}
function limit(vx, vy, max) {
    let m = magnitude(vx, vy);
    if (m > max) {
        let n = normalize(vx, vy);
        return {x: n.x * max, y: n.y * max};
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
        this.r = 4; // base radius
        this.health = 1.0;
        this.age = 0;

        // DNA contains 4 genes:
        // 0: Food Attraction Weight (-2 to +2)
        // 1: Poison Attraction Weight (-2 to +2)
        // 2: Food Perception Radius (10 to 150)
        // 3: Poison Perception Radius (10 to 150)
        if (dna) {
            this.dna = dna;
        } else {
            this.dna = [
                (Math.random() * 4) - 2,
                (Math.random() * 4) - 2,
                (Math.random() * 140) + 10,
                (Math.random() * 140) + 10
            ];
        }
    }

    update() {
        // Apply acceleration to velocity
        this.vx += this.ax;
        this.vy += this.ay;
        let limited = limit(this.vx, this.vy, MAX_SPEED);
        this.vx = limited.x;
        this.vy = limited.y;

        // Update position
        this.x += this.vx;
        this.y += this.vy;

        // Reset acceleration
        this.ax = 0;
        this.ay = 0;

        // Boundaries
        this.x = (this.x + width) % width;
        this.y = (this.y + height) % height;

        // Aging and health decay
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

        // Shortest path handling for toroidal world
        if (desiredX > width/2) desiredX -= width;
        else if (desiredX < -width/2) desiredX += width;
        if (desiredY > height/2) desiredY -= height;
        else if (desiredY < -height/2) desiredY += height;

        let m = magnitude(desiredX, desiredY);
        if (m === 0) return {x:0, y:0};

        let norm = normalize(desiredX, desiredY);
        desiredX = norm.x * MAX_SPEED;
        desiredY = norm.y * MAX_SPEED;

        let steerX = desiredX - this.vx;
        let steerY = desiredY - this.vy;

        let steerLim = limit(steerX, steerY, MAX_FORCE);
        return {x: steerLim.x * weight, y: steerLim.y * weight};
    }

    eat(list, nutrition, perceptionRadius) {
        let record = Infinity;
        let closest = -1;

        for (let i = list.length - 1; i >= 0; i--) {
            let item = list[i];

            // Calc distance considering toroidal world
            let dx = this.x - item.x;
            let dy = this.y - item.y;
            if (dx > width/2) dx -= width;
            else if (dx < -width/2) dx += width;
            if (dy > height/2) dy -= height;
            else if (dy < -height/2) dy += height;

            let d = Math.sqrt(dx*dx + dy*dy);

            if (d < this.r + 2) {
                // Eaten!
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

            // Mutate
            for (let i = 0; i < childDNA.length; i++) {
                if (Math.random() < MUTATION_RATE) {
                    if (i < 2) childDNA[i] += (Math.random() * 0.4 - 0.2); // mutate weights
                    else childDNA[i] += (Math.random() * 20 - 10);        // mutate radii

                    // Clamp values
                    if (i < 2) {
                        childDNA[i] = Math.max(-2, Math.min(2, childDNA[i]));
                    } else {
                        childDNA[i] = Math.max(10, Math.min(150, childDNA[i]));
                    }
                }
            }

            this.health -= 1.0; // Childbirth costs energy
            return new Vehicle(this.x, this.y, childDNA);
        }
        return null;
    }

    draw(ctx) {
        let angle = Math.atan2(this.vy, this.vx);

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(angle);

        if (debugMode) {
            // Draw perception radii
            ctx.beginPath();
            ctx.arc(0, 0, this.dna[2], 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(34, 197, 94, 0.2)'; // Green for food
            ctx.stroke();

            ctx.beginPath();
            ctx.arc(0, 0, this.dna[3], 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.2)'; // Red for poison
            ctx.stroke();

            // Draw force lines (length indicates weight)
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(this.dna[0] * 20, 0);
            ctx.strokeStyle = 'rgba(34, 197, 94, 0.8)';
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(this.dna[1] * 20, 0);
            ctx.strokeStyle = 'rgba(239, 68, 68, 0.8)';
            ctx.stroke();
        }

        // Draw body (Triangle pointing right)
        // Color blends based on health
        let colorMix = Math.max(0, Math.min(1, this.health));
        let r = Math.floor(255 * (1 - colorMix) + 100 * colorMix);
        let g = Math.floor(100 * (1 - colorMix) + 200 * colorMix);
        ctx.fillStyle = `rgba(${r}, ${g}, 150, 0.8)`;
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;

        ctx.beginPath();
        ctx.moveTo(this.r * 2, 0);
        ctx.lineTo(-this.r, -this.r);
        ctx.lineTo(-this.r, this.r);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        ctx.restore();
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

    // Initial population
    for (let i = 0; i < 50; i++) {
        vehicles.push(new Vehicle(Math.random() * width, Math.random() * height));
    }

    spawnItems(food, 100);
    spawnItems(poison, 30);
}

function loop(timestamp) {
    if (!isRunning) {
        lastTime = timestamp;
        animationId = requestAnimationFrame(loop);
        return;
    }

    // Clear background
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, width, height);

    // Random spawns
    if (Math.random() < 0.1) food.push({ x: Math.random() * width, y: Math.random() * height });
    if (Math.random() < 0.02) poison.push({ x: Math.random() * width, y: Math.random() * height });

    // Draw Food
    ctx.fillStyle = '#22c55e';
    for (let i = 0; i < food.length; i++) {
        ctx.beginPath();
        ctx.arc(food[i].x, food[i].y, 2, 0, Math.PI * 2);
        ctx.fill();
    }

    // Draw Poison
    ctx.fillStyle = '#ef4444';
    for (let i = 0; i < poison.length; i++) {
        ctx.beginPath();
        ctx.arc(poison[i].x, poison[i].y, 2, 0, Math.PI * 2);
        ctx.fill();
    }

    let highestAge = 0;

    // Update Vehicles
    for (let i = vehicles.length - 1; i >= 0; i--) {
        let v = vehicles[i];

        v.behaviors(food, poison);
        v.update();
        v.draw(ctx);

        if (v.age > highestAge) highestAge = v.age;

        let child = v.reproduce();
        if (child != null) {
            vehicles.push(child);
        }

        if (v.dead()) {
            // Drop a food when dying (circle of life)
            food.push({x: v.x, y: v.y});
            vehicles.splice(i, 1);
        }
    }

    // Automatically restock population if extinction happens
    if (vehicles.length === 0) {
        init();
    }

    // Update UI
    popCountEl.textContent = vehicles.length;
    foodCountEl.textContent = food.length;
    poisonCountEl.textContent = poison.length;
    maxAgeEl.textContent = highestAge;

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

debugCheckbox.addEventListener('change', (e) => {
    debugMode = e.target.checked;
});

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    // Spawn a burst of food on click
    for (let i = 0; i < 5; i++) {
        food.push({ x: x + (Math.random()*20-10), y: y + (Math.random()*20-10) });
    }
});

// Boot
init();
requestAnimationFrame(loop);