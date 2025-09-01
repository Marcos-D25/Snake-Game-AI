const ws = new WebSocket("ws://127.0.0.1:8000/predecir_movimiento")
ws.onopen = function() {
    console.log("✅ WebSocket conectado!");
    gameStart(); // <-- arranca el juego solo cuando la conexión está lista
};
const PANTALLA = document.querySelector("#game");
const context = PANTALLA.getContext("2d");
const scoreText = document.querySelector("#scoreText");
const resetButton = document.querySelector("#resetButton");

let ultimo_movimiento;


const WIDTH = PANTALLA.width; 
const HEIGHT = PANTALLA.height;
const bgcolor = "black"
const snakeColor = "blue";
const snakeBorder = "black";
const foodColor = "green";

const unitSize = 20;
let running = false;

let movimientos = [{xVel : unitSize, yVel: 0}];
let foodX;
let foodY;
let score = 0;


let snake;
function createSnake(){
    snake = []; 
    for (let i = 1 ; i >= 0; i--){
        snake.push({x:i*unitSize, y:0});
    }   
}


resetButton.addEventListener("click", resetGame);



function gameStart(){
    running = true;
    scoreText.textContent = score;
    createSnake();
    createFood();
    drawFood();
    nextTick();
};
async function nextTick() {
    if (!running) {
        displayGameOver();
        return;
    }
    
    const estado = get_Estado();//Obtengo el esrado actual
    let movimiento;
    try {
        movimiento = await enviarEstadoConRespuesta(estado);
    } catch (err) {
        console.warn("Error al obtener movimiento, usando el anterior:", err);
        movimiento = ultimoMovimiento; // fallback
    }

    
    aplicar_movimiento(movimiento);
    moveSnake();
    clearBoard();
    drawFood();
    drawSnake();
    checkGameOver();

    setTimeout(nextTick, 350);
}
function clearBoard(){
    context.fillStyle = bgcolor;
    context.fillRect(0,0,WIDTH,HEIGHT);
};
function createFood(){
    function randomFood(min,max){
        const randNum = Math.round((Math.random()* (max - min) + min) / unitSize) * unitSize;
        return randNum;
    }
    let valid = false;
    while (!valid) {
        foodX = randomFood(0, WIDTH - unitSize);
        foodY = randomFood(0, HEIGHT - unitSize);

        // Verificar que no caiga encima de la serpiente
        valid = !snake.some(part => part.x === foodX && part.y === foodY);
    }
};
function drawFood(){
    context.fillStyle = foodColor;
    context.fillRect(foodX,foodY,unitSize,unitSize);
};
function moveSnake(){
    let xV; let yV;
    xV = movimientos[0].xVel; yV = movimientos[0].yVel;
    if (movimientos.length > 1 ){
        movimientos.shift();
    }
    const head = {
        x: snake[0].x + xV,
        y: snake[0].y + yV,
    };
    snake.unshift(head);
    if(snake[0].x === foodX && snake[0].y === foodY ){
        score += 1;
        scoreText.textContent = score;
        createFood();
    }else{
        snake.pop();
    }
};
function drawSnake(){
    context.fillStyle = snakeColor;
    context.strokeStyle = snakeBorder;
    snake.forEach(snake_part => {
        context.fillRect(snake_part.x,snake_part.y, unitSize, unitSize);
        context.strokeRect(snake_part.x,snake_part.y, unitSize, unitSize);
    })
};

function aplicar_movimiento(move){
    xV = movimientos[0].xVel; yV = movimientos[0].yVel;
    const goingUp = (yV == -unitSize)
    const goingDown = (yV == unitSize)
    const goingRight = (xV == unitSize)
    const goingLeft = (xV == -unitSize)

    switch (move) {
        case "L":
            if (!goingRight) movimientos.push({xVel:-unitSize, yVel:0});
            break;
        case "R":
            if (!goingLeft) movimientos.push({xVel:unitSize, yVel:0});
            break;
        case "U":
            if (!goingDown) movimientos.push({xVel:0, yVel:-unitSize});
            break;
        case "D":
            if (!goingUp) movimientos.push({xVel:0, yVel:unitSize});
            break;
    }
};
function checkGameOver(){
    
    switch(true){
        case (snake[0].x < 0  || snake[0].x >= WIDTH):
            running = false;
            break;
        case (snake[0].y < 0  || snake[0].y >= HEIGHT):
            running = false;
            break;
    }
    
    for (let i = 1; i < snake.length; i ++){
        if (snake[i].x == snake[0].x && snake[i].y == snake[0].y){
            running = false;
        }
    }
};
function displayGameOver(){
    context.font = "ComicSans";
    context.fillStyle = "white";
    context. textAlign = "center";
    context.fillText("FIN", WIDTH/2, HEIGHT/2);
    running = false;
};
function resetGame(){
    score = 0;
    movimientos = [{xVel : unitSize, yVel: 0}];
    snake = [];
    for (let i = 4 ; i >= 0; i--){
        snake.push({x:i*unitSize, y:0});
    }

    clearInterval(t);
    gameStart();
};

function enviarEstadoConRespuesta(estado) {
    return new Promise((resolve) => { //Creo una promesa que se resolvera cuando el modelo devuela el MOVIMIENTO PREDICHO
        //console.log("Enviando estado:", estado);
        const handler = (event) => {//Creo un listener para cuando el servidor devuelva la respuesta yo poder resolver la promesa y mandar el movimiento para continuar la ejecucion del codigo
            const data = JSON.parse(event.data);
            ws.removeEventListener("message", handler);//Elimino el listener para que no se puedan enviar mas movimientos
            resolve(data.movimiento);//Resuelvo la promesa
        };

        ws.addEventListener("message", handler);//Añado el listener al mensaje del servidor antes de enviar el estado al servidor, para evitar que el servidor responda sin que se pueda procesar la respuesta
        ws.send(JSON.stringify(estado));//Envio el estado al servidor
    });
;}
function colision_cuerpo(coords){
    for(let i = 1;i < snake.length; i++ ){
        if(snake[i].x == coords[0] && snake[i].y == coords[1]){
            return true;
        }
    }
    return false;
}

function get_Estado(){
    //Coordenadas de la cabeza de la serpiente
    let c_s_x = snake[0].x;
    let c_s_y = snake[0].y;
    //Distancias de la comida a la cabeza de la serpiente
    let dist_com_x = Math.abs(foodX-c_s_x);
    let dist_com_y = Math.abs(foodY-c_s_y);
    //Colisiones con las paredes
    let movs = [snake[0].x - unitSize, snake[0].x + unitSize, snake[0].y - unitSize, snake[0].y + unitSize];
    let p_iz = movs[0] < 0;
    let p_der = movs[1] > WIDTH;
    let p_ar = movs[2] < 0;
    let p_ab = movs[3] > HEIGHT;
    //Colisiones con el cuerpo
    let c_iz = colision_cuerpo([movs[0],c_s_y]);
    let c_der = colision_cuerpo([movs[1],c_s_y]);
    let c_ar = colision_cuerpo([c_s_x,movs[2]]);
    let c_ab = colision_cuerpo([c_s_x,movs[3]]);

    return {
        "cabeza_serpiente_x": c_s_x,
        "cabeza_serpiente_y": c_s_y,
        "dist_comida_x": dist_com_x,
        "dist_comida_y": dist_com_y,
        "pared_izq": p_iz,
        "pared_der": p_der,
        "pared_ar": p_ar,
        "pared_ab": p_ab,
        "cuerpo_izq": c_iz,
        "cuerpo_der": c_der,
        "cuerpo_ar": c_ar,
        "cuerpo_ab": c_ab
    };
}