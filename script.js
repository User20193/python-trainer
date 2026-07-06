
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
const HOSPITAL = 6; // Pink
const SHOP = 7; // Cyan
const CITY_HALL = 10; // Gold
const WALL = 8; // Impassable wall
const DOOR = 9; // Passable door

window.cityMap = [];
window.homes = [];
window.works = [];
window.cafes = [];
window.parks = [];
window.hospitals = [];
window.shops = [];
window.cityHalls = [];



// Initialize map
for (let y = 0; y < ROWS; y++) {
    let row = [];
    for (let x = 0; x < COLS; x++) {
        row.push(EMPTY);
    }
    window.cityMap.push(row);
}

// Draw main roads
for (let y = 4; y < ROWS - 4; y++) {
    window.cityMap[y][Math.floor(COLS/2)] = ROAD;
    window.cityMap[y][Math.floor(COLS/2) - 1] = ROAD;
}
for (let x = 4; x < COLS - 4; x++) {
    window.cityMap[Math.floor(ROWS/2)][x] = ROAD;
    window.cityMap[Math.floor(ROWS/2) - 1][x] = ROAD;
}
for (let y = 10; y < ROWS - 10; y++) {
    window.cityMap[y][Math.floor(COLS/4)] = ROAD;
    window.cityMap[y][Math.floor(COLS*3/4)] = ROAD;
}
for (let x = 10; x < COLS - 10; x++) {
    window.cityMap[Math.floor(ROWS/4)][x] = ROAD;
    window.cityMap[Math.floor(ROWS*3/4)][x] = ROAD;
}

// Function to add zones with walls and doors
function addBuilding(x, y, w, h, type, array) {
    for(let i = y; i < y + h; i++) {
        for(let j = x; j < x + w; j++) {
            if(i < ROWS && j < COLS) {
                if (i === y || i === y + h - 1 || j === x || j === x + w - 1) {
                    window.cityMap[i][j] = WALL;
                } else {
                    window.cityMap[i][j] = type;
                    array.push({x: j, y: i});
                }
            }
        }
    }
    if (y + h - 1 < ROWS && x + Math.floor(w/2) < COLS) {
        window.cityMap[y + h - 1][x + Math.floor(w/2)] = DOOR;
        array.push({x: x + Math.floor(w/2), y: y + h - 1});
    }
}

function addPark(x, y, w, h, array) {
    for(let i = y; i < y + h; i++) {
        for(let j = x; j < x + w; j++) {
            if(i < ROWS && j < COLS) {
                window.cityMap[i][j] = PARK;
                array.push({x: j, y: i});
            }
        }
    }
}

// Add Buildings
addBuilding(3, 3, 6, 6, HOME, window.homes);
addBuilding(COLS - 9, 3, 6, 6, HOME, window.homes);
addBuilding(3, ROWS - 9, 6, 6, HOME, window.homes);
addBuilding(Math.floor(COLS/4) + 2, Math.floor(ROWS/4) + 2, 5, 5, HOME, window.homes);

addBuilding(COLS - 15, ROWS - 15, 10, 10, WORK, window.works);

addBuilding(12, Math.floor(ROWS/2) + 2, 8, 8, WORK, window.works);

// City Hall in the center-ish
addBuilding(Math.floor(COLS/2) - 4, Math.floor(ROWS/2) - 4, 10, 10, CITY_HALL, window.cityHalls);


addBuilding(Math.floor(COLS/2) + 3, 5, 8, 8, CAFE, window.cafes);
addBuilding(5, Math.floor(ROWS/4) + 2, 7, 7, HOSPITAL, window.hospitals);
addBuilding(Math.floor(COLS*3/4) + 2, Math.floor(ROWS/2) + 2, 8, 8, SHOP, window.shops);

addPark(Math.floor(COLS/4) + 3, Math.floor(ROWS*3/4) + 3, 9, 9, window.parks);




let offscreenCanvas = document.createElement('canvas');
let offCtx = offscreenCanvas.getContext('2d');
let mapNeedsRedraw = true;

