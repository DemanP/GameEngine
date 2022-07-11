from engine import *

def update():
    speed = Vector(0.25, 0)
    if InputManager.keyDown('a'): player.position -= speed
    if InputManager.keyDown('d'): player.position += speed
    if InputManager.keyDown('space') and player.collided: player.force((0, 1))

platform = Rectangle(Vector(0, -5), radians(0), scale = Vector(5, 1), color = '#00f')
player = Rectangle(Vector(0, 1), color = '#ff0', mass = 10)
player.collider = True
player.have_gravity = True

Screen.run(update)