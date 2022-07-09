from tkinter import *
from time import sleep, time
from keyboard import is_pressed

def tick(time1, time2, FPS):
    sleep(time2-time1+1/FPS)

BLACK = '#000'
WHITE = '#fff'

width, height = 700, 500
tk = Tk()
canvas = Canvas(width = width, height = height, bg = BLACK, highlightthickness=0)
canvas.pack()

class InputManager:
    def __init__(self):
        pass
    def keyDown(key):
        return is_pressed(key)

class Vector:
    unit = 50
    def __init__(self, x  = 0, y = 0, angle = 0):
        self.x = x
        self.y = y
        self.angle = angle
    def __add__(self, other):
        if type(other) == Vector:
            x = self.x + other.x
            y = self.y + other.y
            return x, y
    def __repr__(self) -> tuple:
        return (self.x, self.y)
    def __str__(self):
        return 'Just Vector :)'
# test comment
class Entity:
    def __init__(self, pos = None, rot = None, color = WHITE):
        if not pos:
            pos = Vector(0, 0)
        if not rot:
            rot = Vector(angle = 0)
        self.position = pos
        self.rotation = rot

        self.color = color

        all_entities.append(self)
    def update(self):
        self.draw()
class Square(Entity):
    def __init__(self, pos = None, rot = None, scale = None):
        super().__init__(pos, rot)
        if not scale:
            scale = Vector(1, 1)
        self.scale = scale

        self.verticies = [Vector(x, y) for x in [-scale.x/2, scale.x/2] for y in [-scale.y/2, scale.y/2]]
    def draw(self):
        left_corner, right_corner = self.verticies[0], self.verticies[3]
        draw_verticies = [left_corner.x + self.position.x, left_corner.y + self.position.y, right_corner.x + self.position.x, right_corner.y + self.position.y]
        draw_verticies = [pos * Vector.unit for pos in draw_verticies]
        for i, v in enumerate(draw_verticies):
            if i % 2:
                draw_verticies[i] += height//2
            else:
                draw_verticies[i] += width//2
        print(draw_verticies)
        canvas.create_rectangle(draw_verticies, fill = self.color)

all_entities = []

obj = Square(Vector(0, 0))

while 1:
    time1 = time()
    canvas.delete('all')

    for entity in all_entities:
        entity.update()
    
    if InputManager.keyDown('a'):
        obj.position.x -= 0.1

    time2 = time()
    tick(time1, time2, 30)

    tk.update_idletasks()
    tk.update()