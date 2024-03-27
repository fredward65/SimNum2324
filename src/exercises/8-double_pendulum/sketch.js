/* myPhysicsLab Double Pendulum
https://www.myphysicslab.com/pendulum/double-pendulum-en.html */

let m1 = 0.5;
let m2 = 0.5;
let l1 = 0.1;
let l2 = 0.2;
let fac = 1000;
let a_g = 9.80665;
let th_1, th_2, dth_1, dth_2, ddth_1, ddth_2, dt;


function setup() {
  createCanvas(windowWidth, windowHeight);
  frameRate(60);
  dt = 1/60;

  th_1 = PI * 0.25
  th_2 = PI * 0.30
  dth_1 = 0;
  dth_2 = 0;
}

function draw() {
  background(255, 100);
  translate(width/2, height/2);
  stroke(255);
  
  ddth_1 = 0;
  ddth_2 = 0;

  dth_1 += ddth_1 * dt;
  dth_2 += ddth_2 * dt;
  th_1 += dth_1 * dt;
  th_2 += dth_2 * dt;

  let x1 = (th1) => {return fac*l1*sin(th1)};
  let y1 = (th1) => {return fac*l1*cos(th1)};
  let x2 = (th1, th2) => {return x1(th1) + fac*l2*sin(th2)};
  let y2 = (th1, th2) => {return y1(th1) + fac*l2*cos(th2)};
  
  strokeWeight(3);
  stroke(0, 0, 255);
  line(0, 0, x1(th_1), y1(th_1));
  stroke(255, 0, 0);
  line(x1(th_1), y1(th_1), x2(th_1, th_2), y2(th_1, th_2));
  noStroke();
  fill(0, 0, 255);
  circle(x1(th_1), y1(th_1), 20);
  fill(255, 0, 0);
  circle(x2(th_1, th_2), y2(th_1, th_2), 20);
}