window.drawMap = function() {
    if (mapNeedsRedraw) {
        offscreenCanvas.width = window.width;
        offscreenCanvas.height = window.height;
        let hour = gameTime / 60;
        let isNight = hour < 7 || hour > 19;

        for (let y = 0; y < ROWS; y++) {
            for (let x = 0; x < COLS; x++) {
                let tile = window.cityMap[y][x];
                let px = x * window.TILE_SIZE;
                let py = y * window.TILE_SIZE;

                if (tile === EMPTY) {
                    offCtx.fillStyle = '#1e1e2e';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    if ((x*y) % 7 === 0) {
                        offCtx.fillStyle = '#262638';
                        offCtx.fillRect(px + 4, py + 4, 4, 4);
                    }
                }
                else if (tile === ROAD) {
                    offCtx.fillStyle = '#313244';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = '#45475a';
                    if (x % 2 === 0 && window.cityMap[y][x-1] === ROAD && window.cityMap[y][x+1] === ROAD) {
                        offCtx.fillRect(px + window.TILE_SIZE/4, py + window.TILE_SIZE/2 - 1, window.TILE_SIZE/2, 2);
                    }
                    if (y % 2 === 0 && window.cityMap[y-1] && window.cityMap[y-1][x] === ROAD && window.cityMap[y+1] && window.cityMap[y+1][x] === ROAD) {
                        offCtx.fillRect(px + window.TILE_SIZE/2 - 1, py + window.TILE_SIZE/4, 2, window.TILE_SIZE/2);
                    }
                }
                else if (tile === HOME) {
                    offCtx.fillStyle = '#3b82f6';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = 'rgba(0,0,0,0.2)';
                    offCtx.fillRect(px, py + window.TILE_SIZE/2, window.TILE_SIZE, window.TILE_SIZE/2);
                    if (isNight) {
                        offCtx.fillStyle = '#fde047';
                        offCtx.fillRect(px + 4, py + 4, 6, 6);
                    }
                }
                else if (tile === WORK) {
                    offCtx.fillStyle = '#8b5cf6';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = 'rgba(255,255,255,0.1)';
                    offCtx.fillRect(px + 2, py + 2, window.TILE_SIZE - 4, window.TILE_SIZE - 4);
                }
                else if (tile === CAFE) {
                    offCtx.fillStyle = '#ef4444';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = '#ffffff';
                    offCtx.fillRect(px, py, window.TILE_SIZE, 4);
                    if (isNight) {
                        offCtx.fillStyle = '#fde047';
                        offCtx.fillRect(px + 4, py + 8, window.TILE_SIZE - 8, 8);
                    }
                }
                else if (tile === PARK) {
                    offCtx.fillStyle = '#22c55e';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    if ((x+y) % 2 === 0) {
                        offCtx.fillStyle = '#16a34a';
                        offCtx.beginPath();
                        offCtx.arc(px + window.TILE_SIZE/2, py + window.TILE_SIZE/2, window.TILE_SIZE/3, 0, Math.PI*2);
                        offCtx.fill();
                        offCtx.fillStyle = 'rgba(0,0,0,0.2)';
                        offCtx.beginPath();
                        offCtx.arc(px + window.TILE_SIZE/2 + 2, py + window.TILE_SIZE/2 + 2, window.TILE_SIZE/3, 0, Math.PI*2);
                        offCtx.fill();
                    }
                }
                else if (tile === HOSPITAL) {
                    offCtx.fillStyle = '#f43f5e';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = '#ffffff';
                    offCtx.fillRect(px + window.TILE_SIZE/2 - 2, py + 4, 4, window.TILE_SIZE - 8);
                    offCtx.fillRect(px + 4, py + window.TILE_SIZE/2 - 2, window.TILE_SIZE - 8, 4);
                }

                else if (tile === SHOP) {
                    offCtx.fillStyle = '#0ea5e9';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                }
                else if (tile === CITY_HALL) {
                    offCtx.fillStyle = '#ca8a04'; // Dark gold
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = '#eab308'; // Light gold border
                    offCtx.fillRect(px + 4, py + 4, window.TILE_SIZE - 8, window.TILE_SIZE - 8);
                }
                else if (tile === WALL) {
                    offCtx.fillStyle = '#475569';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = '#64748b';
                    offCtx.fillRect(px, py, window.TILE_SIZE, 4);
                    if (window.cityMap[y+1] && window.cityMap[y+1][x] !== WALL) {
                        offCtx.fillStyle = 'rgba(0,0,0,0.4)';
                        offCtx.fillRect(px, py + window.TILE_SIZE, window.TILE_SIZE, 4);
                    }
                }
                else if (tile === DOOR) {
                    offCtx.fillStyle = '#8b5cf6';
                    offCtx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                    offCtx.fillStyle = '#1e1e2e';
                    offCtx.fillRect(px + 4, py + 4, window.TILE_SIZE - 8, window.TILE_SIZE - 8);
                }

                offCtx.strokeStyle = 'rgba(255,255,255,0.02)';
                offCtx.strokeRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
            }
        }
        mapNeedsRedraw = false;
    }
    ctx.drawImage(offscreenCanvas, 0, 0);
};


window.findPath = function(startX, startY, endX, endY) {
    let queue = [{x: startX, y: startY, path: []}];
    let visited = new Set();
    visited.add(startX + "," + startY);

    while (queue.length > 0) {
        let curr = queue.shift();
        if (curr.x === endX && curr.y === endY) return curr.path;

        let dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]];
        dirs.sort(() => Math.random() - 0.5);

        for (let d of dirs) {
            let nx = curr.x + d[0];
            let ny = curr.y + d[1];

            if (nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS) {
                if (!visited.has(nx + "," + ny)) {
                    if (window.cityMap[ny][nx] !== WALL) {
                        visited.add(nx + "," + ny);
                        queue.push({x: nx, y: ny, path: [...curr.path, {x: nx, y: ny}]});
                    }
                }
            }
        }
    }

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

window.weather = "Солнечно";
window.weatherTimer = 0;
function updateWeather() {
    window.weatherTimer -= 5;
    if (window.weatherTimer <= 0) {
        if (Math.random() < 0.2) {
            window.weather = "Дождь";
            window.weatherTimer = 180; // 3 hours of rain
        } else {
            window.weather = "Солнечно";
            window.weatherTimer = 300;
        }
    }
}

let gameTime = 8 * 60; // Start at 08:00
let dayCount = 1;

let animationId;
let lastFrameTime = 0;

// Election System
let currentMayor = null;
let electionDay = 3; // First election on day 3
let candidates = [];
let isElectionDay = false;

function announce(msg, durationTicks = 120) {
    let banner = document.getElementById('announcementBanner');
    if (banner) {
        banner.style.display = 'block';
        banner.innerHTML = "📣 " + msg;
        setTimeout(() => {
            banner.style.display = 'none';
        }, durationTicks * (isFastForward ? 50 : 200));
    }
}

