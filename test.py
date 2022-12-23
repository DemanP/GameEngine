from engine import *

def update():
    rect.rotation += radians(1)

def on_click(btn):
    global count
    count += 1
    text.text = count

global count
count = 0

Scene.defaultCollider = True

Scene.setSize(1600, 900)

circle = Circle((0, 0), radius = 1, color = Color.YELLOW)
rect = Polygon((4, 3), rot = radians(10), scale = (3, 3), color = Color.BLUE)
text = Text(pos = (-11, -7.5), size = 1.25, text = count, color = Color.WHITE)
btn = Button(pos = (-3, -2), scale = (2, 1), color = Color.RED, text = 'Click', highlight_color = Color.GREEN, onclick = on_click)

Scene.run(update)