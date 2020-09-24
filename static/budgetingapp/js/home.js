
function hideCard(idText) { 
  document.getElementById(idText).style.display="none"; 
}

// MAIN COLOR: "rgb(193, 16, 137)" // TODO: Where to save this?
// TODO: Put this in a function?
$(document).ready(function(){
  var now = new Date();
  var hrs = now.getHours();
  var msg = "";
  if (hrs < 12 && hrs >=  0){
    msg = ("Good Morning");
  } else if (hrs < 17){
    msg = ("Good afternoon");
  } else {
    msg = ("Good evening");
  }
  document.getElementById('goodTimeText').innerHTML = msg;
  for (var i = 1; i <= 3; i++) { // TODO: Figure out how to make this not hard coded...
    var goalVal = document.getElementById('goalValue' + i).innerHTML;
    drawGoalSpeedometer('goalProgress' + i, goalVal);
  }
});
/* 
*/


///////////////////////////////////////////
//// Adapted from
// https://geeksretreat.wordpress.com/2012/04/13/making-a-speedometer-using-html5s-canvas/
///////////////////////////////////////////

/*jslint plusplus: true, sloppy: true, indent: 4 */
(function () {
    "use strict";
    // this function is strict...
}());

var bDecrement = null,
  job = null;

function degToRad(angle) {
  // Degrees to radians
  return ((angle * Math.PI) / 180);
}

function radToDeg(angle) {
  // Radians to degree
  return ((angle * 180) / Math.PI);
}

function drawLine(options, line) {
  // Draw a line using the line object passed in
  options.ctx.beginPath();

  // Set attributes of open
  options.ctx.globalAlpha = line.alpha;
  options.ctx.lineWidth = line.lineWidth;
  options.ctx.fillStyle = line.fillStyle;
  options.ctx.strokeStyle = line.fillStyle;
  options.ctx.moveTo(line.from.X,
    line.from.Y);

  // Plot the line
  options.ctx.lineTo(
    line.to.X,
    line.to.Y
  );

  options.ctx.stroke();
}

function createLine(fromX, fromY, toX, toY, fillStyle, lineWidth, alpha) {
  // Create a line object using Javascript object notation
  return {
    from: {
      X: fromX,
      Y: fromY
    },
    to: {
      X: toX,
      Y: toY
    },
    fillStyle: fillStyle,
    lineWidth: lineWidth,
    alpha: alpha
  };
}

function drawOuterMetallicArc(options) {
  /* Draw the metallic border of the speedometer 
   * Outer grey area
   */
  options.ctx.beginPath();

  // Nice shade of grey
  options.ctx.fillStyle = "rgb(127,127,127)";

  // Draw the outer circle
  options.ctx.arc(options.center.X,
    options.center.Y,
    options.radius,
    0,
    Math.PI,
    true);

  // Fill the last object
  options.ctx.fill();
}

function drawInnerMetallicArc(options) {
  /* Draw the metallic border of the speedometer 
   * Inner white area
   */

  options.ctx.beginPath();

  // White
  options.ctx.fillStyle = "rgb(255,255,255)";

  // Outer circle (subtle edge in the grey)
  options.ctx.arc(options.center.X,
          options.center.Y,
          (options.radius / 100) * 90,
          0,
          Math.PI,
          true);

  options.ctx.fill();
}

function drawMetallicArc(options) {
  /* Draw the metallic border of the speedometer
   * by drawing two semi-circles, one over lapping
   * the other with a bot of alpha transparency
   */

  drawOuterMetallicArc(options);
  drawInnerMetallicArc(options);
}

function drawBackground(options) {
  /* Black background with alphs transparency to
   * blend the edges of the metallic edge and
   * black background
   */
    var i = 0;

  options.ctx.globalAlpha = 0.2;
  options.ctx.fillStyle = "rgb(210, 161, 198)";
  // options.ctx.fillStyle = "rgb(193, 16, 137)";
  // options.ctx.fillStyle = "rgb(255, 255, 255)";

  // Draw semi-transparent circles
  for (i = 170; i < 180; i++) {
    options.ctx.beginPath();

    options.ctx.arc(options.center.X,
      options.center.Y,
      i,
      0,
      Math.PI,
      true);

    options.ctx.fill();
  }
}

function applyDefaultContextSettings(options) {
  /* Helper function to revert to gauges
   * default settings
   */

  options.ctx.lineWidth = 2;
  options.ctx.globalAlpha = 0.5;
  options.ctx.strokeStyle = "rgb(255, 255, 255)";
  options.ctx.fillStyle = 'rgb(255,255,255)';
}

