/* Color Predictor with tf.js
https://thecodingtrain.com/challenges/99-neural-network-color-predictor */

let model;

let resolution = 20;
let cols, rows;

let xs;

let train_xs;
let train_ys;
let value_xs = [];
let value_ys = [];
 
let r, g, b;
let rule = (r_, g_, b_) => {return (r_ + g_ + b_)/3 > 256/2};

function setup() {
  createCanvas(800, 600);
  frameRate(3);
  cols = width / resolution;
  rows = height / resolution;

  model = tf.sequential();
  let hidden = tf.layers.dense({inputShape: [3], units: 3, activation: 'sigmoid'});
  let output = tf.layers.dense({units: 2, activation: 'sigmoid'});
  model.add(hidden);
  model.add(output);

  const optimizer = tf.train.adam(0.2);
  model.compile({optimizer: optimizer, loss: 'meanSquaredError'});

  for(let i = 0; i < 1; i++){
    let r_i = random(256);
    let g_i = random(256);
    let b_i = random(256);
    value_xs.push([r_i, g_i, b_i]);
    let ans = rule(r_i, g_i, b_i) ? [1, 0] : [0, 1]
    value_ys.push(ans);
  }
  
  train_xs = tf.tensor2d(value_xs);
  train_ys = tf.tensor2d(value_ys);

  setTimeout(train, 10);
  
  update();
  predict();
}

function draw(){
  update();
  predict();
  setTimeout(train, 10);
}


function update(){
  r = random(256);
  g = random(256);
  b = random(256);
  xs = tf.tensor2d([[r, g, b]]);
  background(r, g, b);
  noStroke();
  textAlign(CENTER, CENTER);
  textSize(50);
  fill(0);
  text("BLACK", width/4, height/2);
  fill(255);
  text("WHITE", 3*width/4, height/2);
  strokeWeight(10);
  stroke(256-r, 256-g, 256-b);
  line(width/2, 0, width/2, height);
}

function predict(){
  tf.tidy(() => {
    let ys = model.predict(xs);
    let y_vals = ys.dataSync();

    let side = y_vals[0] > y_vals[1] ? 1 : 3;
    noStroke();
    fill(floor(side / 3) * 255)
    circle(side * width/4, 3*height/4, 100);
    let true_val = rule(r, g, b) ? 1 : 3;
    fill(floor(true_val / 3) * 255)
    circle(true_val * width/4, 1*height/4, 100);

    // let y_user = mouseX < width/2 ? [1, 0] : [0, 1];
    // value_ys.push(y_user);
    value_ys.push([1 - floor(true_val / 3), floor(true_val / 3)])
    value_xs.push([r, g, b]);
    train_xs = tf.tensor2d(value_xs);
    train_ys = tf.tensor2d(value_ys);
  });
}

function train() {
  trainModel().then(result => {
    console.log(result);
  });
}

function trainModel() {
  return model.fit(train_xs, train_ys, {shuffle: true, epochs: 1});
}