/* Three Body Problem - http://www.scholarpedia.org/article/Three_body_problem */

let dt;
let sun;
let planets = [];

function setup() {
  createCanvas(windowWidth, windowHeight);
  frameRate(60);
  dt = 1/60;
  
  sun = new Body(100, createVector(width/2, height/2), createVector(0, 0), 50);
  planets.push(sun);
  for(let i = 0; i < 3; i++){
    planets.push(new Body(random(10, 30),
                         createVector(random(width), random(height)), 
                         p5.Vector.random2D().mult(random(100)), random(360)))
  }

  background(0);
}

function draw() {
  background(0, 50);

  sun.show();
  for (let planet_c of planets){
    for (let planet of planets){
      if(planet != planet_c && planet!=sun){
        planet_c.attract(planet);
        planet.show();
      }
    }
  }
}