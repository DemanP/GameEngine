from engine import *

def update():
    mouse_pos = InputManager.mousePos()
    circle.position = Vector(mouse_pos[0], mouse_pos[1])
    circle.color = 'yellow'
    if circle.collided: circle.color = '#0f0'

Scene.defaultCollider = True

circle = Circle((-1, 0), radius = 0.5, color = 'yellow')
rect = Rectangle((6, 0), color = 'blue')

Scene.run(update)