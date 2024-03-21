let r, y, x, dt, ddy, dy, y_repos, k, c;
const fac = 1000;

function setup() {
  createCanvas(400, 400);
  frameRate(60);
  dt = 1/60;
  k = 8;
  c = 2;
  r = 75;
  y_repos = 0.10;
  x = width/2;
  dy = 0;
  y = y_repos * 3;
}

function draw() {
  background(0);
  ddy = -(k * (y - y_repos)) -(c * dy);
  dy = dy + ddy * dt;
  y = y + dy * dt;
  stroke(255);
  strokeWeight(5);
  line(x, 0, x, y * fac);
  strokeWeight(1);
  line(0, y_repos * fac, width, y_repos * fac);
  noStroke();
  circle(x, y * fac, r);
}

function mousePressed(){
  y = mouseY / fac;
  dy = 0;
}