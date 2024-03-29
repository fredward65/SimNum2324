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
  frameRate(2);
  cols = width / resolution;
  rows = height / resolution;

  model = tf.sequential();
  let hidden = tf.layers.dense({inputShape: [3], units: 3, activation: 'sigmoid'});
  let output = tf.layers.dense({units: 2, activation: 'sigmoid'});
  model.add(hidden);
  model.add(output);

  const optimizer = tf.train.adam(0.2);
  model.compile({optimizer: optimizer, loss: 'meanSquaredError'});

  for(let i = 0; i < 100; i++){
    let r_i = random(256);
    let g_i = random(256);
    let b_i = random(256);
    value_xs.push([r_i/255, g_i/255, b_i/255]);
    let ans = rule(r_i, g_i, b_i) ? [1, 0] : [0, 1]
    value_ys.push(ans);
  }
  
  train_xs = tf.tensor2d(value_xs);
  train_ys = tf.tensor2d(value_ys);

  setTimeout(train, 10);
  
  update();
  predict();
  // noLoop();
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
  xs = tf.tensor2d([[r/255, g/255, b/255]]);
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

    value_xs.push([r/256, g/256, b/256]);
    train_xs = tf.tensor2d(value_xs);
    train_ys = tf.tensor2d(value_ys);
  });

  let model_data = [];
  for (let elem of model.getWeights()) model_data.push(elem.dataSync());
  
  strokeWeight(2);
  fill(255);
  let n_in = [[3*width/8,  9*height/12],
              [3*width/8, 10*height/12],
              [3*width/8, 11*height/12]];
  let n_hd = [[width/2,  9*height/12],
              [width/2, 10*height/12],
              [width/2, 11*height/12]];
  let n_ou = [[5*width/8, 11*height/14],
              [5*width/8, 12*height/14]];           
  for (let i = 0; i < n_in.length; i++){
    for (let j = 0; j < n_hd.length; j++){
      stroke(0, 255 * (model_data[0][i + j*n_hd.length]));
      line(n_in[i][0], n_in[i][1], n_hd[j][0], n_hd[j][1]);
    }
  }
  for (let i = 0; i < n_hd.length; i++){
    for (let j = 0; j < n_ou.length; j++){
      stroke(0, 255 * (model_data[2][i + j*n_ou.length]));
      line(n_hd[i][0], n_hd[i][1], n_ou[j][0], n_ou[j][1]);
    }
  }
  stroke(0);
  for (let i = 0; i < n_in.length; i++) circle(n_in[i][0], n_in[i][1], 10);
  for (let i = 0; i < n_hd.length; i++){
    fill(255 * model_data[1][i]);
    circle(n_hd[i][0], n_hd[i][1], 10);
  }
  for (let i = 0; i < n_ou.length; i++){
    fill(255 * model_data[3][i]);
    circle(n_ou[i][0], n_ou[i][1], 10);
  }
  
  
}

function train() {
  trainModel().then(result => {
    console.log(result.params.samples);
  });
}

function trainModel() {
  return model.fit(train_xs, train_ys, {shuffle: true, epochs: 1});
}