from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

# Configurações do Jogo
GRID_SIZE = 20

@app.route('/')
def index():
    # HTML e JavaScript do jogo embutidos para rodar tudo em um único arquivo de forma simples
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Azure DevOps Snake Game</title>
        <style>
            body {
                background-color: #0c1015;
                color: #f0f6fc;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            h1 {
                color: #0078d4; /* Azul Azure */
                margin-bottom: 5px;
            }
            .subtitle {
                color: #8b949e;
                margin-bottom: 20px;
                font-size: 0.9rem;
            }
            #score-board {
                font-size: 1.5rem;
                margin-bottom: 10px;
                font-weight: bold;
            }
            canvas {
                border: 4px solid #0078d4;
                background-color: #161b22;
                box-shadow: 0px 0px 20px rgba(0, 120, 212, 0.3);
            }
            .controls {
                margin-top: 15px;
                color: #8b949e;
                font-size: 0.85rem;
                text-align: center;
            }
            .badge {
                background-color: #238636;
                color: white;
                padding: 2px 6px;
                border-radius: 3px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <h1>Azure DevOps Edition</h1>
        <div class="subtitle">Alimente a cobrinha com pacotes de código para fazer o deploy!</div>

        <div id="score-board">Deploy Score: <span id="score" class="badge">0</span></div>
        <canvas id="gameCanvas" width="400" height="400"></canvas>

        <div class="controls">
            Use as <b>Setas do Teclado</b> ou <b>W, A, S, D</b> para mover.<br>
            Evite bater nas paredes ou em si mesmo!
        </div>

        <script>
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");
            const scoreElement = document.getElementById("score");

            const gridSize = 20;
            const tileCount = canvas.width / gridSize;

            let snake = [{x: 10, y: 10}];
            let food = {x: 5, y: 5};
            let dx = 1;
            let dy = 0;
            let score = 0;
            let gameSpeed = 100;
            let gameLoopInterval;

            function main() {
                if (hasGameEnded()) {
                    alert("Pipeline Falhou! Fim de jogo. Seu score de deploys foi: " + score);
                    resetGame();
                }

                clearCanvas();
                drawFood();
                moveSnake();
                drawSnake();
            }

            function clearCanvas() {
                ctx.fillStyle = "#161b22";
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            function drawSnake() {
                snake.forEach((part, index) => {
                    // A cabeça é azul Azure, o corpo é um tom ligeiramente diferente
                    ctx.fillStyle = index === 0 ? "#0078d4" : "#288ad6";
                    ctx.strokeStyle = "#161b22";
                    ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
                });
            }

            function moveSnake() {
                const head = {x: snake[0].x + dx, y: snake[0].x + dy};
                
                // Teleporte pelas paredes (opcional, mas deixa o jogo mais fluido)
                if (head.x < 0) head.x = tileCount - 1;
                if (head.x >= tileCount) head.x = 0;
                if (head.y < 0) head.y = tileCount - 1;
                if (head.y >= tileCount) head.y = 0;
                
                // Atualiza a posição real da cabeça baseada na direção atual
                const actualHead = {x: snake[0].x + dx, y: snake[0].y + dy};
                snake.unshift(actualHead);

                // Verifica se comeu o "deploy"
                if (actualHead.x === food.x && actualHead.y === food.y) {
                    score += 10;
                    scoreElement.innerText = score;
                    generateFood();
                } else {
                    snake.pop();
                }
            }

            function generateFood() {
                food.x = Math.floor(Math.random() * tileCount);
                food.y = Math.floor(Math.random() * tileCount);
                
                // Garante que a comida não spawne dentro da cobra
                snake.forEach(part => {
                    if (part.x === food.x && part.y === food.y) generateFood();
                });
            }

            function drawFood() {
                ctx.fillStyle = "#f35b14"; // Laranja (cor dos alertas/artefatos)
                ctx.fillRect(food.x * gridSize, food.y * gridSize, gridSize - 2, gridSize - 2);
            }

            function hasGameEnded() {
                // Bater no próprio corpo
                for (let i = 4; i < snake.length; i++) {
                    if (snake[i].x === snake[0].x && snake[i].y === snake[0].y) return true;
                }
                
                // Se preferir que bater nas paredes dê Game Over, descomente as linhas abaixo:
                /*
                const hitLeftWall = snake[0].x < 0;
                const hitRightWall = snake[0].x >= tileCount;
                const hitToptWall = snake[0].y < 0;
                const hitBottomWall = snake[0].y >= tileCount;
                return hitLeftWall || hitRightWall || hitToptWall || hitBottomWall;
                */
                return false;
            }

            function resetGame() {
                snake = [{x: 10, y: 10}];
                food = {x: 5, y: 5};
                dx = 1;
                dy = 0;
                score = 0;
                scoreElement.innerText = score;
            }

            // Captura as teclas de direção
            document.addEventListener("keydown", changeDirection);

            function changeDirection(event) {
                const keyPressed = event.keyCode;
                const KEY_LEFT = 37, KEY_A = 65;
                const KEY_UP = 38, KEY_W = 87;
                const KEY_RIGHT = 39, KEY_D = 68;
                const KEY_DOWN = 40, KEY_S = 83;

                const goingUp = dy === -1;
                const goingDown = dy === 1;
                const goingRight = dx === 1;
                const goingLeft = dx === -1;

                if ((keyPressed === KEY_LEFT || keyPressed === KEY_A) && !goingRight) { dx = -1; dy = 0; }
                if ((keyPressed === KEY_UP || keyPressed === KEY_W) && !goingDown) { dx = 0; dy = -1; }
                if ((keyPressed === KEY_RIGHT || keyPressed === KEY_D) && !goingLeft) { dx = 1; dy = 0; }
                if ((keyPressed === KEY_DOWN || keyPressed === KEY_S) && !goingUp) { dx = 0; dy = 1; }
            }

            // Inicia o loop do jogo
            setInterval(main, gameSpeed);
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    # Roda o app localmente na porta 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
