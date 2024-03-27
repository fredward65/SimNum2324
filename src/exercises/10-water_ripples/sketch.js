/* Water Ripples
https://web.archive.org/web/20160418004149/http://freespace.virgin.net/hugo.elias/graphics/x_water.htm
https://thecodingtrain.com/challenges/102-2d-water-ripple */

let buffer_1, buffer_2;
let damping;

function setup() {
  createCanvas(800, 600);
  frameRate(60);
  damping = 0.95;
  buffer_1 = new Array(width).fill(0).map(() => new Array(height).fill(0));
  buffer_2 = new Array(width).fill(0).map(() => new Array(height).fill(0));
}

function draw() {
  background(0);
  loadPixels();

  // Ripples loop
  for (let i = 1; i < width - 1; i++){
    for (let j = 1; j < height - 1; j++){
      // Buffer update

      let idx = 4*i + 4*j*width;
      pixels[idx + 0] = buffer_2[i][j];
      pixels[idx + 1] = buffer_2[i][j];
      pixels[idx + 2] = buffer_2[i][j];
      pixels[idx + 3] = 255;
    }
  }
  
  // Buffer swap
  let temp = buffer_2;
  buffer_2 = buffer_1;
  buffer_1 = temp;

  updatePixels();
}

function mouseDragged() {
  let x = int(mouseX);
  let y = int(mouseY);
  let r = 5;
  for (let i = -r; i <= r; i++){
    for (let j = -r; j <= r; j++){
      buffer_2[x + i][y + j] = 255;
    }
  }
}
