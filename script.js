const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

const toggleBtn = document.getElementById('toggleBtn');
const randomizeRulesBtn = document.getElementById('randomizeRulesBtn');
const resetParticlesBtn = document.getElementById('resetParticlesBtn');
const frictionSlider = document.getElementById('frictionSlider');
const radiusSlider = document.getElementById('radiusSlider');

// Configuration
const width = canvas.width;
const height = canvas.height;
let isRunning = true;
let animationId;

// Physics parameters
let friction = 0.5; // (will be derived from slider)
let maxRadius = 80;

// Particle setup
const numParticlesPerColor = 400;
const colors = ['#ef4444', '#22c55e', '#3b82f6', '#eab308', '#a855f7', '#06b6d4']; // Red, Green, Blue, Yellow, Purple, Cyan
let particles = [];
let rules = []; // Matrix of attraction/repulsion between colors

// Initialize rules matrix with random values between -1 (repel) and 1 (attract)
function randomizeRules() {
    rules = [];
    for (let i = 0; i < colors.length; i++) {
        let row = [];
        for (let j = 0; j < colors.length; j++) {
            // Random value between -1 and 1
            row.push(Math.random() * 2 - 1);
        }
        rules.push(row);
    }
}

// Create particles
function initParticles() {
    particles = [];
    for (let i = 0; i < colors.length; i++) {
        for (let j = 0; j < numParticlesPerColor; j++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: 0,
                vy: 0,
                colorIndex: i,
                color: colors[i]
            });
        }
    }
}

// Core physics engine
function updateParticles() {
    friction = frictionSlider.value / 100;
    maxRadius = parseInt(radiusSlider.value);

    // Using a simple O(N^2) for 2400 particles is manageable in JS,
    // but we optimize by pre-calculating some things.
    for (let i = 0; i < particles.length; i++) {
        let p1 = particles[i];
        let fx = 0;
        let fy = 0;

        for (let j = 0; j < particles.length; j++) {
            if (i === j) continue;
            let p2 = particles[j];

            let dx = p1.x - p2.x;
            let dy = p1.y - p2.y;

            // Toroidal wrap (wrap around screen edges for distance calculation)
            if (dx > width / 2) dx -= width;
            else if (dx < -width / 2) dx += width;

            if (dy > height / 2) dy -= height;
            else if (dy < -height / 2) dy += height;

            let d2 = dx * dx + dy * dy;

            if (d2 > 0 && d2 < maxRadius * maxRadius) {
                let d = Math.sqrt(d2);
                // Force factor based on rule matrix
                let force = rules[p1.colorIndex][p2.colorIndex];

                // Extremely close particles repel strongly (collision avoidance)
                if (d < 5) {
                    force = 3; // Positive force pushes p1 away from p2 (repulsion)
                }

                // Normal attraction/repulsion based on distance
                // The force fades out linearly as distance approaches maxRadius
                let strength = force * (1 - d / maxRadius);

                fx += (dx / d) * strength;
                fy += (dy / d) * strength;
            }
        }

        // Apply force to velocity, with friction
        p1.vx = (p1.vx + fx) * friction;
        p1.vy = (p1.vy + fy) * friction;

        // Speed limit
        let speed = Math.sqrt(p1.vx * p1.vx + p1.vy * p1.vy);
        if (speed > 15) {
            p1.vx = (p1.vx / speed) * 15;
            p1.vy = (p1.vy / speed) * 15;
        }

        // Update position
        p1.x += p1.vx;
        p1.y += p1.vy;

        // Wrap around screen boundaries
        if (p1.x < 0) p1.x += width;
        else if (p1.x >= width) p1.x -= width;

        if (p1.y < 0) p1.y += height;
        else if (p1.y >= height) p1.y -= height;
    }
}

function drawParticles() {
    ctx.clearRect(0, 0, width, height);

    // We can draw slightly larger/blurred to look cool, or just solid squares
    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 3, 3);
    }
}

function loop() {
    if (isRunning) {
        updateParticles();
        drawParticles();
    }
    animationId = requestAnimationFrame(loop);
}

// Event Listeners
toggleBtn.addEventListener('click', () => {
    isRunning = !isRunning;
    toggleBtn.textContent = isRunning ? "Pause" : "Start";
});

randomizeRulesBtn.addEventListener('click', () => {
    randomizeRules();
});

resetParticlesBtn.addEventListener('click', () => {
    initParticles();
});

// Boot up
randomizeRules();
initParticles();
loop();
