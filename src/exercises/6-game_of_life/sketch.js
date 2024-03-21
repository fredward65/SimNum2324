/* The Game of Life, by John Conway - https://web.stanford.edu/class/sts145/Library/life.pdf */

let res = 10;
let cols, rows;
let grid;
let start = false;

function setup() {
  createCanvas(800, 600);
  frameRate(30);
  cols = floor(width  / res);
  rows = floor(height / res);
  grid = new Array(cols).fill(0).map(() => new Array(rows).fill(0));
  for (let i = 0; i < grid.length; i++){
    for (let j = 0; j < grid[j].length; j++){
      grid[i][j] = int(random(0, 2));
    }
  }
}

function draw() {
  background(0);
  stroke(128 * (1 - start), 128 * start, 128 * start);

  if (start){
    /* Game rules here */
    let n_grid = new Array(cols).fill(0).map(() => new Array(rows).fill(0));
    
    for (let i = 0; i < grid.length; i++){
      for (let j = 0; j < grid[j].length; j++){
        let current_cell = grid[i][j]; // CURRENT CELL
        n_grid[i][j] = current_cell;

        let counter = 0;
        for (let x = -1; x <= 1; x++){
          for (let y = -1; y <= 1; y++){
            let x_ = (grid.length + i + x) % grid.length;
            let y_ = (grid[j].length + j + y) % grid[j].length;
            if(!(x == 0 && y == 0)){
              counter += grid[x_][y_] // CURRENT NEIGHBOUR
            }
          }
        }

        if(current_cell == 0 && counter == 3){
          n_grid[i][j] = 1;
        }
        if(current_cell == 1 && !(counter == 2 || counter == 3)){
          n_grid[i][j] = 0;
        }
      }
    }

    grid = n_grid;
  }

  for (let i = 0; i < grid.length; i++){
    for (let j = 0; j < grid[j].length; j++){
      let state = 255 * grid[i][j];
      fill(state);
      square(i * res, j * res, res);
    }
  }
}

function mouseClicked() {
  let i = floor(mouseX / res);
  let j = floor(mouseY / res);
  grid[i][j] = 1 - grid[i][j];
}

function keyPressed() {
  if (keyCode === ENTER){
    start = !start;
  }
  if (keyCode === BACKSPACE){
    grid = new Array(cols).fill(0).map(() => new Array(rows).fill(0));
    start = false;
  }
}