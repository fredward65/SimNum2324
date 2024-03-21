let r, y, x, l, dt, ddth, dth, th;
const fac = 1000;
const a_g = 9.80665;

function setup() {
  createCanvas(400, 400);
  frameRate(60);
  dt = 1/60;
  th = PI/5;
  r = 75;
  l = 200 / fac;
  dth = 0;
}

function draw() {
  background(0);
  ddth = -(a_g / l) * sin(th) - 0.75 * dth;
  dth += ddth * dt;
  th += dth * dt;
  x = fac * l * sin(th) + width/2;
  y = fac * l * cos(th);
  stroke(255);
  strokeWeight(5);
  line(width/2, 0, x, y);
  noStroke();
  fill(255,0,0);
  circle(x, y, r);
}