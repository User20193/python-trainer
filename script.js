const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');

window.TILE_SIZE = 20;
window.width = canvas.width;
window.height = canvas.height;

// Map representation
const COLS = Math.floor(window.width / window.TILE_SIZE);
const ROWS = Math.floor(window.height / window.TILE_SIZE);

const EMPTY = 0;
const ROAD = 1;
const HOME = 2; // Blue
const WORK = 3; // Purple
const CAFE = 4; // Red
const PARK = 5; // Green

window.cityMap = [];
window.homes = [];
window.works = [];
window.cafes = [];
window.parks = [];

// Initialize map
for (let y = 0; y < ROWS; y++) {
    let row = [];
    for (let x = 0; x < COLS; x++) {
        row.push(EMPTY);
    }
    window.cityMap.push(row);
}

// Draw roads
for (let y = 5; y < ROWS - 5; y++) window.cityMap[y][Math.floor(COLS/2)] = ROAD;
for (let x = 5; x < COLS - 5; x++) window.cityMap[Math.floor(ROWS/2)][x] = ROAD;
for (let y = 10; y < ROWS - 10; y++) window.cityMap[y][Math.floor(COLS/4)] = ROAD;
for (let y = 10; y < ROWS - 10; y++) window.cityMap[y][Math.floor(COLS*3/4)] = ROAD;

// Function to add zones
function addZone(x, y, w, h, type, array) {
    for(let i = y; i < y + h; i++) {
        for(let j = x; j < x + w; j++) {
            if(i < ROWS && j < COLS) {
                window.cityMap[i][j] = type;
                array.push({x: j, y: i});
            }
        }
    }
}

// Add zones
addZone(2, 2, 4, 4, HOME, window.homes);
addZone(10, 2, 4, 4, HOME, window.homes);
addZone(COLS - 8, 2, 4, 4, HOME, window.homes);

addZone(2, ROWS - 8, 6, 6, WORK, window.works);
addZone(COLS - 10, ROWS - 8, 6, 6, WORK, window.works);

addZone(Math.floor(COLS/2) + 2, 5, 5, 5, CAFE, window.cafes);
addZone(Math.floor(COLS/4) + 2, Math.floor(ROWS/2) + 2, 6, 6, PARK, window.parks);

window.drawMap = function() {
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            let tile = window.cityMap[y][x];
            if (tile === EMPTY) ctx.fillStyle = '#1e1e2e';
            else if (tile === ROAD) ctx.fillStyle = '#313244';
            else if (tile === HOME) ctx.fillStyle = '#3b82f6';
            else if (tile === WORK) ctx.fillStyle = '#8b5cf6';
            else if (tile === CAFE) ctx.fillStyle = '#ef4444';
            else if (tile === PARK) ctx.fillStyle = '#22c55e';

            ctx.fillRect(x * window.TILE_SIZE, y * window.TILE_SIZE, window.TILE_SIZE, window.TILE_SIZE);

            // Draw grid
            ctx.strokeStyle = 'rgba(255,255,255,0.02)';
            ctx.strokeRect(x * window.TILE_SIZE, y * window.TILE_SIZE, window.TILE_SIZE, window.TILE_SIZE);
        }
    }
};

window.findPath = function(startX, startY, endX, endY) {
    let path = [];
    let currX = startX;
    let currY = startY;

    while (currX !== endX || currY !== endY) {
        if (currX < endX) currX++;
        else if (currX > endX) currX--;
        else if (currY < endY) currY++;
        else if (currY > endY) currY--;

        path.push({x: currX, y: currY});
    }
    return path;
};

const toggleBtn = document.getElementById('toggleBtn');
const speedBtn = document.getElementById('speedBtn');
const dayCountEl = document.getElementById('dayCount');
const clockTimeEl = document.getElementById('clockTime');

// Inspector UI
const inspectorPanel = document.getElementById('inspectorPanel');
const insHint = document.querySelector('.inspector-hint');
const insData = document.querySelector('.inspector-data');
const insName = document.getElementById('insName');
const insAction = document.getElementById('insAction');
const barEnergy = document.getElementById('barEnergy');
const barHunger = document.getElementById('barHunger');
const barSocial = document.getElementById('barSocial');
const insMoney = document.getElementById('insMoney');
const memoryLog = document.getElementById('memoryLog');

let isRunning = true;
let isFastForward = false;

window.weather = "Sunny";
window.weatherTimer = 0;
function updateWeather() {
    window.weatherTimer -= 5;
    if (window.weatherTimer <= 0) {
        if (Math.random() < 0.2) {
            window.weather = "Raining";
            window.weatherTimer = 180; // 3 hours of rain
        } else {
            window.weather = "Sunny";
            window.weatherTimer = 300;
        }
    }
}

