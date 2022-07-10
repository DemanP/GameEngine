from tkinter import *
from time import sleep, time
from keyboard import is_pressed
import matrix
from math import radians, degrees
from copy import copy

def tick(time1, time2, FPS):
    sleep(time2-time1+1/FPS)

BLACK = '#000'
WHITE = '#fff'


def empty():
    pass

class Screen:
    all_entities = []
    width, height = 1000, 800
    tk = Tk()
    canvas = Canvas(width = width, height = height, bg = BLACK, highlightthickness=0)
    canvas.pack()
    def run(update = empty):
        while 1:
            core_Engine_update(update)
    def refresh():
        Screen.tk.update_idletasks()
        Screen.tk.update()
        Screen.canvas.delete('all')

class InputManager:
    def __init__(self):
        pass
    def keyDown(key):
        return is_pressed(key)
    def mousePos():
        mouse_x = (Screen.tk.winfo_pointerx() - Screen.tk.winfo_rootx() - Screen.width//2) / Vector.unit
        mouse_y = (Screen.tk.winfo_pointery() - Screen.tk.winfo_rooty() - Screen.height//2) / Vector.unit
        return mouse_x, mouse_y

class Vector:
    unit = 50
    def normalise(self):
        max_n = max(abs(self.x), abs(self.y))
        self.x, self.y = self.x / max_n, self.y / max_n
    def getPosition(self):
        return (self.x,), (self.y,)
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
    def __mul__(self, other):
        if type(other) == Vector:
            x = self.x * other.x
            y = self.y * other.y
            return x, y
        if type(other) == int:
            x = self.x * other
            y = self.y * other
            return x, y
    def __rmul__(self, other):
        return self.__mul__(other)
    def __sub__(self, other):
        if type(other) == Vector:
            x = self.x - other.x
            y = self.y - other.y
            return x, y
class Entity:
    def __init__(self, pos = None, rot = 0, color = WHITE, mass = 4):
        # if not pos:
        #     pos = Vector(0, 0)
        self.position = pos
        self.rotation = rot
        self.color = color

        self.collider = False
        self.collided = False

        self.tag = None

        self.accX = 0
        self.accY = 0
        self.velX = 0
        self.velY = 0

        self.mass = mass

        Screen.all_entities.append(self)
    def gravity(self):
        self.force(0, self.mass*g)
    def force(self, x, y):
        fX = x / Vector.unit / 100
        fY = y / Vector.unit / 100
        self.accX += fX
        self.accY += fY
class Square(Entity):
    def __init__(self, pos = copy(Vector(0, 0)), rot = 0, scale = None, color = WHITE):
        super().__init__(pos, rot, color)
        if not scale:
            scale = Vector(1, 1)
        self.scale = scale
        self.last_rotation = 0

        self.verticies = [Vector(x, y) for x in [-scale.x/2, scale.x/2] for y in [-scale.y/2, scale.y/2]]
        self.verticies[2], self.verticies[3] = self.verticies[3], self.verticies[2]
    def update(self):
        # if self.collider:
        #     for __ent_ in all_entities:
        if not self.collided:
            self.velX += self.accX
            self.velY += self.accY
            # if abs(self.velX) >= 0.5:
            self.position.x += self.velX
            # if abs(self.velY) >= 0.5:
            self.position.y += self.velY
            self.accX = 0
            self.accY = 0
                
        for v in self.verticies:
            rotated = matrix.multiply(matrix.rotation(self.rotation - self.last_rotation), v.getPosition())
            v.x, v.y = rotated[0][0], rotated[1][0]
        self.last_rotation = self.rotation
        self.draw()
    def draw(self):
        draw_verticies = [pos2 for pos in self.verticies for pos2 in pos.__repr__()]   
        for i, v in enumerate(draw_verticies):
            if i % 2:
                draw_verticies[i] += self.position.y
            else:
                draw_verticies[i] += self.position.x
            draw_verticies[i] *= Vector.unit
            if i % 2:
                draw_verticies[i] += Screen.height//2
            else:
                draw_verticies[i] += Screen.width//2
        Screen.canvas.create_polygon(draw_verticies, fill = self.color)
    def collision(self, other):
        self.collided = False
        for i, v1 in enumerate(other.verticies):
            x1 = v1.x + other.position.x
            y1 = v1.y + other.position.y
            x2 = other.verticies[(i+1) % 4].x + other.position.x
            y2 = other.verticies[(i+1) % 4].y + other.position.y

            for j, v2 in enumerate(self.verticies):
                x3 = v2.x + self.position.x
                y3 = v2.y + self.position.y
                x4 = self.verticies[(j+1) % 4].x + self.position.x
                y4 = self.verticies[(j+1) % 4].y + self.position.y

                den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if (den == 0):
                    continue

                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den;
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den;
                if 1 > t > 0 and 1 > u > 0:
                    self.collided = True
                    return True

class Raycast:
    def ray(self, start_point, dir):
        dir.normalise()
        x3 = start_point.x
        y3 = start_point.y
        x4 = start_point.x + dir.x
        y4 = start_point.y + dir.y

        for other in Screen.all_entities:
            for i, v1 in enumerate(other.verticies):
                x1 = v1.x + other.position.x
                y1 = v1.y + other.position.y
                x2 = other.verticies[(i+1) % 4].x + other.position.x
                y2 = other.verticies[(i+1) % 4].y + other.position.y


                den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if (den == 0):
                    continue

                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den;
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den;
                if 1 > t > 0 and u > 0:
                    pt = Vector()
                    pt.x = x1 + t * (x2 - x1)
                    pt.y = y1 + t * (y2 - y1)
                    return pt + other.position;

g = 9.8

raycaster = Raycast()

def core_Engine_update(update):
    time1 = time()

    for entity in Screen.all_entities:
        entity.update()
    
    update()

    time2 = time()
    tick(time1, time2, 30)

    Screen.refresh()