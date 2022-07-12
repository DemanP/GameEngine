from engine import *

def update():
    mouse_pos = InputManager.mousePos()
    circle.position = Vector(mouse_pos[0], mouse_pos[1])
    circle.color = YELLOW
    if circle.collided: circle.color = GREEN

Scene.defaultCollider = True

circle = Circle((0, 0), radius = 1)
rect = Rectangle((0, 0), rot = radians(10), scale = (3, 3), color = BLUE)

Scene.run(update)