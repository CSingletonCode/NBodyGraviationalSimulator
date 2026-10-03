# N-Body Simulation with ModernGL UI Engine

A Python based N-body gravitational simulation featuring a freely controllable camera and a resolution independent UI made from scratch and rendered with GPU shaders using Pygame ModernGl and glsl. Uses velocity verlet integration to handle the equations of motion and orbital physics as it is relatively simple to code and helps prevent energy creep.

## Features:
- A fully moveable camera with two modes:
  - **Locked**: Follows one body, can be rotated around the body by clicking and dragging, and zoomed in and out with the mouse wheel.
  - **free**: Able to move around the simulation as a whole, uses WASD to slide up, down, left and right, clicking and dragging rotates the camera around and the mouse wheel moves it forwards and backwards.
