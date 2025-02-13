var canvas = document.getElementById("myCanvas");
const redColor = "#FF0000";
const glowColor = "#eb96a1";
const bgColor = "#21012b";
var c = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var w = canvas.width;
var h = canvas.height;


var initBubbles = 50;
var minBubbles = 15;
//var B = new Bubble (100, 100, 20, 0, -2);
//B.draw();
var bubbles = [];

//event listener on page open
window.addEventListener("load", init)

// init as a simple game engine for looping and drawing
function init () {
    // fills array with bubbles
    while (bubbles.length < initBubbles) {
        bubbles.push(createBubble());
    }
    //console.log(bubbles)

    // draw function goes here
    draw();
}



function Bubble(x, y, r, vx, vy) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.vx = vx;
    this.vy = vy;
    this.color = glowColor;
    this.draw = function() {

        c.beginPath();
        c.fillStyle= this.color;
        c.arc(this.x, this.y, this.r, 0, 2*Math.PI, false);
        c.fill();
        c.closePath();

        c.beginPath();
        c.fillStyle= redColor;
        c.shadowBlur = 70;
        c.shadowColor = redColor;
        c.arc(this.x, this.y, this.r - (r/10), 0, 2*Math.PI, false);
        c.fill();
        c.closePath();

    }
}

// bubble ramdomizer

function createBubble() {
    var r = Math.floor(Math.random()*11)  + 10; // from 10 px to 40 px
    var x = Math.random() * w;
    var y = Math.random() * h;
    // velocity
    var vx = (Math.random() * 4) - 2;
    var vy = - (Math.random() * 3) - 1;
    //bubble generate
    return new Bubble(x, y, r, vx, vy)

}



function draw () {
    //bg paint
    c.fillStyle = bgColor;
    c.fillRect(0, 0, w, h);

    //loop and bubble drawing from array
    for (var i =0; i< bubbles.length; i++) {
        var currentBubble = bubbles[i];
        
        //update position of bubbles
        currentBubble.x += currentBubble.vx;
        currentBubble.y += currentBubble.vy;
        currentBubble.draw();


        //restart loop after initial 50 bubbles
        if (currentBubble.x > w || currentBubble.x < 0 || currentBubble.y < 10) {
            bubbles.splice(i,1);
            if(bubbles.length <= minBubbles) {
                bubbles.splice(i, 0, createBubble());
            }
        }
    }

    //starts loop and animates
    requestAnimationFrame(draw);

}