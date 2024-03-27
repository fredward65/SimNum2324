let G = 6.67408;  // 6.67408e-11 N m^2 / kg^2

class Body {
  constructor(radius, pos, vel, col){
    this.pos = pos;
    this.vel = vel;
    this.mass = radius * 2e4;
    this.radius = radius;
    this.F = createVector(0, 0);
    colorMode(HSB);
    this.color = color(col, 100, 100);
    colorMode(RGB);
  }

  attract(other){
    /* F = G * (m1 * m2) / (d**2) */
    let d = p5.Vector.dist(this.pos, other.pos);
    let F = createVector(0, 0);
    if(d > this.radius + other.radius){
      let F_mag = G * (this.mass * other.mass) / (d*d);
      let F_dir = p5.Vector.sub(this.pos, other.pos);
      F = F_dir.setMag(F_mag);
    }
    other.applyForce(F);
  }

  applyForce(F){
    this.F.add(F);
  }

  update(){
    let acc = p5.Vector.div(this.F, this.mass);
    this.vel.add(p5.Vector.mult(acc, dt));
    this.pos.add(p5.Vector.mult(this.vel, dt));
    this.F = createVector(0, 0);

    // if(this.pos.x < 0) this.pos.x = width;
    // if(this.pos.y < 0) this.pos.y = height;
    // if(this.pos.x > width) this.pos.x = 0;
    // if(this.pos.y > height) this.pos.y = 0;
    
    if(this.pos.x < 0 || this.pos.x > width) this.vel.x *= -1;
    if(this.pos.y < 0 || this.pos.y > height) this.vel.y *= -1;
  }

  show(){
    this.update();
    noStroke();
    fill(this.color);
    circle(this.pos.x, this.pos.y, this.radius * 2);
  }
}