function drawSmallTickMarks(options) {
  /* The small tick marks against the coloured
   * arc drawn every 5 mph from 10 degrees to
   * 170 degrees.
   */

  var tickvalue = options.levelRadius - 8,
      iTick = 0,
      gaugeOptions = options.gaugeOptions,
      iTickRad = 0,
      onArchX,
      onArchY,
      innerTickX,
      innerTickY,
      fromX,
      fromY,
      line,
    toX,
    toY;

  applyDefaultContextSettings(options);

  // Tick every 20 degrees (small ticks)
  for (iTick = 10; iTick < 180; iTick += 16) {

    iTickRad = degToRad(iTick);

    /* Calculate the X and Y of both ends of the
     * line I need to draw at angle represented at Tick.
     * The aim is to draw the a line starting on the 
     * coloured arc and continueing towards the outer edge
     * in the direction from the center of the gauge. 
     */

    onArchX = gaugeOptions.radius - (Math.cos(iTickRad) * tickvalue);
    onArchY = gaugeOptions.radius - (Math.sin(iTickRad) * tickvalue);
    innerTickX = gaugeOptions.radius - (Math.cos(iTickRad) * gaugeOptions.radius);
    innerTickY = gaugeOptions.radius - (Math.sin(iTickRad) * gaugeOptions.radius);

    fromX = (options.center.X - gaugeOptions.radius) + onArchX;
    fromY = (gaugeOptions.center.Y - gaugeOptions.radius) + onArchY;
    toX = (options.center.X - gaugeOptions.radius) + innerTickX;
    toY = (gaugeOptions.center.Y - gaugeOptions.radius) + innerTickY;

    // Create a line expressed in JSON
    line = createLine(fromX, fromY, toX, toY, "rgb(127,127,127)", 3, 0.6);

    // Draw the line
    drawLine(options, line);

  }
}

function drawLargeTickMarks(options) {
  /* The large tick marks against the coloured
   * arc drawn every 10 mph from 10 degrees to
   * 170 degrees.
   */

  var tickvalue = options.levelRadius - 8,
      iTick = 0,
        gaugeOptions = options.gaugeOptions,
        iTickRad = 0,
        innerTickY,
        innerTickX,
        onArchX,
        onArchY,
        fromX,
        fromY,
        toX,
        toY,
        line;

  applyDefaultContextSettings(options);

  tickvalue = options.levelRadius - 2;

  // 10 units (major ticks)
  for (iTick = 18; iTick < 170; iTick += 16) {

    iTickRad = degToRad(iTick);

    /* Calculate the X and Y of both ends of the
     * line I need to draw at angle represented at Tick.
     * The aim is to draw the a line starting on the 
     * coloured arc and continueing towards the outer edge
     * in the direction from the center of the gauge. 
     */

    onArchX = gaugeOptions.radius - (Math.cos(iTickRad) * tickvalue);
    onArchY = gaugeOptions.radius - (Math.sin(iTickRad) * tickvalue);
    innerTickX = gaugeOptions.radius - (Math.cos(iTickRad) * gaugeOptions.radius);
    innerTickY = gaugeOptions.radius - (Math.sin(iTickRad) * gaugeOptions.radius);

    fromX = (options.center.X - gaugeOptions.radius) + onArchX;
    fromY = (gaugeOptions.center.Y - gaugeOptions.radius) + onArchY;
    toX = (options.center.X - gaugeOptions.radius) + innerTickX;
    toY = (gaugeOptions.center.Y - gaugeOptions.radius) + innerTickY;

    // Create a line expressed in JSON
    line = createLine(fromX, fromY, toX, toY, "rgb(127,127,127)", 3, 0.6);

    // Draw the line
    drawLine(options, line);
  }
}

function drawTicks(options) {
  /* Two tick in the coloured arc!
   * Small ticks every 5
   * Large ticks every 10
   */
  drawSmallTickMarks(options);
  drawLargeTickMarks(options);
}

