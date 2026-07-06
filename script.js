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

window.cityMap = [];
window.homes = [];
window.works = [];
window.cafes = [];
window.parks = [];
window.hospitals = [];
window.shops = [];



// Initialize map
for (let y = 0; y < ROWS; y++) {
    let row = [];
    for (let x = 0; x < COLS; x++) {
        row.push(EMPTY);
    }
    window.cityMap.push(row);
}

// Draw main roads (cross pattern + outer ring)
for (let y = 4; y < ROWS - 4; y++) {
    window.cityMap[y][Math.floor(COLS/2)] = ROAD;
    window.cityMap[y][Math.floor(COLS/2) - 1] = ROAD; // Wider roads
}
for (let x = 4; x < COLS - 4; x++) {
    window.cityMap[Math.floor(ROWS/2)][x] = ROAD;
    window.cityMap[Math.floor(ROWS/2) - 1][x] = ROAD;
}
for (let y = 8; y < ROWS - 8; y++) {
    window.cityMap[y][Math.floor(COLS/4)] = ROAD;
    window.cityMap[y][Math.floor(COLS*3/4)] = ROAD;
}
for (let x = 8; x < COLS - 8; x++) {
    window.cityMap[Math.floor(ROWS/4)][x] = ROAD;
    window.cityMap[Math.floor(ROWS*3/4)][x] = ROAD;
}


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

// Add zones (spreading them out on the larger map)
addZone(2, 2, 5, 5, HOME, window.homes);
addZone(COLS - 7, 2, 5, 5, HOME, window.homes);
addZone(2, ROWS - 7, 5, 5, HOME, window.homes);
addZone(Math.floor(COLS/4) + 2, Math.floor(ROWS/4) + 2, 4, 4, HOME, window.homes);

addZone(COLS - 12, ROWS - 12, 8, 8, WORK, window.works);
addZone(10, Math.floor(ROWS/2) + 2, 6, 6, WORK, window.works);

addZone(Math.floor(COLS/2) + 2, 5, 6, 6, CAFE, window.cafes);
addZone(Math.floor(COLS/4) + 2, Math.floor(ROWS*3/4) + 2, 7, 7, PARK, window.parks);

addZone(5, Math.floor(ROWS/4) + 2, 6, 6, HOSPITAL, window.hospitals);
addZone(Math.floor(COLS*3/4) + 2, Math.floor(ROWS/2) + 2, 6, 6, SHOP, window.shops);