let gameTime = 8 * 60; // Start at 08:00
let dayCount = 1;
let animationId;
let lastFrameTime = 0;

const NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank"];

class Person {
    constructor(id) {
        this.id = id;
        this.name = NAMES[id % NAMES.length];

        // Assign a random home
        let home = window.homes[Math.floor(Math.random() * window.homes.length)];
        this.x = home.x;
        this.y = home.y;
        this.home = home;

        // Needs (0 to 100)
        this.energy = 100;
        this.hunger = 100;
        this.social = 100;
        this.money = 50;

        // AI State

        // AI State
        this.currentAction = "Idle";
        this.path = [];
        this.target = null;
        this.memory = [];

        // Emergence stats/traits
        this.statusEffects = []; // e.g. "Cold", "Angry"
        this.inventory = [];

        // Relationships: person.id -> relationship value (-100 to 100)
        this.relationships = {};


        // Personality (Decay rates)
        this.decay = {
            energy: 0.05 + Math.random() * 0.05,
            hunger: 0.1 + Math.random() * 0.1,
            social: 0.08 + Math.random() * 0.08
        };

        this.log("Woke up in MiniVille.");
    }


    log(msg) {
        let timeStr = formatTime(gameTime);
        this.memory.unshift(`[${timeStr}] ${msg}`);
        if (this.memory.length > 8) this.memory.pop();
    }

    addStatus(status, duration) {
        let existing = this.statusEffects.find(s => s.name === status);
        if (existing) {
            existing.duration = Math.max(existing.duration, duration);
        } else {
            this.statusEffects.push({name: status, duration: duration});
            this.log(`Gained status: ${status}`);
        }
    }


    update() {
        // Decay needs over time
        let eDecay = this.decay.energy;
        if (this.statusEffects.find(s => s.name === "Sick")) eDecay *= 2.0; // Sickness drains energy

        this.energy -= eDecay;
        this.hunger -= this.decay.hunger;

        let sDecay = this.decay.social;
        if (this.statusEffects.find(s => s.name === "Angry")) sDecay *= 0.5; // Angry people don't want to talk as much
        this.social -= sDecay;

        // Clamp
        this.energy = Math.max(0, Math.min(100, this.energy));
        this.hunger = Math.max(0, Math.min(100, this.hunger));
        this.social = Math.max(0, Math.min(100, this.social));

        // Update statuses
        for (let i = this.statusEffects.length - 1; i >= 0; i--) {
            this.statusEffects[i].duration -= 5; // 5 mins per tick
            if (this.statusEffects[i].duration <= 0) {
                this.log(`Lost status: ${this.statusEffects[i].name}`);
                this.statusEffects.splice(i, 1);
            }
        }

        // Movement along path
        if (this.path && this.path.length > 0) {
            let nextStep = this.path[0];
            this.x = nextStep.x;
            this.y = nextStep.y;
            this.path.shift();
            return; // Busy walking
        }


        // Utility AI: Evaluate needs and pick action

        // Weather effects on emergence
        if (window.weather === "Raining" && this.currentAction !== "Sleeping" && this.currentAction !== "Working" && this.currentAction !== "Eating at Cafe") {
             if (Math.random() < 0.05) {
                 this.addStatus("Sick", 200);
                 this.log("Got sick from the rain.");
             }
        }

        this.decideAction();

    }