function drawTextMarkers(options) {
  /* The text labels marks above the coloured
   * arc drawn every 10 mph from 10 degrees to
   * 170 degrees.
   */
  var innerTickX = 0,
      innerTickY = 0,
        iTick = 0,
        gaugeOptions = options.gaugeOptions,
        iTickToPrint = 0;

  applyDefaultContextSettings(options);

  // Font styling
  options.ctx.font = 'italic 14px sans-serif';
  options.ctx.textBaseline = 'top';
  options.ctx.fillStyle = 'rgb(0,0,0)';

  options.ctx.beginPath();

  // Tick every 20 (small ticks)
  for (iTick = 10; iTick < 180; iTick += 16) {

    innerTickX = gaugeOptions.radius - (Math.cos(degToRad(iTick)) * gaugeOptions.radius);
    innerTickY = gaugeOptions.radius - (Math.sin(degToRad(iTick)) * gaugeOptions.radius);

    options.ctx.fillText((iTickToPrint*1).toString() + "%",
                         (options.center.X - gaugeOptions.radius - 28) + 1.1*innerTickX,
                         (gaugeOptions.center.Y - gaugeOptions.radius - 12) + innerTickY - 3);

    // MPH increase by 10 every 20 degrees
    iTickToPrint += 10; // Math.round(2160 / 9);
  }

    options.ctx.stroke();
}

function drawSpeedometerPart(options, alphaValue, strokeStyle, startPos) {
  /* Draw part of the arc that represents
  * the colour speedometer arc
  */

  options.ctx.beginPath();

  options.ctx.globalAlpha = alphaValue;
  options.ctx.lineWidth = 5;
  options.ctx.strokeStyle = strokeStyle;

  options.ctx.arc(options.center.X,
    options.center.Y,
    options.levelRadius,
    Math.PI + (Math.PI / 360 * startPos),
    0 - (Math.PI / 360 * 10),
    false);

  options.ctx.stroke();
}

function drawSpeedometerColourArc(options) {
  /* Draws the colour arc.  Three different colours
   * used here; thus, same arc drawn 3 times with
   * different colours.
   * TODO: Gradient possible?
   */

  // Arc goes from 10 to 170
  let colorArcParams = [
      [ 10,  "rgb(255, 255, 255)" ],
      [ 20,  "rgb(239, 239, 239)" ],
      [ 30,  "rgb(223, 223, 223)" ],
      [ 40,  "rgb(207, 207, 207)" ],
      [ 50,  "rgb(191, 191, 191)" ],
      [ 60,  "rgb(175, 175, 175)" ],
      [ 70,  "rgb(159, 159, 159)" ],
      [ 80,  "rgb(143, 143, 143)" ],
      [ 90,  "rgb(128, 128, 128)" ],
      [ 100, "rgb(112, 112, 112)" ],
      [ 110, "rgb( 96,  96,  96)" ],
      [ 120, "rgb( 80,  80,  80)" ],
      [ 130, "rgb( 64,  64,  64)" ],
      [ 140, "rgb( 48,  48,  48)" ],
      [ 150, "rgb( 32,  32,  32)" ],
      [ 160, "rgb( 16,  16,  16)" ],
      [ 170, "rgb(  0,   0,   0)" ],
  ]
  for ( var i = 0; i < colorArcParams.length; i++ ) {
    drawSpeedometerPart(options, 1.0, colorArcParams[i][1], colorArcParams[i][0]);
  }

}

function drawNeedleDial(options, alphaValue, strokeStyle, fillStyle) {
  /* Draws the metallic dial that covers the base of the
  * needle.
  */
    var i = 0;

  options.ctx.globalAlpha = alphaValue;
  options.ctx.lineWidth = 3;
  options.ctx.strokeStyle = strokeStyle;
  options.ctx.fillStyle = fillStyle;

  // Draw several transparent circles with alpha
  for (i = 0; i < 30; i++) {

    options.ctx.beginPath();
    options.ctx.arc(options.center.X,
      options.center.Y,
      i,
      0,
      Math.PI,
      true);

    options.ctx.fill();
    options.ctx.stroke();
  }
}

function convertSpeedToAngle(options) {
  /* Helper function to convert a speed to the 
  * equivelant angle.
  */
  var iSpeed = (options.speed / 100);
  if (iSpeed < 0) {
    iSpeed = 0;
  } else if (iSpeed > 1) {
    iSpeed = 1;
  }
  var iSpeedAsAngle = (iSpeed * (170 - 10)) + 10;

  return iSpeedAsAngle;
}

