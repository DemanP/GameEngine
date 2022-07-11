from engine import *

def update():
    if not player.collision(platform):
        player.gravity()
    if InputManager.keyDown('a'):
        player.position.x -= 0.1
    if InputManager.keyDown('d'):
        player.position.x += 0.1
    if InputManager.keyDown('space') and player.collided:
        player.force((0, -1.5))

player = Square(Vector(0, -1), color = '#ff0', mass = 10)
player.collider = True
player.tag = 'player'
platform = Square(Vector(0, 0), scale = Vector(5, 1), color = '#00f')

Screen.run(update)