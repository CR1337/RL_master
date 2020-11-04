class Button {
  constructor(handler, tooltip) {
    this.handler = handler;
    this.tooltip = tooltip;
    this.enabled = true;
    this.size = 50;
    this.margin = 6;
    this.y = -1;
    this.x = -1;

    this.clicked = 0;
    this.flashing = 0;
    this.flash_color = color(0);
    this.flash_frames = 30;

    this.fade_color = color(0);
    this.fading = false;
    this.fade_counter = 0.0;
  }

   set left(x) {
  this.x = x;
 }

 set top(y) {
  this.y = y;
 }
}

class SimpleButton extends Button {
 constructor(handler, tooltip, picture) {
    super(handler, tooltip);
    this.picture = picture;
    this.disabled_picture = picture;
    this.disabled_picture.filter(GRAY);
 }

 draw() {
   if (this.clicked > 0) {
     this.clicked -= 1;
     stroke(255);
     strokeWeight(4);
   } else {
     stroke(128);
     strokeWeight(2);
   }
   let img;
   if (this.enabled) {
     if (this.flashing > 0) {
       let flash_ratio = this.flashing / this.flash_frames;
       fill(lerpColor(color(0), this.flash_color, flash_ratio));
       this.flashing -= 1;
     } else if (this.fading) {
       let fade_ratio = sin(this.fade_counter);
       fill(lerpColor(color(0), this.fade_color, fade_ratio * fade_ratio));
       this.fade_counter += 0.1;
     } else {
       fill(0);
     }
     img = this.picture;
   } else {
     fill(64);
     img = this.disabled_picture;
   }
   square(this.x, this.y, this.size, 10);
   image(img, this.x + this.margin, this.y + this.margin, this.size - 2 * this.margin, this.size - 2 * this.margin);
 }

 click(x, y) {
   if (x < this.x || x > this.x + this.size || y < this.y || y > this.y + this.size) {
      return;
   }
   if (!this.enabled) {
     return;
   }
   this.clicked = 4;
   this.handler(this);
 }

 flash(color) {
   this.stop_fading();
   this.flash_color = color;
   this.flashing = this.flash_frames;
 }

 fade(color) {
   this.flashing = 0;
   this.fading = true;
   this.fade_color = color;
   this.fade_counter = 0;
 }

 stop_fading() {
  this.fading = false;
 }
}