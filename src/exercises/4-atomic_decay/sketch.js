let t, N_0, lambda, i;
let tableau = [];

function setup() {
  createCanvas(400, 300);
  i = 0;
  t = 0;
  N_0 = height;
  lambda = 3.8394E-12;
}

function draw() {
  background(0);
  /* N(t) = N_0 * e^(-lambda*t) */
  let N = N_0 * exp(-lambda*t);
  t += 100 * 365 * 24 * 3600;
  x = i;
  y = height - N;
  tableau.push([x, y]);
  noFill()
  beginShape()
  let flag = false;
  for (let point of tableau){
    stroke(255)
    if((height - point[1]) <= N_0 / 2 && !flag){
      stroke(0, 255, 255);
      strokeWeight(1);
      text(100 * point[0] + " ans", point[0] + 5, point[1])
      line(0, point[1], point[0], point[1]);
      line(point[0], height, point[0], point[1]);
      flag = true;
    }
    strokeWeight(3);
    vertex(point[0], point[1]);
  }
  endShape()
  strokeWeight(1);
  text(i * 100 + " ans", x + 5, y)
  i++;
  if(i > width) noLoop();
}