function drawNeedle(options) {
  /* Draw the needle in a nice read colour at the
  * angle that represents the options.speed value.
  */

  var iSpeedAsAngle = convertSpeedToAngle(options),
      iSpeedAsAngleRad = degToRad(iSpeedAsAngle),
        gaugeOptions = options.gaugeOptions,
        innerTickX = gaugeOptions.radius - (Math.cos(iSpeedAsAngleRad) * 20),
        innerTickY = gaugeOptions.radius - (Math.sin(iSpeedAsAngleRad) * 20),
        fromX = (options.center.X - gaugeOptions.radius) + innerTickX,
        fromY = (gaugeOptions.center.Y - gaugeOptions.radius) + innerTickY,
        endNeedleX = gaugeOptions.radius - (Math.cos(iSpeedAsAngleRad) * gaugeOptions.radius),
        endNeedleY = gaugeOptions.radius - (Math.sin(iSpeedAsAngleRad) * gaugeOptions.radius),
        toX = (options.center.X - gaugeOptions.radius) + endNeedleX,
        toY = (gaugeOptions.center.Y - gaugeOptions.radius) + endNeedleY,
        backLine = createLine(fromX, fromY, toX, toY, "rgb(255, 255, 255)", 12, 0.6),
        line = createLine(fromX, fromY, toX, toY, "rgb(193, 16, 137)", 9, 0.6);

  drawLine(options, backLine);
  drawLine(options, line);

  // Two circle to draw the dial at the base (give its a nice effect?)
  // 96, 8, 70
  drawNeedleDial(options, 1.0, "rgb(255, 255, 255)", "rgb(255,255,255)");
  // drawNeedleDial(options, 0.2, "rgb(210, 161, 198)", "rgb(210, 161, 198)");
  drawNeedleDial(options, 0.2, "rgb(193, 16, 137)", "rgb(193, 16, 137)");
  // drawNeedleDial(options, 0.6, "rgb(127, 127, 127)", "rgb(255,255,255)");
  // drawNeedleDial(options, 0.2, "rgb(127, 127, 127)", "rgb(127,127,127)");

}

function buildOptionsAsJSON(canvas, iSpeed) {
  /* Setting for the speedometer 
  * Alter these to modify its look and feel
  */

  var centerX = 210,
      centerY = 210,
        radius = 140,
        outerRadius = 200;

  // Create a speedometer object using Javascript object notation
  return {
    ctx: canvas.getContext('2d'),
    speed: iSpeed,
    center: {
      X: centerX,
      Y: centerY
    },
    levelRadius: radius - 10,
    gaugeOptions: {
      center: {
        X: centerX,
        Y: centerY
      },
      radius: radius
    },
    radius: outerRadius
  };
}

function clearCanvas(options) {
  options.ctx.clearRect(0, 0, 800, 600);
  applyDefaultContextSettings(options);
}

function drawGoalSpeedometer(canvasId, targetValue) {
  /* Main entry point for drawing the speedometer
  * If canvas is not support alert the user.
  */
  if (isNaN(targetValue)) {
    iTargetSpeed = 0;
  } else if (targetValue < 0) {
    iTargetSpeed = 0;
  } else if (targetValue > 100) {
    iTargetSpeed = 100;
  }
    
  // console.log('Target: ' + targetValue);
  
  var canvas = document.getElementById(canvasId),
      options = null;

  // Canvas good?
  if (canvas !== null && canvas.getContext) {
    options = buildOptionsAsJSON(canvas, targetValue);

      // Clear canvas
      clearCanvas(options);

    // Draw the metallic styled edge
    // drawMetallicArc(options);

    // Draw thw background
    drawBackground(options);

    // Draw tick marks
    drawTicks(options);

    // Draw labels on markers
    drawTextMarkers(options);

    // Draw speeometer colour arc
    drawSpeedometerColourArc(options);

    // Draw the needle and base
    drawNeedle(options);
    
  } else {
    alert("Canvas not supported by your browser!");
  }
}

/////////////////////////////////////////////////////////////
// Display
/////////////////////////////////////////////////////////////

function showTabs(tabs) { // sTabs = shownTabs, aTabs = availableTabs
  for (var tabId in tabs) {
      console.log(tabId);
      if (tabs[tabId] === 0) {
        document.getElementById(tabId).style.display = "inline";
      } else {
        document.getElementById(tabId).style.display = "none";
      }
  }
}

var tab_html_arr = document.getElementsByClassName("rec-tab");
var tabs = {};
for (var i = 0; i < tab_html_arr.length; i++) {
  var tabIdx = parseInt(i)+1; // Javascript issues
  var tabId = "rec" + tabIdx;
  if (i < 3) {
    tabs[tabId] = 0;
  } else {
    tabs[tabId] = 1;
  }
}
console.log(tab_html_arr);
console.log(tabs);
showTabs(tabs)

function updateTabs(tabId) {
  tabs[tabId] = 2;
  for (var tabId in tabs) {
      console.log(tabId);
      if (tabs[tabId] === 1) {
        tabs[tabId] = 0;
        break;
      }
  }
  showTabs(tabs);
}