    decideAction() {
        let hour = Math.floor(gameTime / 60);
        let action = "Idle";
        let targetLocation = null;
        let highestUtility = 0;

        // 1. SLEEP (High priority if energy is low or it's late night)
        let sleepUtility = (100 - this.energy) * 1.5;
        if (hour >= 22 || hour < 6) sleepUtility += 100; // Go home at night
        if (sleepUtility > highestUtility) {
            highestUtility = sleepUtility;
            action = "Sleeping";
            targetLocation = this.home;
        }

        // 2. EAT (High priority if hunger is low)
        let eatUtility = (100 - this.hunger) * 2;
        if (this.money < 10) eatUtility -= 50; // Can't afford cafe
        if (eatUtility > highestUtility && eatUtility > 50) {
            highestUtility = eatUtility;
            action = "Eating at Cafe";
            targetLocation = window.cafes[Math.floor(Math.random() * window.cafes.length)];
        }

        // 3. WORK (Priority during work hours if needs are somewhat met)
        let workUtility = 0;
        if (hour >= 9 && hour <= 17 && this.energy > 30 && this.hunger > 30) {
            workUtility = 80;
        }
        if (workUtility > highestUtility) {
            highestUtility = workUtility;
            action = "Working";
            targetLocation = window.works[Math.floor(Math.random() * window.works.length)];
        }

        // 4. SOCIALIZE (If lonely and free time)
        let socialUtility = (100 - this.social) * 1.2;
        if (hour >= 18 && hour <= 21) socialUtility += 30; // Evening in park
        if (socialUtility > highestUtility && socialUtility > 40) {
            highestUtility = socialUtility;
            action = "Socializing in Park";
            targetLocation = window.parks[Math.floor(Math.random() * window.parks.length)];
        }

        // Execution of Action
        if (this.currentAction !== action) {
            this.currentAction = action;
            this.log(`Decided to: ${action}`);

            // Generate path if target is different from current location
            if (targetLocation && (this.x !== targetLocation.x || this.y !== targetLocation.y)) {
                this.path = window.findPath(this.x, this.y, targetLocation.x, targetLocation.y);
                // Remove first step if it's current position
                if (this.path && this.path.length > 0 && this.path[0].x === this.x && this.path[0].y === this.y) {
                    this.path.shift();
                }
            }
        } else {

            // Arrived at destination, perform action effects
            if (action === "Sleeping") {
                this.energy += 5;
                if (this.statusEffects.find(s => s.name === "Sick")) this.energy += 2; // Sleep helps sickness
            }
            if (action === "Eating at Cafe") {
                this.hunger += 10;
                this.money -= 0.5;
                // Chance to get sick from cafe
                if (Math.random() < 0.01) {
                    this.addStatus("Sick", 120); // Sick for 2 hours
                }
            }
            if (action === "Working") {
                this.money += 2;
                this.energy -= 0.1;
                this.social -= 0.1;
                if (this.statusEffects.find(s => s.name === "Angry")) {
                    this.money -= 1; // Angry workers perform poorly
                }
            }

            // Emergent Interactions Engine
            let othersHere = people.filter(p => p !== this && p.x === this.x && p.y === this.y && p.currentAction === this.currentAction);

            if (action === "Socializing in Park" || othersHere.length > 0) {
                this.social += 5;

                for (let other of othersHere) {
                    let rel = this.relationships[other.id] || 0;

                    // Condition 1: Both are hungry and one has food (simulated by money right now)
                    if (this.hunger < 30 && other.hunger < 30 && other.money > 20 && this.money < 10 && action !== "Working") {
                        if (Math.random() < 0.1) {
                            this.log(`Begged ${other.name} for food.`);
                            this.hunger += 30;
                            other.money -= 10;
                            this.relationships[other.id] = rel - 5; // They don't like beggars
                            other.addStatus("Annoyed", 60);
                        }
                    }

                    // Condition 2: Angry person meets someone
                    if (this.statusEffects.find(s => s.name === "Angry")) {
                        if (Math.random() < 0.2) {
                            this.log(`Yelled at ${other.name}!`);
                            other.addStatus("Angry", 120); // Spread anger
                            this.relationships[other.id] = rel - 15;
                            this.statusEffects = this.statusEffects.filter(s => s.name !== "Angry"); // Relieved anger
                            this.log("Felt better after yelling.");
                        }
                    }
                    // Condition 3: Normal chat
                    else if (Math.random() < 0.1) {
                        if (rel > 10) {
                            this.log(`Had a wonderful chat with friend ${other.name}.`);
                            this.social += 15;
                            this.energy += 2; // Good chats energize
                        } else if (other.statusEffects.find(s => s.name === "Sick")) {
                             this.log(`Talked to ${other.name}, but they sneezed on me.`);
                             if (Math.random() < 0.5) this.addStatus("Sick", 180);
                        } else {
                            this.log(`Had a chat with ${other.name}.`);
                            this.social += 10;
                            this.relationships[other.id] = rel + 2;
                        }
                    }

                    // Random argument
                    if (Math.random() < 0.005) {
                        this.log(`Got into a fight with ${other.name}!`);
                        this.addStatus("Angry", 120);
                        other.addStatus("Angry", 120);
                        this.relationships[other.id] = rel - 20;
                    }

                    break; // Interact with one person at a time
                }
            }

        }
    }