function handleElections() {
    let hour = Math.floor(gameTime / 60);

    // Start of election day (08:00)
    if (dayCount === electionDay && hour === 8 && !isElectionDay) {
        isElectionDay = true;

        // Pick 3 random candidates who are not currently mayor
        let eligible = people.filter(p => p !== currentMayor);
        eligible.sort(() => Math.random() - 0.5);
        candidates = eligible.slice(0, 3);


        candidates.forEach(c => {
            c.isCandidate = true;
            c.partyName = generatePartyName();
            c.votes = 0;
            c.log("Выдвинул кандидатуру от " + c.partyName);
        });

        document.getElementById('electionPanel').style.display = 'block';
        updateElectionUI();

        announce(`Выборы начались! Кандидаты: ${candidates.map(c => c.name).join(", ")}`, 300);

    }

    // End of election day / Voting time (20:00)
    if (isElectionDay && hour === 20) {
        isElectionDay = false;

        let votes = {};
        candidates.forEach(c => votes[c.id] = 0);

        // Everyone votes
        people.forEach(voter => {
            let bestCandidate = null;
            let bestScore = -999;

            candidates.forEach(c => {
                let score = 0;
                // Voters like friends
                if (voter.relationships[c.id]) score += voter.relationships[c.id];
                // Voters respect wealth (bribes/success)
                score += c.money * 0.5;
                // Self vote
                if (voter === c) score += 999;

                if (score > bestScore) {
                    bestScore = score;
                    bestCandidate = c;
                }
            });


            if (bestCandidate) {
                votes[bestCandidate.id]++;
                bestCandidate.votes++; // For UI
                if(voter !== bestCandidate) voter.log(`Проголосовал за ${bestCandidate.name}.`);
            }
        });

        updateElectionUI();


        // Count votes
        let winner = candidates[0];
        let maxVotes = -1;
        for (let cid in votes) {
            if (votes[cid] > maxVotes) {
                maxVotes = votes[cid];
                winner = people.find(p => p.id == cid);
            }
        }

        // Demote old mayor
        if (currentMayor && currentMayor !== winner) {
            currentMayor.profession = "Безработный";
            currentMayor.workplace = null;
            currentMayor.pixels[1] = [currentMayor.skinColor, currentMayor.baseColor, currentMayor.baseColor, currentMayor.skinColor]; // Reset clothes
            currentMayor.log("Проиграл выборы. Сложил полномочия.");
        }

        // Promote new mayor
        currentMayor = winner;
        currentMayor.profession = "Мэр";
        currentMayor.workplace = window.cityHalls[0]; // Mayor works at City Hall

        // Mayor gets a golden jacket!
        let gold = '#eab308';
        for(let i=1; i<3; i++) {
             for(let j=1; j<3; j++) {
                 currentMayor.pixels[i][j] = gold;
             }
        }

        currentMayor.log("УРА! Я стал новым Мэром!");
        announce(`${currentMayor.fio} избран новым Мэром (${maxVotes} голосов)!`, 400);

        // Clear candidates
        candidates.forEach(c => c.isCandidate = false);
        candidates = [];


        document.getElementById('electionPanel').style.display = 'none';

        // Next election in 3 days

        electionDay += 3;
    }
}




// Procedural Semantic Dialogue Engine
const DICTIONARY = {
    work: {
        subjects: ["Начальник", "Клиент", "Проект", "Отчет", "График", "Офис", "Коллега", "Компьютер"],
        verbs: ["сломал", "закрыл", "проверил", "уничтожил", "потерял", "нашел", "забыл"],
        objects: ["зарплату", "документы", "смысл", "время", "файлы", "задачу", "кассу"]
    },
    food: {
        subjects: ["Повар", "Официант", "Рецепт", "Борщ", "Майонез", "Сыр", "Пицца"],
        verbs: ["пересолил", "сварил", "съел", "выплюнул", "пожарил", "купил", "украл"],
        objects: ["кастрюлю", "макароны", "котлету", "вкус", "аппетит", "рыбу", "хлеб"]
    },
    general: {
        subjects: ["Кот", "Сосед", "Мэр", "Телевизор", "Космонавт", "Динозавр", "Трактор", "Смысл жизни"],
        verbs: ["прыгает на", "смотрит на", "жует", "ищет", "разрушает", "любит", "ненавидит"],
        objects: ["забор", "диван", "тапочки", "космос", "квант", "гвоздь", "безумие"]
    }
};

function generateDialogue(theme = "general") {
    let dict = DICTIONARY[theme] || DICTIONARY.general;
    let pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
    let subject = pick(dict.subjects);
    let verb = pick(dict.verbs);
    let obj = pick(dict.objects);
    let punctuation = Math.random() > 0.7 ? "!" : (Math.random() > 0.5 ? "?" : ".");
    return `${subject} ${verb} ${obj}${punctuation}`;
}

