const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

const toggleBtn = document.getElementById('toggleBtn');
const randomizeRulesBtn = document.getElementById('randomizeRulesBtn');
const resetParticlesBtn = document.getElementById('resetParticlesBtn');
const frictionSlider = document.getElementById('frictionSlider');
const radiusSlider = document.getElementById('radiusSlider');
const trailsCheckbox = document.getElementById('trailsCheckbox');
const fpsCounter = document.getElementById('fpsCounter');

// Configuration
const width = canvas.width;
const height = canvas.height;
let isRunning = true;
let animationId;
let useTrails = true;

// FPS
let lastTime = 0;
let frameCount = 0;

// Physics parameters
let friction = 0.5;
let maxRadius = 80;

// Particle setup - increased significantly for better emergence!
const numParticlesPerColor = 800; // Total: 4800 particles
const colors = ['#ef4444', '#22c55e', '#3b82f6', '#eab308', '#a855f7', '#06b6d4']; // Red, Green, Blue, Yellow, Purple, Cyan
let particles = [];
let rules = [];

// Spatial Hashing Grid
// We will divide the screen into a grid of cells.
// A particle in cell (cx, cy) only needs to check neighboring cells.
let grid = [];
let cellSize = maxRadius;
let cols = 0;
let rows = 0;

function updateGridSize() {
    let newCellSize = parseInt(radiusSlider.value);
    let newCols = Math.ceil(width / newCellSize);
    let newRows = Math.ceil(height / newCellSize);

    // Only reallocate if dimensions change to save GC overhead
    if (cellSize !== newCellSize || cols !== newCols || rows !== newRows) {
        cellSize = newCellSize;
        cols = newCols;
        rows = newRows;
        grid = new Array(cols * rows).fill(null).map(() => []);
    } else {
        // Just clear the existing arrays (much faster for Garbage Collector)
        for (let i = 0; i < grid.length; i++) {
            grid[i].length = 0;
        }
    }
}

function randomizeRules() {
    rules = [];
    for (let i = 0; i < colors.length; i++) {
        let row = [];
        for (let j = 0; j < colors.length; j++) {
            row.push(Math.random() * 2 - 1);
        }
        rules.push(row);
    }
}

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

function updateParticles() {
    friction = frictionSlider.value / 100;

    // Clear and populate spatial grid
    updateGridSize();

    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        let cx = Math.floor(p.x / cellSize);
        let cy = Math.floor(p.y / cellSize);
        // Ensure within bounds just in case
        cx = (cx + cols) % cols;
        cy = (cy + rows) % rows;
        grid[cy * cols + cx].push(p);
    }

    let maxRadSq = cellSize * cellSize;

    for (let i = 0; i < particles.length; i++) {
        let p1 = particles[i];
        let fx = 0;
        let fy = 0;

        let cx = Math.floor(p1.x / cellSize);
        let cy = Math.floor(p1.y / cellSize);

        // Check 9 neighboring cells (3x3), including wrapping for toroidal space
        for (let yOff = -1; yOff <= 1; yOff++) {
            for (let xOff = -1; xOff <= 1; xOff++) {

                let nx = (cx + xOff + cols) % cols;
                let ny = (cy + yOff + rows) % rows;
                let cellIndex = ny * cols + nx;
                let neighbors = grid[cellIndex];

                for (let j = 0; j < neighbors.length; j++) {
                    let p2 = neighbors[j];
                    if (p1 === p2) continue;

                    let dx = p1.x - p2.x;
                    let dy = p1.y - p2.y;

                    // Toroidal wrap distance
                    if (dx > width / 2) dx -= width;
                    else if (dx < -width / 2) dx += width;

                    if (dy > height / 2) dy -= height;
                    else if (dy < -height / 2) dy += height;

                    let d2 = dx * dx + dy * dy;

                    if (d2 > 0 && d2 < maxRadSq) {
                        let d = Math.sqrt(d2);
                        let force = rules[p1.colorIndex][p2.colorIndex];

                        // Collision avoidance
                        if (d < 5) {
                            force = 3;
                        }

                        let strength = force * (1 - d / cellSize);

                        fx += (dx / d) * strength;
                        fy += (dy / d) * strength;
                    }
                }
            }
        }

        p1.vx = (p1.vx + fx) * friction;
        p1.vy = (p1.vy + fy) * friction;

        let speed = Math.sqrt(p1.vx * p1.vx + p1.vy * p1.vy);
        if (speed > 15) {
            p1.vx = (p1.vx / speed) * 15;
            p1.vy = (p1.vy / speed) * 15;
        }
    }

    // Apply positions
    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0) p.x += width;
        else if (p.x >= width) p.x -= width;
        if (p.y < 0) p.y += height;
        else if (p.y >= height) p.y -= height;
    }
}

function drawParticles() {
    if (useTrails) {
        // Trails effect: draw a semi-transparent black rectangle over the previous frame
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.fillRect(0, 0, width, height);
    } else {
        ctx.clearRect(0, 0, width, height);
        // Ensure solid background if trails are off
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, width, height);
    }

    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        ctx.fillStyle = p.color;
        ctx.fillRect(p.x, p.y, 2, 2); // Slightly smaller particles to accommodate the huge count
    }
}

function loop(timestamp) {
    if (isRunning) {
        updateParticles();
        drawParticles();

        // Calculate FPS
        frameCount++;
        if (timestamp - lastTime >= 1000) {
            fpsCounter.textContent = `FPS: ${frameCount}`;
            frameCount = 0;
            lastTime = timestamp;
        }
    } else {
        lastTime = timestamp; // Prevent FPS spike when resuming
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
    // Clear trails immediately
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, width, height);
});

trailsCheckbox.addEventListener('change', (e) => {
    useTrails = e.target.checked;
    if (!useTrails) {
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, width, height);
    }
});

// Boot up
randomizeRules();
initParticles();
updateGridSize();

// Fill initial background
ctx.fillStyle = '#000';
ctx.fillRect(0, 0, width, height);

requestAnimationFrame(loop);
