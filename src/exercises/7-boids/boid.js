class Boid {
  constructor(x, y, color = 255){
    this.pos = createVector(x, y);
    this.vel = 10;
    this.dir = p5.Vector.random2D().mult(this.vel);
    this.size = 50;
    this.color = color;
    this.view_r = 100;
  }

  separation(others){
    let vec = createVector(0, 0);
    
    return vec;
  }

  alignment(others){
    let mean = createVector(0, 0);
    
    return mean;
  }
  
  cohesion(others){
    let mean = createVector(0, 0);
    
    return mean;
  }

  steer(others){
    let sep = this.separation(others);
    let ali = this.alignment(others);
    let coh = this.cohesion(others);
    let total = createVector(0, 0);
    total.add(sep.mult(1));
    total.add(ali.mult(1));
    total.add(coh.mult(1));
    this.dir.add(total.limit(10));
    this.dir.limit(this.vel);
  }

  update(){
    this.pos.add(this.dir);
    if(this.pos.x < 0) this.pos.x = width;
    if(this.pos.y < 0) this.pos.y = height;
    if(this.pos.x > width) this.pos.x = 0;
    if(this.pos.y > height) this.pos.y = 0;
  }

  show(){
    let a = floor(this.size / 2);
    let b = floor(a / 2);
    let angle = this.dir.heading();
    noStroke();
    fill(this.color);
    push();
    translate(this.pos.x, this.pos.y);
    rotate(angle - 0.5*PI)
    triangle(-b, -a, 0, a/2, b, -a);
    pop();
  }
}