const NAMES_FIRST = ["Иван", "Александр", "Дмитрий", "Сергей", "Андрей", "Алексей", "Максим", "Евгений", "Михаил", "Владимир", "Анна", "Мария", "Елена", "Дарья", "Ольга", "Екатерина", "Наталья", "Татьяна", "Юлия", "Анастасия"];
const NAMES_LAST = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов", "Михайлов", "Новиков", "Федоров", "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев"];
const NAMES_PATRO = ["Иванович", "Александрович", "Дмитриевич", "Сергеевич", "Андреевич", "Алексеевич", "Максимович", "Евгеньевич", "Михайлович", "Владимирович"];
const NAMES_PATRO_F = ["Ивановна", "Александровна", "Дмитриевна", "Сергеевна", "Андреевна", "Алексеевна", "Максимовна", "Евгеньевна", "Михайловна", "Владимировна"];


function generatePartyName() {
    let adjs = ["Святого", "Квадратного", "Жидкого", "Золотого", "Тайного", "Мокрого", "Великого", "Быстрого", "Ржавого", "Липкого", "Бодрого", "Соленого", "Эпичного"];
    let nouns = ["Борща", "Капибары", "Кванта", "Майонеза", "Тапочка", "Динозавра", "Кефира", "Трактора", "Сырка", "Безумия", "Бетона", "Пельменя"];

    let adj = adjs[Math.floor(Math.random() * adjs.length)];
    let noun = nouns[Math.floor(Math.random() * nouns.length)];

    let prefix = Math.random() > 0.5 ? "Партия" : "Движение";

    return `${prefix} ${adj} ${noun}`;
}


function generateFIO() {
    let first = NAMES_FIRST[Math.floor(Math.random() * NAMES_FIRST.length)];
    let last = NAMES_LAST[Math.floor(Math.random() * NAMES_LAST.length)];
    let isFemale = first.endsWith('а') || first.endsWith('я');
    if (isFemale && !last.endsWith('а') && !last.endsWith('в')) {
         if(last.endsWith('ов') || last.endsWith('ев') || last.endsWith('ин')) {
             last += 'а';
         }
    } else if (isFemale && (last.endsWith('ов') || last.endsWith('ев'))) {
         last += 'а';
    }
    let patro = isFemale ? NAMES_PATRO_F[Math.floor(Math.random() * NAMES_PATRO_F.length)] : NAMES_PATRO[Math.floor(Math.random() * NAMES_PATRO.length)];
    return `${last} ${first} ${patro}`;
}


class Person {
    constructor(id) {
        this.id = id;
        let home = window.homes[Math.floor(Math.random() * window.homes.length)];
        this.x = home.x;
        this.y = home.y;
        this.home = home;

        this.fio = generateFIO();
        this.name = this.fio.split(" ")[1] || this.fio;
        this.age = Math.floor(Math.random() * 50) + 18;

        this.pixels = [];
        let baseColor = `hsl(${Math.random() * 360}, 70%, 60%)`;
        let accentColor = `hsl(${Math.random() * 360}, 80%, 40%)`;
        let skinColor = Math.random() > 0.5 ? '#fcd34d' : '#f87171';
        this.skinColor = skinColor;
        this.baseColor = baseColor;

        this.profession = "Безработный";
        this.workplace = null;
        if (id % 3 === 0) {
            this.profession = "Офис-менеджер";
            this.workplace = window.works[Math.floor(Math.random() * window.works.length)];
        } else if (id % 3 === 1) {
            this.profession = "Врач";
            this.workplace = window.hospitals[Math.floor(Math.random() * window.hospitals.length)];
            baseColor = '#ffffff';
        } else {
            this.profession = "Продавец";
            this.workplace = window.shops[Math.floor(Math.random() * window.shops.length)];
            baseColor = '#0ea5e9';
        }

        for (let i = 0; i < 4; i++) {
            let row = [];
            for (let j = 0; j < 4; j++) {
                if (i === 0 && (j === 1 || j === 2)) row.push(skinColor);
                else if (i === 1) row.push(baseColor);
                else if (i === 2 && (j === 1 || j === 2)) row.push(baseColor);
                else if (i === 2 && (j === 0 || j === 3)) row.push(skinColor);
                else if (i === 3 && (j === 1 || j === 2)) row.push(accentColor);
                else row.push('transparent');
            }
            this.pixels.push(row);
        }


        // Visual Coordinates for Lerp
        this.visualX = this.x;
        this.visualY = this.y;


        // Needs (0 to 100)
        this.energy = 100;
        this.hunger = 100;
        this.social = 100;
        this.money = 50;

        // AI State

        // AI State
        this.currentAction = "Безделье";
        this.path = [];
        this.target = null;
        this.memory = [];
        this.speechBubble = "";
        this.speechTimer = 0;
        this.chatTimer = 0;
        this.chatTarget = null;

        // Emergence stats/traits
        this.statusEffects = []; // e.g. "Cold", "Злой"
        this.inventory = [];

        // Relationships: person.id -> relationship value (-100 to 100)
        this.relationships = {};


        // Personality (Decay rates)
        this.decay = {
            energy: 0.05 + Math.random() * 0.05,
            hunger: 0.1 + Math.random() * 0.1,
            social: 0.08 + Math.random() * 0.08
        };

        this.log("Проснулся в Лисеу-Сити.");
    }