window.drawMap = function() {
    let hour = gameTime / 60;
    let isNight = hour < 7 || hour > 19;

    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            let tile = window.cityMap[y][x];
            let px = x * window.TILE_SIZE;
            let py = y * window.TILE_SIZE;

            // Base ground
            if (tile === EMPTY) {
                ctx.fillStyle = '#1e1e2e';
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                // Grass details randomly
                if ((x*y) % 7 === 0) {
                    ctx.fillStyle = '#262638';
                    ctx.fillRect(px + 4, py + 4, 4, 4);
                }
            }
            else if (tile === ROAD) {
                ctx.fillStyle = '#313244';
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                // Road markings
                ctx.fillStyle = '#45475a';
                if (x % 2 === 0 && window.cityMap[y][x-1] === ROAD && window.cityMap[y][x+1] === ROAD) {
                    ctx.fillRect(px + window.TILE_SIZE/4, py + window.TILE_SIZE/2 - 1, window.TILE_SIZE/2, 2);
                }
                if (y % 2 === 0 && window.cityMap[y-1] && window.cityMap[y-1][x] === ROAD && window.cityMap[y+1] && window.cityMap[y+1][x] === ROAD) {
                    ctx.fillRect(px + window.TILE_SIZE/2 - 1, py + window.TILE_SIZE/4, 2, window.TILE_SIZE/2);
                }
            }
            else if (tile === HOME) {
                ctx.fillStyle = '#3b82f6';
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                // Roof shadow
                ctx.fillStyle = 'rgba(0,0,0,0.2)';
                ctx.fillRect(px, py + window.TILE_SIZE/2, window.TILE_SIZE, window.TILE_SIZE/2);
                // Window light
                if (isNight) {
                    ctx.fillStyle = '#fde047'; // yellow light
                    ctx.fillRect(px + 4, py + 4, 6, 6);
                }
            }
            else if (tile === WORK) {
                ctx.fillStyle = '#8b5cf6';
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                ctx.fillStyle = 'rgba(255,255,255,0.1)';
                ctx.fillRect(px + 2, py + 2, window.TILE_SIZE - 4, window.TILE_SIZE - 4);
            }
            else if (tile === CAFE) {
                ctx.fillStyle = '#ef4444';
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                // Awning
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(px, py, window.TILE_SIZE, 4);
                // Window light
                if (isNight) {
                    ctx.fillStyle = '#fde047';
                    ctx.fillRect(px + 4, py + 8, window.TILE_SIZE - 8, 8);
                }
            }

            else if (tile === PARK) {
                ctx.fillStyle = '#22c55e';
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                // Tree
                if ((x+y) % 2 === 0) {
                    ctx.fillStyle = '#16a34a';
                    ctx.beginPath();
                    ctx.arc(px + window.TILE_SIZE/2, py + window.TILE_SIZE/2, window.TILE_SIZE/3, 0, Math.PI*2);
                    ctx.fill();
                    // Tree shadow
                    ctx.fillStyle = 'rgba(0,0,0,0.2)';
                    ctx.beginPath();
                    ctx.arc(px + window.TILE_SIZE/2 + 2, py + window.TILE_SIZE/2 + 2, window.TILE_SIZE/3, 0, Math.PI*2);
                    ctx.fill();
                }
            }
            else if (tile === HOSPITAL) {
                ctx.fillStyle = '#f43f5e'; // Pink-red
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                // Cross
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(px + window.TILE_SIZE/2 - 2, py + 4, 4, window.TILE_SIZE - 8);
                ctx.fillRect(px + 4, py + window.TILE_SIZE/2 - 2, window.TILE_SIZE - 8, 4);
            }
            else if (tile === SHOP) {
                ctx.fillStyle = '#0ea5e9'; // Cyan
                ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
                ctx.fillStyle = 'rgba(255,255,255,0.2)';
                // Stripes
                if (x % 2 === 0) ctx.fillRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
            }


            // Grid lines
            ctx.strokeStyle = 'rgba(255,255,255,0.02)';
            ctx.strokeRect(px, py, window.TILE_SIZE, window.TILE_SIZE);
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



// Procedural Absurd Dialogue Engine
const DICTIONARY = {
    words: [
        "кот", "борщ", "сингулярность", "тапочки", "космос", "пицца", "квант", "забор", "луна", "кирпич",
        "пельмени", "робот", "носок", "дождь", "кактус", "шляпа", "трактор", "философия", "сыр", "колбаса",
        "огурец", "карандаш", "матрица", "пылесос", "динозавр", "банан", "бульдозер", "макароны", "утка", "чайник",
        "капибара", "майонез", "телевизор", "диван", "смысл", "безумие", "табуретка", "вилка", "кефир", "шаурма",
        "прыгать", "спать", "летать", "жевать", "кричать", "бежать", "думать", "плакать", "чихать", "смеяться",
        "красть", "строить", "ломать", "любить", "ждать", "искать", "падать", "кидать", "копать", "танцевать",
        "мерцать", "булькать", "жужжать", "храпеть", "варить", "жарить", "шептать", "выть", "сиять", "глючить",
        "зеленый", "мокрый", "странный", "квадратный", "вкусный", "холодный", "лысый", "пушистый", "глупый", "великий",
        "быстрый", "мягкий", "острый", "ржавый", "соленый", "громкий", "тайный", "святой", "эпичный", "жидкий",
        "колючий", "сладкий", "кривой", "железный", "деревянный", "золотой", "скользкий", "мутный", "липкий", "бодрый",
        "внезапно", "вчера", "громко", "быстро", "печально", "весело", "тайно", "медленно", "вкусно", "странно",
        "зачем-то", "никогда", "всегда", "уныло", "бодро", "криво", "яростно", "нежно", "тихо", "эпично",
        "однако", "потому", "если", "хотя", "чтобы", "затем", "потом", "или", "и", "но",
        "ай", "ой", "ого", "ух", "ага", "увы", "вау", "хм", "э", "брр",
        "космонавт", "кастрюля", "бетон", "улитка", "голубь", "собака", "картошка", "трава", "солнце", "ветер",
        "самолет", "колесо", "гвоздь", "молоток", "топор", "утюг", "окно", "дверь", "стена", "пол",
        "потолок", "крыша", "труба", "коробка", "бумага", "книга", "буква", "цифра", "ноль", "единица",
        "корова", "свинья", "лошадь", "мышь", "слон", "жираф", "бегемот", "крокодил", "змея", "паук",
        "муха", "комар", "пчела", "оса", "шмель", "жук", "бабочка", "мотылек", "гусеница", "червяк",
        "дерево", "куст", "цветок", "лист", "корень", "ветка", "ствол", "кора", "мох", "гриб",
        "яблоко", "груша", "слива", "вишня", "черешня", "клубника", "малина", "смородина", "крыжовник", "арбуз",
        "дыня", "тыква", "кабачок", "баклажан", "помидор", "морковь", "свекла", "лук", "чеснок", "перец",
        "соль", "сахар", "мука", "масло", "хлеб", "булка", "печенье", "конфета", "шоколад", "мороженое",
        "пить", "есть", "кусать", "лизать", "глотать", "плевать", "нюхать", "дышать", "кашлять", "зевать",
        "моргать", "смотреть", "видеть", "слушать", "слышать", "трогать", "гладить", "чесать", "щипать", "бить",

        // Expansion words
        "магазин", "больница", "таблетка", "врач", "покупки", "касса", "деньги", "карта", "шприц", "градусник",
        "лекарство", "сироп", "здоровье", "хлеб", "молоко", "яйца", "рыба", "мясо", "сыр", "колбаса",
        "купить", "продать", "лечить", "болеть", "выздоравливать", "платить", "брать", "отдавать", "считать",
        "дорого", "дешево", "больно", "здорово", "полезно", "вредно", "сладко", "горько", "кисло",
        "аптека", "продукт", "товар", "пакет", "скидка", "акция", "чек", "сдача", "очередь", "кассир",
        "пациент", "диагноз", "рецепт", "витамин", "бинт", "пластырь", "укол", "операция", "медсестра"

    ]
};

function generateDialogue() {
    let pick = () => DICTIONARY.words[Math.floor(Math.random() * DICTIONARY.words.length)];
    let length = Math.floor(Math.random() * 4) + 2; // 2 to 5 words
    let sentence = [];
    for(let i = 0; i < length; i++) {
        sentence.push(pick());
    }
    // Capitalize first word and add punctuation
    let text = sentence.join(" ");
    let punctuation = Math.random() > 0.7 ? "!" : (Math.random() > 0.5 ? "?" : ".");
    return text.charAt(0).toUpperCase() + text.slice(1) + punctuation;
}



const NAMES_FIRST = ["Иван", "Александр", "Дмитрий", "Сергей", "Андрей", "Алексей", "Максим", "Евгений", "Михаил", "Владимир", "Анна", "Мария", "Елена", "Дарья", "Ольга", "Екатерина", "Наталья", "Татьяна", "Юлия", "Анастасия"];
const NAMES_LAST = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Петров", "Соколов", "Михайлов", "Новиков", "Федоров", "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев"];
const NAMES_PATRO = ["Иванович", "Александрович", "Дмитриевич", "Сергеевич", "Андреевич", "Алексеевич", "Максимович", "Евгеньевич", "Михайлович", "Владимирович"];
const NAMES_PATRO_F = ["Ивановна", "Александровна", "Дмитриевна", "Сергеевна", "Андреевна", "Алексеевна", "Максимовна", "Евгеньевна", "Михайловна", "Владимировна"];

function generateFIO() {
    let first = NAMES_FIRST[Math.floor(Math.random() * NAMES_FIRST.length)];
    let last = NAMES_LAST[Math.floor(Math.random() * NAMES_LAST.length)];

    // Simple gender check based on first name ending (not perfect but ok for mock data)
    let isFemale = first.endsWith('а') || first.endsWith('я');

    if (isFemale && !last.endsWith('а') && !last.endsWith('в')) {
         // handle genderizing last name naively
         if(last.endsWith('ов') || last.endsWith('ев') || last.endsWith('ин')) {
             last += 'а';
         }
    } else if (isFemale && (last.endsWith('ов') || last.endsWith('ев'))) {
         last += 'а';
    }

    let patro = isFemale ?
                NAMES_PATRO_F[Math.floor(Math.random() * NAMES_PATRO_F.length)] :
                NAMES_PATRO[Math.floor(Math.random() * NAMES_PATRO.length)];

    return `${last} ${first} ${patro}`;
}


class Person {

    constructor(id) {
        this.id = id;
        this.fio = generateFIO();
        this.name = this.fio.split(" ")[1] || this.fio; // Short name for logs

        this.age = Math.floor(Math.random() * 50) + 18; // 18 to 67 years old


        // Generate a 4x4 unique pixel art avatar
        this.pixels = [];
        let baseColor = `hsl(${Math.random() * 360}, 70%, 60%)`;

        // Assign Profession
        this.profession = "Безработный";
        this.workplace = null;
        if (id % 3 === 0) {
            this.profession = "Офис-менеджер";
            this.workplace = window.works[Math.floor(Math.random() * window.works.length)];
        } else if (id % 3 === 1) {
            this.profession = "Врач";
            this.workplace = window.hospitals[Math.floor(Math.random() * window.hospitals.length)];
            baseColor = '#ffffff'; // Doctors wear white
        } else {
            this.profession = "Продавец";
            this.workplace = window.shops[Math.floor(Math.random() * window.shops.length)];
            baseColor = '#0ea5e9'; // Shop uniform
        }

        let accentColor = `hsl(${Math.random() * 360}, 80%, 40%)`;
        let skinColor = Math.random() > 0.5 ? '#fcd34d' : '#f87171'; // basic skin tones

        for (let i = 0; i < 4; i++) {
            let row = [];
            for (let j = 0; j < 4; j++) {
                if (i === 0 && (j === 1 || j === 2)) row.push(skinColor); // head
                else if (i === 1) row.push(baseColor); // shoulders/chest
                else if (i === 2 && (j === 1 || j === 2)) row.push(baseColor); // body
                else if (i === 2 && (j === 0 || j === 3)) row.push(skinColor); // hands
                else if (i === 3 && (j === 1 || j === 2)) row.push(accentColor); // legs
                else row.push('transparent');
            }
            this.pixels.push(row);
        }



        // Assign a random home
        let home = window.homes[Math.floor(Math.random() * window.homes.length)];
        this.x = home.x;
        this.y = home.y;

        this.home = home;

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

        this.log("Проснулся в МиниГраде.");
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
                this.say(generateDialogue());
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
        if (this.chatTimer > 0) return; // Don't interrupt existing chat

        // Find people on same or adjacent tiles to increase interaction frequency
        let othersHere = people.filter(p => p !== this && Math.abs(p.x - this.x) <= 1 && Math.abs(p.y - this.y) <= 1);
        for (let other of othersHere) {
            if (other.chatTimer > 0) continue;

            let rel = this.relationships[other.id] || 0;

            // Friends stopping to chat (higher chance now)
            if (rel > 10 && Math.random() < 0.4) {
                this.log(`Случайно встретил друга ${other.name}!`);
                this.startChat(other, 80);
                return;
            }

            // Enemies fighting on sight!
            if (rel < -10 && Math.random() < 0.5) {
                this.log(`Увидел врага ${other.name} и завязалась драка!`);
                this.energy -= 10;
                other.energy -= 10;
                this.addStatus("Злой", 100);
                other.addStatus("Злой", 100);

                this.say(generateDialogue());
                other.say(generateDialogue());

                this.currentAction = "Бегство";
                this.target = this.home;
                this.path = window.findPath(this.x, this.y, this.home.x, this.home.y);

                other.currentAction = "Бегство";
                other.target = other.home;
                other.path = window.findPath(other.x, other.y, other.home.x, other.home.y);
                return;
            }

            // Desperate stealing
            if (this.hunger < 30 && this.money < 10 && other.money > 20 && Math.random() < 0.2) {
                this.log(`Украл деньги у ${other.name} от отчаяния!`);
                this.say(generateDialogue());
                other.say(generateDialogue());
                this.money += 15;
                other.money -= 15;
                this.relationships[other.id] = rel - 50;
                other.relationships[this.id] = (other.relationships[this.id] || 0) - 50;
                other.addStatus("Злой", 200);
                return;
            }

            // Random neutral chat with strangers
            if (Math.random() < 0.05) {
                this.log(`Остановился поболтать с ${other.name}.`);
                this.startChat(other, 50);
                this.relationships[other.id] = rel + 5;
                other.relationships[this.id] = (other.relationships[this.id] || 0) + 5;
                return;
            }
        }
    }

    startChat(other, duration) {
        this.chatTimer = duration;
        this.chatTarget = other;
        other.chatTimer = duration;
        other.chatTarget = this;

        this.currentAction = "Разговор";
        other.currentAction = "Разговор";

        this.say(generateDialogue());
        setTimeout(() => {
           if (other.chatTimer > 0) other.say(generateDialogue());
        }, 1500); // Small visual delay
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


        // 3. WORK (Priority during work hours if needs are somewhat met)
        let workUtility = 0;
        if (hour >= 9 && hour <= 17 && this.energy > 30 && this.hunger > 30 && this.profession !== "Безработный") {
            workUtility = 80;
        }
        if (workUtility > highestUtility) {
            highestUtility = workUtility;
            action = "Работа (" + this.profession + ")";
            targetLocation = this.workplace;
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
                this.money += 2;
                this.energy -= 0.1;
                this.social -= 0.1;
                if (this.statusEffects.find(s => s.name === "Злой")) {
                    this.money -= 1; // Angry workers perform poorly
                }
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
                            this.say(generateDialogue());
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
                            this.say(generateDialogue());
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
                            this.say(generateDialogue());
                            this.social += 15;
                            this.energy += 2; // Good chats energize
                        } else if (other.statusEffects.find(s => s.name === "Болен")) {
                             this.log(`Говорил с ${other.name}, и он чихнул на меня.`);
                             other.say(generateDialogue());
                             if (Math.random() < 0.5) this.addStatus("Болен", 180);
                        } else {
                            this.log(`Поболтал с ${other.name}.`);
                            this.say(generateDialogue());
                            this.social += 10;
                            this.relationships[other.id] = rel + 2;
                        }
                    }

                    // Random argument
                    if (Math.random() < 0.005) {
                        this.log(`Подрался с ${other.name}!`);
                        this.say(generateDialogue());
                        other.say(generateDialogue());
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

        // Shadow
        ctx.fillStyle = 'rgba(0,0,0,0.3)';
        ctx.beginPath();
        ctx.arc(vx + window.TILE_SIZE / 2,
                vy + window.TILE_SIZE - 2,
                window.TILE_SIZE / 3, 0, Math.PI * 2);
        ctx.fill();

        // Draw 4x4 Pixel Art
        let pSize = window.TILE_SIZE / 4;
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                if (this.pixels[i][j] !== 'transparent') {
                    ctx.fillStyle = this.pixels[i][j];
                    ctx.fillRect(vx + j * pSize, vy + i * pSize, pSize, pSize);

                    // Highlight selected outline
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
        if (this.currentAction === "Отдых в парке") emoji = "💬";

        if (this.currentAction === "В гостях") emoji = "🏠";
        if (this.currentAction === "Лечится") emoji = "🏥";
        if (this.currentAction === "Шопинг") emoji = "🛍️";
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


function updateInspector() {


    if (selectedPerson) {
        insHint.style.display = 'none';
        insData.style.display = 'block';

        let fioEl = document.getElementById('insFIO');
        if(fioEl) fioEl.textContent = selectedPerson.fio + " (" + selectedPerson.profession + ")";
        let ageEl = document.getElementById('insAge');
        if(ageEl) ageEl.textContent = `Возраст: ${selectedPerson.age} лет`;



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