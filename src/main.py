from app import App

if __name__ == "__main__":
    App().run()



# OrbitSimulator/
# │
# ├── main.py
# │
# ├── app.py
# │
# ├── simulation/
# │   ├── __init__.py
# │   ├── simulation.py
# │   ├── body.py
# │   └── physics.py
# │
# ├── rendering/
# │   ├── __init__.py
# │   ├── renderer.py
# │   ├── ui_renderer.py
# │   ├── camera.py
# │   │
# │   └── shaders/
# │       ├── planet_vertex.glsl
# │       ├── planet_fragment.glsl
# │       ├── ui_vertex.glsl
# │       └── ui_fragment.glsl
# │
# ├── ui/
# │   ├── __init__.py
# │   ├── ui_manager.py
# │   ├── button.py
# │   ├── panel.py
# │   ├── slider.py
# │   └── textbox.py
# │
# └── assets/
#     ├── textures/
#     └── fonts/
