const PANTALLA = document.querySelector("#game");
const context = PANTALLA.getContext("2d");
const scoreText = document.querySelector("#scoreText");
const resetButton = document.querySelector("#resetButton");

let t;


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

window.addEventListener("keydown", changeDirection);

resetButton.addEventListener("click", resetGame);

gameStart();


function gameStart(){
    running = true;
    scoreText.textContent = score;
    createSnake();
    createFood();
    drawFood();
    nextTick();
};
function nextTick(){
    if(running){
        t = setTimeout(() => {
            clearBoard();
            drawFood();
            moveSnake();
            drawSnake();
            checkGameOver();
            nextTick();
        }, 150)
    }else{
        displayGameOver();
    }
};
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
function changeDirection(event){
    const keyPressed = event.keyCode;
    const LEFT = 37;
    const RIGHT  = 39;
    const UP = 38;
    const DOWN = 40;
    xV = movimientos[0].xVel; yV = movimientos[0].yVel;

    const goingUp = (yV == -unitSize)
    const goingDown = (yV == unitSize)
    const goingRight = (xV == unitSize)
    const goingLeft = (xV == -unitSize)

    switch(true){
        case (keyPressed == LEFT && !goingRight):
            movimientos.push({xVel:-unitSize, yVel: 0});
            break;
        case (keyPressed == UP && !goingDown):
            movimientos.push({xVel:0, yVel: -unitSize});
            break;
        case (keyPressed == RIGHT && !goingLeft):
            movimientos.push({xVel:unitSize, yVel: 0});
            break;
        case (keyPressed == DOWN && !goingUp):
            movimientos.push({xVel:0, yVel: unitSize});
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