    say(text) {
        this.speechBubble = text;
        this.speechTimer = 150; // Show for about 3 seconds in-game time ticks
        this.log(`Сказал: "${text}"`);
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
            this.log(`Получен статус: ${status}`);
        }
    }



    update() {
        if (this.speechTimer > 0) this.speechTimer -= 5;

        // Chatting state takes priority over movement and needs decay
        if (this.chatTimer > 0) {
            this.chatTimer -= 5;
            this.currentAction = "Разговор";
            // Occasionally say something new while chatting
            if (Math.random() < 0.1) {
                this.say(generateDialogue(this.chatTheme || "general"));
            }
            // Ensure target is also staying
            if (this.chatTarget && this.chatTarget.chatTimer <= 0) {
                this.chatTarget = null;
                this.chatTimer = 0; // End chat if partner leaves
            }
            return;
        }

        // Decay needs over time

        let eDecay = this.decay.energy;
        if (this.statusEffects.find(s => s.name === "Болен")) eDecay *= 2.0; // Sickness drains energy

        this.energy -= eDecay;
        this.hunger -= this.decay.hunger;

        let sDecay = this.decay.social;
        if (this.statusEffects.find(s => s.name === "Злой")) sDecay *= 0.5; // Angry people don't want to talk as much
        this.social -= sDecay;

        // Clamp
        this.energy = Math.max(0, Math.min(100, this.energy));
        this.hunger = Math.max(0, Math.min(100, this.hunger));
        this.social = Math.max(0, Math.min(100, this.social));

        // Update statuses
        for (let i = this.statusEffects.length - 1; i >= 0; i--) {
            this.statusEffects[i].duration -= 5; // 5 mins per tick
            if (this.statusEffects[i].duration <= 0) {
                this.log(`Потерян статус: ${this.statusEffects[i].name}`);
                this.statusEffects.splice(i, 1);
            }
        }


        // Movement along path
        if (this.path && this.path.length > 0) {
            let nextStep = this.path[0];
            this.x = nextStep.x;
            this.y = nextStep.y;
            this.path.shift();

            // Dynamic Encounters on the road!
            this.checkDynamicEncounters();

            return; // Busy walking
        }



        // Utility AI: Evaluate needs and pick action

        // Weather effects on emergence
        if (window.weather === "Дождь" && this.currentAction !== "Сон" && this.currentAction !== "Работа" && this.currentAction !== "Ест в кафе") {
             if (Math.random() < 0.05) {
                 this.addStatus("Болен", 200);
                 this.log("Заболел из-за дождя.");
             }
        }

        this.decideAction();

    }





    checkDynamicEncounters() {
        if (this.chatTimer > 0) return;

        let othersHere = people.filter(p => p !== this && Math.abs(p.x - this.x) <= 1 && Math.abs(p.y - this.y) <= 1);
        for (let other of othersHere) {
            if (other.chatTimer > 0) continue;

            let rel = this.relationships[other.id] || 0;

            // CAMPAIGNING MECHANICS
            if (this.isCandidate) {
                // 1. Black PR / Debates against other candidates
                if (other.isCandidate && Math.random() < 0.6) {
                    this.log(`Устроил публичные дебаты с ${other.name}!`);
                    this.say(`Твоя ${other.partyName} - это позор!`);
                    other.say(`Сам такой!`);
                    this.relationships[other.id] = rel - 30;
                    other.relationships[this.id] = (other.relationships[this.id] || 0) - 30;
                    this.addStatus("Злой", 60);

                    // Bystanders react
                    let bystanders = people.filter(p => p !== this && p !== other && Math.abs(p.x - this.x) <= 3 && Math.abs(p.y - this.y) <= 3);
                    bystanders.forEach(b => {
                         if (Math.random() > 0.5) {
                             b.relationships[this.id] = (b.relationships[this.id] || 0) + 10;
                             b.say(`${this.name} прав!`);
                         } else {
                             b.relationships[other.id] = (b.relationships[other.id] || 0) + 10;
                             b.say(`${other.name} лучше!`);
                         }
                    });

                    this.startChat(other, 60, "general");
                    return;
                }

                // 2. Bribery!
                if (!other.isCandidate && this.money > 25 && Math.random() < 0.3) {
                    this.log(`Дал взятку ${other.name} за голос.`);
                    this.say("Голосуй за меня, вот деньги!");
                    other.say("Ого, спасибо!");
                    this.money -= 10;
                    other.money += 10;
                    this.relationships[other.id] = rel + 50; // Bought their love
                    other.relationships[this.id] = (other.relationships[this.id] || 0) + 50;
                    this.startChat(other, 30, "general");
                    return;
                }

                // 3. Campaigning slogans
                if (!other.isCandidate && Math.random() < 0.5) {
                    this.log(`Агитировал ${other.name}.`);
                    this.say(`Голосуй за ${this.partyName}!`);
                    other.say("Я подумаю...");
                    this.relationships[other.id] = rel + 10;
                    other.relationships[this.id] = (other.relationships[this.id] || 0) + 10;
                    this.startChat(other, 40, "general");
                    return;
                }
            }


            if (rel > 10 && Math.random() < 0.4) {
                this.log(`Случайно встретил друга ${other.name}!`);
                let theme = (this.profession === other.profession && this.profession !== "Безработный") ? "work" : "general";
                this.startChat(other, 80, theme);
                return;
            }

            if (rel < -10 && Math.random() < 0.5) {
                this.log(`Увидел врага ${other.name} и завязалась драка!`);
                this.energy -= 10;
                other.energy -= 10;
                this.addStatus("Злой", 100);
                other.addStatus("Злой", 100);

                this.say("Я тебя ненавижу!");
                other.say("Сам такой!");

                this.currentAction = "Бегство";
                this.target = this.home;
                this.path = window.findPath(this.x, this.y, this.home.x, this.home.y);

                other.currentAction = "Бегство";
                other.target = other.home;
                other.path = window.findPath(other.x, other.y, other.home.x, other.home.y);
                return;
            }

            if (this.hunger < 30 && this.money < 10 && other.money > 20 && Math.random() < 0.2) {
                this.log(`Украл деньги у ${other.name} от отчаяния!`);
                this.say(generateDialogue("food"));
                other.say("Эй! Отдай!");
                this.money += 15;
                other.money -= 15;
                this.relationships[other.id] = rel - 50;
                other.relationships[this.id] = (other.relationships[this.id] || 0) - 50;
                other.addStatus("Злой", 200);
                return;
            }

            if (this.energy > 50 && other.energy > 50 && Math.random() < 0.05) {
                this.log(`Остановился поболтать с ${other.name}.`);
                this.startChat(other, 50, "general");
                this.relationships[other.id] = rel + 5;
                other.relationships[this.id] = (other.relationships[this.id] || 0) + 5;
                return;
            }
        }
    }

    startChat(other, duration, theme = "general") {
        this.chatTimer = duration;
        this.chatTarget = other;
        other.chatTimer = duration;
        other.chatTarget = this;

        this.currentAction = "Разговор";
        other.currentAction = "Разговор";

        this.chatTheme = theme;
        other.chatTheme = theme;

        this.say(generateDialogue(theme));
        setTimeout(() => {
           if (other.chatTimer > 0) other.say(generateDialogue(theme));
        }, 1500);
    }



    decideAction() {
        let hour = Math.floor(gameTime / 60);
        let action = "Безделье";
        let targetLocation = null;
        let highestUtility = 0;

        // 1. SLEEP (High priority if energy is low or it's late night)
        let sleepUtility = (100 - this.energy) * 1.5;
        if (hour >= 22 || hour < 6) sleepUtility += 100; // Go home at night
        if (sleepUtility > highestUtility) {
            highestUtility = sleepUtility;
            action = "Сон";
            targetLocation = this.home;
        }

        // 2. EAT (High priority if hunger is low)
        let eatUtility = (100 - this.hunger) * 2;
        if (this.money < 10) eatUtility -= 50; // Can't afford cafe
        if (eatUtility > highestUtility && eatUtility > 50) {
            highestUtility = eatUtility;
            action = "Ест в кафе";
            targetLocation = window.cafes[Math.floor(Math.random() * window.cafes.length)];
        }


        // 0. CAMPAIGNING (If candidate, prioritize park to talk to people)
        let campaignUtility = 0;
        if (this.isCandidate && hour >= 9 && hour <= 19) {
            campaignUtility = 95; // Very high priority
        }
        if (campaignUtility > highestUtility) {
            highestUtility = campaignUtility;
            action = "Предвыборная кампания";
            targetLocation = window.parks[Math.floor(Math.random() * window.parks.length)];
        }

        // 3. WORK

        let workUtility = 0;
        if (hour >= 9 && hour <= 17 && this.energy > 30 && this.hunger > 30 && this.profession !== "Безработный") {
            workUtility = 80;
        }
        if (workUtility > highestUtility) {
            highestUtility = workUtility;
            action = "Работа (" + this.profession + ")";
            targetLocation = this.workplace;
        }

        // 5. HOSPITAL (High priority if sick)
        let hospitalUtility = 0;
        if (this.statusEffects.find(s => s.name === "Болен")) {
            hospitalUtility = 90;
        }
        if (hospitalUtility > highestUtility) {
            highestUtility = hospitalUtility;
            action = "Лечится";
            targetLocation = window.hospitals[Math.floor(Math.random() * window.hospitals.length)];
        }

        // 6. SHOP (Medium priority if money is ok and hunger is ok)
        let shopUtility = 0;
        if (this.money > 20 && this.hunger > 60 && Math.random() < 0.05) {
            shopUtility = 60; // Random desire to shop
        }
        if (shopUtility > highestUtility) {
            highestUtility = shopUtility;
            action = "Шопинг";
            targetLocation = window.shops[Math.floor(Math.random() * window.shops.length)];
        }

        if (workUtility > highestUtility) {
            highestUtility = workUtility;
            action = "Работа";
            targetLocation = window.works[Math.floor(Math.random() * window.works.length)];
        }

        // 4. SOCIALIZE (If lonely and free time)
        let socialUtility = (100 - this.social) * 1.2;
        if (hour >= 18 && hour <= 21) socialUtility += 30; // Evening in park
        if (socialUtility > highestUtility && socialUtility > 40) {
            highestUtility = socialUtility;
            action = "Отдых в парке";
            targetLocation = window.parks[Math.floor(Math.random() * window.parks.length)];
        }


        // 4.5. В ГОСТЯХ (Visit a friend if social is low but park is boring/raining, or just want to visit friends)
        let visitUtility = 0;
        let friendToVisit = null;
        if (this.social < 60) {
            // Find a friend (relationship > 10)
            let friends = people.filter(p => p !== this && (this.relationships[p.id] || 0) > 10);
            if (friends.length > 0) {
                friendToVisit = friends[Math.floor(Math.random() * friends.length)];
                visitUtility = (100 - this.social) * 1.1; // Slightly less than park but good alternative
                if (window.weather === "Дождь") visitUtility += 40; // Prefer visiting indoors if raining
            }
        }

        if (visitUtility > highestUtility && visitUtility > 45) {
            highestUtility = visitUtility;
            action = "В гостях";
            targetLocation = friendToVisit.home;
        }


        // Execution of Action
        if (this.currentAction !== action) {
            this.currentAction = action;
            this.log(`Решил(а): ${action}`);

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
            if (action === "Сон") {
                this.energy += 5;
                if (this.statusEffects.find(s => s.name === "Болен")) this.energy += 2; // Sleep helps sickness
            }
            if (action === "Ест в кафе") {
                this.hunger += 10;
                this.money -= 0.5;
                // Chance to get sick from cafe
                if (Math.random() < 0.01) {
                    this.addStatus("Болен", 120); // Sick for 2 hours
                }
            }

            if (action.startsWith("Работа")) {
                let pay = 2;
                if (this.profession === "Мэр") pay = 15; // Mayors are rich

                this.money += pay;
                this.energy -= 0.1;
                this.social -= 0.1;
                if (this.statusEffects.find(s => s.name === "Злой")) {
                    this.money -= 1; // Angry workers perform poorly
                }
            }
            if (action === "Предвыборная кампания") {
                this.social += 2;
                this.energy -= 0.2;
            }

            if (action === "Лечится") {
                if (this.money >= 5) {
                    this.money -= 5;
                    this.statusEffects = this.statusEffects.filter(s => s.name !== "Болен");
                    this.log("Вылечился в больнице.");
                } else {
                    this.log("Не хватило денег на лечение.");
                }
            }
            if (action === "Шопинг") {
                if (this.money >= 10) {
                    this.money -= 10;
                    this.social += 5; // Retail therapy
                    this.energy -= 2;
                    this.log("Сделал покупки в магазине.");
                }
            }

            // Emergent Interactions Engine
            let othersHere = people.filter(p => p !== this && p.x === this.x && p.y === this.y && p.currentAction === this.currentAction);


            if (action === "Отдых в парке" || action === "В гостях" || othersHere.length > 0) {

                this.social += 5;

                for (let other of othersHere) {
                    let rel = this.relationships[other.id] || 0;

                    // Condition 1: Both are hungry and one has food (simulated by money right now)
                    if (this.hunger < 30 && other.hunger < 30 && other.money > 20 && this.money < 10 && action !== "Работа") {
                        if (Math.random() < 0.1) {
                            this.log(`Выпросил еду у ${other.name}.`);
                            this.say(generateDialogue("general"));
                            other.say("Ладно, держи...");
                            this.hunger += 30;
                            other.money -= 10;
                            this.relationships[other.id] = rel - 5; // They don't like beggars
                            other.addStatus("Раздражен", 60);
                        }
                    }

                    // Condition 2: Angry person meets someone
                    if (this.statusEffects.find(s => s.name === "Злой")) {
                        if (Math.random() < 0.2) {
                            this.log(`Наорал на ${other.name}!`);
                            this.say(generateDialogue("general"));
                            other.addStatus("Злой", 120); // Spread anger
                            this.relationships[other.id] = rel - 15;
                            this.statusEffects = this.statusEffects.filter(s => s.name !== "Злой"); // Relieved anger
                            this.log("Стало легче после крика.");
                        }
                    }
                    // Condition 3: Normal chat
                    else if (Math.random() < 0.1) {
                        if (rel > 10) {
                            this.log(`Отлично поболтал с другом ${other.name}.`);
                            this.say(generateDialogue("general"));
                            this.social += 15;
                            this.energy += 2; // Good chats energize
                        } else if (other.statusEffects.find(s => s.name === "Болен")) {
                             this.log(`Говорил с ${other.name}, и он чихнул на меня.`);
                             other.say(generateDialogue("general"));
                             if (Math.random() < 0.5) this.addStatus("Болен", 180);
                        } else {
                            this.log(`Поболтал с ${other.name}.`);
                            this.say(generateDialogue("general"));
                            this.social += 10;
                            this.relationships[other.id] = rel + 2;
                        }
                    }

                    // Random argument
                    if (Math.random() < 0.005) {
                        this.log(`Подрался с ${other.name}!`);
                        this.say(generateDialogue("general"));
                        other.say(generateDialogue("general"));
                        this.addStatus("Злой", 120);
                        other.addStatus("Злой", 120);
                        this.relationships[other.id] = rel - 20;
                    }

                    break; // Interact with one person at a time
                }
            }

        }
    }



    draw(ctx) {
        let vx = this.visualX * window.TILE_SIZE;
        let vy = this.visualY * window.TILE_SIZE;

        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.beginPath();
        ctx.arc(vx + window.TILE_SIZE / 2,
                vy + window.TILE_SIZE - 2,
                window.TILE_SIZE / 3, 0, Math.PI * 2);
        ctx.fill();

        let pSize = window.TILE_SIZE / 4;
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (this.pixels[i][j] !== 'transparent') {
                    ctx.fillStyle = this.pixels[i][j];
                    ctx.fillRect(vx + j * pSize, vy + i * pSize, pSize, pSize);

                    if (selectedPerson === this) {
                        ctx.strokeStyle = '#fff';
                        ctx.lineWidth = 1;
                        ctx.strokeRect(vx + j * pSize, vy + i * pSize, pSize, pSize);
                    }
                }
            }
        }



        // Draw emoji bubble based on action
        let emoji = "";
        if (this.currentAction === "Сон") emoji = "💤";
        if (this.currentAction === "Ест в кафе") emoji = "🍔";
        if (this.currentAction.startsWith("Работа")) emoji = "💼";
        if (this.profession === "Мэр") emoji = "👑"; // Always show crown for mayor
        if (this.currentAction === "Предвыборная кампания") emoji = "📢";
        if (this.currentAction === "Лечится") emoji = "🏥";
        if (this.currentAction === "Шопинг") emoji = "🛍️";
        if (this.currentAction === "Разговор") emoji = "🗣️";
        if (this.currentAction === "Отдых в парке") emoji = "💬";
        if (this.currentAction === "В гостях") emoji = "🏠";
        if (this.currentAction === "Бегство") emoji = "🏃";
        if (this.currentAction === "Разговор") emoji = "🗣️";

        if (this.statusEffects.find(s => s.name === "Злой")) emoji = "🤬"; // override with status emotion
        if (this.statusEffects.find(s => s.name === "Болен")) emoji = "🤒";



        if (emoji) {
            ctx.font = "16px Arial";
            ctx.textAlign = "center";
            ctx.fillText(emoji, vx + window.TILE_SIZE / 2,
                               vy + 10);
        }

        // Draw speech bubble
        if (this.speechTimer > 0 && this.speechBubble !== "") {
            ctx.font = "12px sans-serif";
            let textWidth = ctx.measureText(this.speechBubble).width;
            let padding = 4;

            let bx = vx + window.TILE_SIZE / 2 - textWidth / 2;
            let by = vy - 15;

            // Bubble background
            ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
            ctx.beginPath();
            ctx.roundRect(bx - padding, by - 12 - padding, textWidth + padding * 2, 16 + padding * 2, 4);
            ctx.fill();
            ctx.strokeStyle = "#333";
            ctx.lineWidth = 1;
            ctx.stroke();

            // Text
            ctx.fillStyle = "#000";
            ctx.textAlign = "center";
            ctx.fillText(this.speechBubble, vx + window.TILE_SIZE / 2, by);
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



function updateElectionUI() {
    let list = document.getElementById('candidateList');
    if (!list) return;
    list.innerHTML = "";
    candidates.forEach(c => {
        let li = document.createElement('li');
        li.style.marginBottom = "8px";
        li.style.borderBottom = "1px solid #333";
        li.style.paddingBottom = "4px";

        let header = document.createElement('div');
        header.style.fontWeight = "bold";
        header.style.color = "#fff";
        header.textContent = c.fio;

        let party = document.createElement('div');
        party.style.fontSize = "0.85em";
        party.style.color = "#a78bfa";
        party.style.fontStyle = "italic";
        party.textContent = c.partyName;

        let votes = document.createElement('div');
        votes.style.color = "#4ade80";
        votes.style.fontSize = "0.85em";
        votes.textContent = "Голоса: " + (c.votes > 0 ? c.votes : "?"); // Reveal mostly at end

        li.appendChild(header);
        li.appendChild(party);
        li.appendChild(votes);
        list.appendChild(li);
    });
}

function updateInspector() {
    if (selectedPerson) {
        insHint.style.display = 'none';
        insData.style.display = 'block';

        let fioEl = document.getElementById('insFIO');
        if(fioEl) fioEl.textContent = selectedPerson.fio + " (" + selectedPerson.profession + ")";
        let ageEl = document.getElementById('insAge');
        if(ageEl) ageEl.textContent = `Возраст: ${selectedPerson.age} лет`;


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
            handleElections();
            if (gameTime % 60 === 0 && (gameTime === 7*60 || gameTime === 20*60)) mapNeedsRedraw = true;

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
    people.sort((a,b) => a.visualY - b.visualY);
    for (let p of people) {
        // Lerp movement
        if (isRunning) {
            p.visualX += (p.x - p.visualX) * 0.2;
            p.visualY += (p.y - p.visualY) * 0.2;
        }
        p.draw(ctx);
    }

    // Day/Night Cycle Overlay
    let hour = gameTime / 60;
    let darkness = 0;
    if (hour < 6) darkness = 0.6; // Night
    else if (hour < 8) darkness = 0.6 - (hour - 6) * 0.3; // Sunrise
    else if (hour > 18 && hour < 20) darkness = (hour - 18) * 0.3; // Sunset
    else if (hour >= 20) darkness = 0.6; // Night

    if (darkness > 0) {
        ctx.fillStyle = `rgba(10, 10, 30, ${darkness})`;
        ctx.fillRect(0, 0, window.width, window.height);
    }

    // Rain Effects
    if (window.weather === "Дождь") {
        ctx.strokeStyle = "rgba(150, 180, 255, 0.4)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        for (let i = 0; i < 100; i++) {
            let rx = Math.random() * window.width;
            let ry = Math.random() * window.height;
            ctx.moveTo(rx, ry);
            ctx.lineTo(rx - 5, ry + 15);
        }
        ctx.stroke();
    }

    animationId = requestAnimationFrame(gameLoop);

}

// Events
toggleBtn.addEventListener('click', () => {
    isRunning = !isRunning;
    toggleBtn.textContent = isRunning ? "Пауза" : "Старт";
});

speedBtn.addEventListener('click', () => {
    isFastForward = !isFastForward;
    if (isFastForward) {
        speedBtn.classList.add('active-fast');
        speedBtn.textContent = "Обычная Скорость ⏯️";
    } else {
        speedBtn.classList.remove('active-fast');
        speedBtn.textContent = "Ускорение ⏩";
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