from engine import *

def update():
    mouse_pos = InputManager.mousePos()
    circle.position = Vector(mouse_pos[0], mouse_pos[1])
    circle.color = YELLOW
    if circle.collided: circle.color = GREEN
    if not rect.collided:
        rect.rotation += radians(1)

Scene.defaultCollider = True

Scene.setSize(1600, 900)

circle = Circle((0, 0), radius = 1)
rect = Rectangle((4, 3), rot = radians(10), scale = (3, 3), color = BLUE)

Scene.run(update)