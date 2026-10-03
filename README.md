# N-Body Simulation with ModernGL UI Engine

A Python based N-body gravitational simulation featuring a freely controllable camera and a resolution independent UI made from scratch and rendered with GPU shaders using Pygame ModernGl and glsl. Uses velocity verlet integration to handle the equations of motion and orbital physics as it is relatively simple to code and helps prevent energy creep.

## Features:
- A fully moveable camera with two modes:
  - **Locked**: Follows one body, can be rotated around the body by clicking and dragging, and zoomed in and out with the mouse wheel.
  - **free**: Able to move around the simulation as a whole, uses WASD to slide up, down, left and right, clicking and dragging rotates the camera around and the mouse wheel moves it forwards and backwards.

- A custom designed UI which makes use of several different techniques:
  - **SDF Styling**: UI elements make use of an SDF function for smooth edges, anti aliasing and rounded corners.
  - **Dynamic Sizing**: Uses the ratio of the active screen and 1440p to scale all UI elements to the correct size for the screen.
  - **Text Rendering**: Uses PyGame to create transparent surfaces with text on them, makes textures out of these surfaces to be added to textboxes.

- UI features built completely from scratch including buttons, panels and textboxes which can have labels, rounded edges and shadows. All custom made with ModernGL and glsl.

- A Sandbox simulation using velocity verlet integration with:
  - **Changeable Speed**: The user can change the speed multiplier of the simulation, with larger values causing the physics loop to be broken into steps, preventing bodies from flying away due to massive jumps.
  - **Custom Bodies**: The user can enter their own celestial bodies where they can specify attributes such as spin, radius, density, tilt and initial velocity.
  - **Pre-sets**: The user can choose to add several pre made bodies with attributes accurate to their real world counterparts, these include Mars, Earth, The moon and more. The XZ plane is treated as the plane of the ecliptic and all values are relative to it.
  - **Orbit Trails**: The user can choose to display the orbit paths of each body as a thin white circle.

- All planetary data is saved to JSON file on close and loaded when run again.

## Technologies Used:
- **Main Language**: Python
- **Secondary Language**: GLSL
- **Libraries**: PyGame, ModernGL, Numpy, Math, PyGLM
