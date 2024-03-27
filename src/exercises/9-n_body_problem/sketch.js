/* Three Body Problem - http://www.scholarpedia.org/article/Three_body_problem */

let dt;

function setup() {
  createCanvas(windowWidth, windowHeight);
  frameRate(60);
  dt = 1/60;
  
  sun = new Body(100, createVector(width/2, height/2), createVector(0, 0), 50);
  planet = new Body(20, createVector(width/2, height/4), createVector(250, 0), 200);
  
  background(0);
}

function draw() {
  background(0, 50);

  sun.attract(planet);
  sun.show();
  planet.show();
}