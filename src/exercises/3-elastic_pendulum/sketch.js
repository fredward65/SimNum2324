let r, x, y, dt, l, dl, ddl, ddth, dth, th;
const fac = 250;
const l_0 = 200 / fac;
const a_g = 9.80665;
const m = 0.1;
const k = 1;
let tableau = [];

function setup() {
  /* Parametres */
  createCanvas(400, 400);
  frameRate(60);
  r = 75;
  dt = 1/60;
  l = l_0 * 1.5;
  dl = 0;
  th = PI/8;
  dth = 0;
}

function draw() {
  /* Boucle Dessin */
  background(0);
  ll = l_0 + l;
  ddl = ll*(dth*dth) - (k/m)*l + a_g*cos(th);
  ddth = -(a_g/ll)*sin(th) -((2*dl)/ll)*dth;
  dl += ddl * dt;
  l += dl * dt;
  dth += ddth * dt;
  th += dth * dt;
  x = fac * l * sin(th) + width/2;
  y = fac * l * cos(th);
  tableau.push([x, y]);
  stroke(255, 100);
  strokeWeight(1);
  noFill();
  beginShape();
  for(let point of tableau){
    vertex(point[0], point[1]);
  }
  endShape();
  stroke(255);
  strokeWeight(5);
  line(width/2, 0, x, y);
  noStroke();
  fill(255,0,0);
  circle(x, y, r);
}