    draw(ctx) {
        // Draw person as a circle
        ctx.beginPath();
        ctx.arc(this.x * window.TILE_SIZE + window.TILE_SIZE / 2,
                this.y * window.TILE_SIZE + window.TILE_SIZE / 2,
                window.TILE_SIZE / 3, 0, Math.PI * 2);

        if (selectedPerson === this) {
            ctx.fillStyle = '#fcd34d'; // Highlight selected
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 2;
        } else {
            ctx.fillStyle = '#cbd5e1';
            ctx.strokeStyle = '#333';
            ctx.lineWidth = 1;
        }

        ctx.fill();
        ctx.stroke();

        // Draw emoji bubble based on action
        let emoji = "";
        if (this.currentAction === "Sleeping") emoji = "💤";
        if (this.currentAction === "Eating at Cafe") emoji = "🍔";
        if (this.currentAction === "Working") emoji = "💼";
        if (this.currentAction === "Socializing in Park") emoji = "💬";

        if (emoji) {
            ctx.font = "16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(emoji, this.x * window.TILE_SIZE + window.TILE_SIZE / 2,
                               this.y * window.TILE_SIZE + 10);
        }
    }
}

let people = [];
let selectedPerson = null;

function init() {
    people = [];
    for (let i = 0; i < 15; i++) {
        people.push(new Person(i));
    }
}

function formatTime(minutes) {
    let h = Math.floor(minutes / 60) % 24;
    let m = Math.floor(minutes % 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}`;
}


function updateInspector() {
    if (selectedPerson) {
        insHint.style.display = 'none';
        insData.style.display = 'block';

        insName.textContent = selectedPerson.name;

        let statuses = selectedPerson.statusEffects.map(s => s.name).join(", ");
        let statStr = statuses ? ` [${statuses}]` : "";
        insAction.textContent = selectedPerson.currentAction + statStr;

        barEnergy.style.width = `${selectedPerson.energy}%`;
        barHunger.style.width = `${selectedPerson.hunger}%`;
        barSocial.style.width = `${selectedPerson.social}%`;

        // Colors based on level
        barEnergy.style.backgroundColor = selectedPerson.energy < 30 ? '#ef4444' : '#3b82f6';
        barHunger.style.backgroundColor = selectedPerson.hunger < 30 ? '#ef4444' : '#22c55e';
        barSocial.style.backgroundColor = selectedPerson.social < 30 ? '#ef4444' : '#f97316';

        insMoney.textContent = Math.floor(selectedPerson.money);

        memoryLog.innerHTML = "";
        for (let log of selectedPerson.memory) {
            let li = document.createElement('li');
            li.textContent = log;
            memoryLog.appendChild(li);
        }
    } else {
        insHint.style.display = 'block';
        insData.style.display = 'none';
    }
}

function gameLoop(timestamp) {
    if (isRunning) {
        let timeStep = timestamp - lastFrameTime;
        let updateInterval = isFastForward ? 50 : 200; // ms per game tick

        if (timeStep > updateInterval) {
            gameTime += 5; // advance 5 minutes per tick

            if (gameTime >= 24 * 60) {
                gameTime = 0;
                dayCount++;
            }

            updateWeather();

            dayCountEl.textContent = dayCount;
            clockTimeEl.textContent = formatTime(gameTime) + ` (${window.weather})`;


            for (let p of people) {
                p.update();
            }

            updateInspector();
            lastFrameTime = timestamp;
        }
    } else {
        lastFrameTime = timestamp; // prevent jump when unpausing
    }

    // Render
    ctx.clearRect(0, 0, window.width, window.height);
    window.drawMap();

    // Sort people by Y so they draw nicely
    people.sort((a,b) => a.y - b.y);
    for (let p of people) {
        p.draw(ctx);
    }

    animationId = requestAnimationFrame(gameLoop);
}

// Events
toggleBtn.addEventListener('click', () => {
    isRunning = !isRunning;
    toggleBtn.textContent = isRunning ? "Pause" : "Start";
});

speedBtn.addEventListener('click', () => {
    isFastForward = !isFastForward;
    if (isFastForward) {
        speedBtn.classList.add('active-fast');
        speedBtn.textContent = "Normal Speed ⏯️";
    } else {
        speedBtn.classList.remove('active-fast');
        speedBtn.textContent = "Fast Forward ⏩";
    }
});

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const clickY = e.clientY - rect.top;

    let gridX = Math.floor(clickX / window.TILE_SIZE);
    let gridY = Math.floor(clickY / window.TILE_SIZE);

    selectedPerson = null;
    for (let p of people) {
        if (p.x === gridX && p.y === gridY) {
            selectedPerson = p;
            break;
        }
    }
    updateInspector();
});

// Boot up
init();
lastFrameTime = performance.now();
requestAnimationFrame(gameLoop);