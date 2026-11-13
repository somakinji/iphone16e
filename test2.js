const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreDisplay = document.getElementById("score");

let score = 0; //スコアの初期値

//プレイヤの設定
const player = {
    x: 140,
    y: 360,
    width: 60,
    height: 15,
    speed: 6
};

//ターゲットの設定
const target = {
    x: Math.random() * (canvas.width - 20),
    y: 0,
    size:20,
    speed: 3
};

//操作状態の設定
const move = {
    left: false,
    right: false
};
document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") move.left=true;
    if (e.key === "ArrowRight") move.right=true;
});
document.addEventListener("keyup", (e) => {
    if (e.key === "ArrowLeft") move.left=false;
    if (e.key === "ArrowRight") move.right=false;
});

//iphoneタッチボタンの対応
const leftBtn = document.getElementById("leftBtn");
const rightBtn = document.getElementById("rightBtn");

//左ボタン
leftBtn.addEventListener("touchstart", (e) => {e.preventDefault(); move.left=true;});
leftBtn.addEventListener("touchend", () => { move.left=false;});
leftBtn.addEventListener("mousedown", () => { move.left=true;});
leftBtn.addEventListener("mouseup", () => { move.left=false;});

//右ボタン
rightBtn.addEventListener("touchstart", (e) => {e.preventDefault(); move.right=true;});
rightBtn.addEventListener("touchend", () => { move.right=false;});
rightBtn.addEventListener("mousedown", () => { move.right=true;});
rightBtn.addEventListener("mouseup", () => { move.right=false;});

//ゲームループの設定
function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); //キャンバスをクリア

    if (move.left && player.x > 0) {player.x -= player.speed;}
    if (move.right && player.x + player.width < canvas.width) {player.x += player.speed;}

    target.y += target.speed; //ターゲットを下に移動

    //当たり判定
    if (target.x<player.x + player.width && target.x+target.size > player.x && target.y<player.y+player.height && target.y+target.size>player.y){
        score +=10;
        scoreDisplay.textContent = score; //スコア表示を更新
        resetTarger();
    }
    
    //ターゲットが画面下に到達したらリセット
    if (target.y > canvas.height) {
        resetTarger();
    }   

    //プレイヤーの描画
    ctx.fillStyle = "#0077b6";
    ctx.fillRect(player.x, player.y, player.width, player.height);

    ctx.fillStyle = "#e63946";
    ctx.fillRect(target.x, target.y, target.size, target.size);

    requestAnimationFrame(gameLoop); //次のフレームを描画
}

function resetTarger() {
    target.x = Math.random() * (canvas.width - target.size);
    target.y = 0;
}

//ゲーム開始
gameLoop();
