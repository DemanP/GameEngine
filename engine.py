from tkinter import Tk, Canvas
from time import sleep, time
from keyboard import is_pressed
import pgengine.matrix as matrix
from math import hypot, radians, degrees, sqrt
from copy import copy

BLACK = '#000'
WHITE = '#fff'
GRAY = '#888'
RED = '#f00'
GREEN = '#0f0'
BLUE = '#00f'
YELLOW = '#ff0'
VIOLET = '#f0f'
LIGHTBLUE = '#0ff'

def add(a, b): return Vector(a.x + b.x, a.y + b.y)
def sub(a, b): return Vector(a.x - b.x, a.y - b.y)
def dot(a, b): return a.x * b.x + a.y * b.y
def hypot2(a, b): return dot(sub(a, b), sub(a, b))

def proj(a, b):
    k = dot(a, b) / dot(b, b)
    return Vector(k * b.x, k * b.y)

def _empty():
    pass

class Scene:
    '''
    This is scene class. It contains all information about:
    -window(window width and height, that you can change)
    -all entities on the scene
    -FPS
    -etc.
    '''
    all_entities = []

    FPS = 40

    g = 9.8

    defaultCollider = False

    width, height = 1000, 800
    def_width, def_height = width, height
    tk = Tk()
    canvas = Canvas(width = width, height = height, bg = BLACK, highlightthickness=0)
    canvas.pack()
    def background(color):
        Scene.canvas.configure(bg = color)
    def tick(time1, time2, FPS):
        sleep(time2-time1+1/FPS)
    def fullscreen(state:bool = True):
        '''
        Enter or exit fullscreen mode.

        :param state: Enter or exit fullscreen variable.
        :type state: bool
        '''
        if state:
            Scene.tk.attributes('-fullscreen', True)
            screen_width = Scene.tk.winfo_screenwidth()
            screen_height = Scene.tk.winfo_screenheight()
            Scene.setSize(screen_width, screen_height, defValue = False)
        else:
            Scene.tk.attributes('-fullscreen', False)
            Scene.setSize(Scene.def_width, Scene.def_height)
    def run(update = _empty):
        while 1:
            engine_update(update)
    def refresh():
        Scene.tk.update_idletasks()
        Scene.tk.update()
        Scene.canvas.delete('all')
    def setSize(width: int, height: int, defValue: bool = True):
        '''
        Seting a size of window to specified width and height

        :type width: int
        :type height: int
        '''
        if defValue:
            Scene.def_width, Scene.def_height = width, height
        Scene.width, Scene.height = width, height
        Scene.canvas.configure(width = width, height = height)

class InputManager:
    def keyDown(key):
        '''
        :return: is key pressed
        '''
        return is_pressed(key)
    def mousePos():
        '''
        :return: mouse position
        '''
        mouse_x = (Scene.tk.winfo_pointerx() - Scene.tk.winfo_rootx() - Scene.width//2) / Vector.unit
        mouse_y = (Scene.tk.winfo_pointery() - Scene.tk.winfo_rooty() - Scene.height//2) / Vector.unit
        return mouse_x, mouse_y

class Vector:
    unit = 50
    def normalise(self):
        '''
        This method normalising vector
        '''
        max_n = max(abs(self.x), abs(self.y))
        self.x, self.y = self.x / max_n, self.y / max_n
        return self
    def normalised(self):
        '''
        This method normalising vector
        '''
        max_n = max(abs(self.x), abs(self.y))
        return Vector(self.x / max_n, self.y / max_n)
        
    def getMatrixPosition(self):
        '''
        :return: vector position in matrix style
        '''
        return (self.x, ), (self.y, )
    def __init__(self, x  = 0, y = 0, angle = 0):
        self.x = x
        self.y = y
        self.angle = angle
    def __add__(self, other):
        if type(other) == Vector:
            x = self.x + other.x
            y = self.y + other.y
            return Vector(x, y)
    def __radd__(self, other):
        return self.__add__(other)
    def __repr__(self) -> tuple:
        return (self.x, self.y)
    def __mul__(self, other):
        if type(other) == Vector:
            x = self.x * other.x
            y = self.y * other.y
            return Vector(x, y)
        if type(other) in [int, float]:
            x = self.x * other
            y = self.y * other
            return Vector(x, y)
    def __rmul__(self, other):
        return self.__mul__(other)
    def __sub__(self, other):
        if type(other) == Vector:
            x = self.x - other.x
            y = self.y - other.y
            return Vector(x, y)
    def __rsub__(self, other):
        return self.__sub__(other)
    def __str__(self):
        return str(self.x) + ', ' + str(self.y)
class Entity:
    def __init__(self, pos = None, rot = 0, color: str = WHITE, tag = None, mass = 5, drawable = True):
        if type(pos) == tuple:
            pos = Vector(pos[0], pos[1])
        self.position = pos
        self.rotation = rot
        self.color = color
        self.last_rotation = 0

        self.drawable = drawable

        self.collider_shape = None
        self.tag = tag

        self.orientation = Vector(1, 0)
        rotated = matrix.multiply(matrix.rotation(self.rotation), self.orientation.getMatrixPosition())
        self.orientation.x, self.orientation.y = rotated[0][0], rotated[1][0]
        # self.last_rotation = self.rotation
        self.forward = self.orientation

        self.collider = Scene.defaultCollider
        self.collided = False
        self.colliding_objects = 'all'

        self.accX = 0
        self.accY = 0
        self.velX = 0
        self.velY = 0

        self.move_y = None

        self.have_gravity = False

        self.mass = mass

        Scene.all_entities.append(self)
    def update(self):
        # self.last_rotation = self.rotation
        if self.collider and self.colliding_objects == 'all':
            for _entity in Scene.all_entities:
                if _entity != self and _entity.collider and self.collision(_entity):
                    self.collided = True
                    break
                self.collided = False
        if self.have_gravity:
            if not self.collided:
                self.gravity()
        
        if self.have_gravity and not self.collided:
            gravity_casts = []
            verticies_g = []
            last_v = Vector(0, 0)
            for v in self.verticies:
                if v.y <= last_v.y and len(gravity_casts) < 3:
                    ray = raycaster.ray(v + self.position, Vector(0, -1))
                    
                    gravity_casts.append(ray)
                    verticies_g.append(v)
                    last_v = v
            rays_y = [ray.y for ray in gravity_casts if ray != None]
            if len(rays_y) and not self.collided:
                self.move_y = max(rays_y)
                index = rays_y.index(self.move_y)
                v = verticies_g[index]
                self.move_y -= v.y + 1/Vector.unit
        
        if self.collided and self.velY < 0:
            self.accY = 0
            self.velY = 0
        self.velX += self.accX
        self.velY += self.accY

        self.position.x += self.velX
        self.position.y += self.velY

        self.accX = 0
        self.accY = 0
        # if self.have_gravity:
        if self.collider and self.colliding_objects == 'all':
            for _entity in Scene.all_entities:
                if _entity != self and _entity.collider and self.collision(_entity):
                    self.collided = True
                    break
                self.collided = False

        if self.collided and self.move_y != None:
            self.position.y = self.move_y
            self.move_y = None
        
        if self.collider_shape == 'rectangle':
            for v in self.verticies:
                rotated = matrix.multiply(matrix.rotation(self.rotation - self.last_rotation), v.getMatrixPosition())
                v.x, v.y = rotated[0][0], rotated[1][0]
        rotated = matrix.multiply(matrix.rotation(self.rotation - self.last_rotation), self.orientation.getMatrixPosition())
        self.orientation.x, self.orientation.y = rotated[0][0], rotated[1][0]
        self.last_rotation = self.rotation

        self.forward = self.orientation
        
        self.draw()
    def gravity(self):
        self.force((0, -self.mass / 1000 * Scene.g))
    def force(self, pos):
        if type(pos) == tuple:
            x, y = pos
        if type(pos) == Vector:
            x, y = pos.getMatrixPosition()
        
        fX = x / Vector.unit * 10
        fY = y / Vector.unit * 10
        self.accX += fX
        self.accY += fY
    def circle_polygon_collision(circle, polygon):
        for i, v in enumerate(polygon.verticies):
            A = v
            B = copy(polygon.verticies[(i+1) % len(polygon.verticies)])

            linePt = None
        
            x1 = (A.x + polygon.position.x)
            y1 = (-A.y - polygon.position.y)
            x2 = (B.x + polygon.position.x)
            y2 = (-B.y - polygon.position.y)

            x1D = copy(-A.x + polygon.position.x)
            x2D = copy(-B.x + polygon.position.x)
            y1D = copy(-A.y + polygon.position.x)
            y2D = copy(-B.y + polygon.position.x)

            direction = (B - A)
            direction.x, direction.y = direction.y, direction.x

            x3 = circle.position.x 
            y3 = -circle.position.y
            x4 = (circle.position.x + direction.x)
            y4 = (-circle.position.y + direction.y)

            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if (den == 0):
                continue
            
            pt = Vector(x4, y4)
            Scene.canvas.create_oval(pt.x * Vector.unit - 5 + Scene.width//2, -pt.y * Vector.unit - 5 + Scene.height//2, pt.x * Vector.unit + 5 + Scene.width//2, -pt.y * Vector.unit + 5 + Scene.height//2, fill = 'yellow')

            pt = Vector(x1, y1)
            Scene.canvas.create_oval(pt.x * Vector.unit - 5 + Scene.width//2, -pt.y * Vector.unit - 5 + Scene.height//2, pt.x * Vector.unit + 5 + Scene.width//2, -pt.y * Vector.unit + 5 + Scene.height//2, fill = 'yellow')
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
            if 1 > t > 0 and 1 > u > 0:
                linePt = Vector()
                linePt.x = (x1 + t * (x2 - x1))
                linePt.y = (y1 + t * (y2 - y1))
            
            if linePt == None:
                distA = sqrt((x1 - circle.position.x) ** 2 + (y1 + circle.position.y) ** 2)
                distB = sqrt((x2 - circle.position.x) ** 2 + (y2 + circle.position.y) ** 2)
                if distA <= circle.radius or distB <= circle.radius:
                    # print(distA, distB)
                    pt = Vector(x1, y1)
                    Scene.canvas.create_oval(pt.x * Vector.unit - 5 + Scene.width//2, -pt.y * Vector.unit - 5 + Scene.height//2, pt.x * Vector.unit + 5 + Scene.width//2, -pt.y * Vector.unit + 5 + Scene.height//2, fill = 'red')
            
                    return True
                continue

            pt = copy(circle.position)
            pt.y *= -1
            Scene.canvas.create_oval(pt.x * Vector.unit - 5 + Scene.width//2, -pt.y * Vector.unit - 5 + Scene.height//2, pt.x * Vector.unit + 5 + Scene.width//2, -pt.y * Vector.unit + 5 + Scene.height//2, fill = 'yellow')
            
            pt = linePt
            Scene.canvas.create_oval(pt.x * Vector.unit - 5 + Scene.width//2, -pt.y * Vector.unit - 5 + Scene.height//2, pt.x * Vector.unit + 5 + Scene.width//2, -pt.y * Vector.unit + 5 + Scene.height//2, fill = 'yellow')
            
            if hypot(pt.x - circle.position.x, pt.y + circle.position.y) <= circle.radius:
                print(pt, circle.position, hypot(pt.x - circle.position.x, pt.y - circle.position.y))
                return True
    def collision(self, other):
        if self.collider_shape == 'rectangle':
            if other.collider_shape == 'rectangle':
                for i, v1 in enumerate(other.verticies):
                    x1 = -(v1.x + other.position.x)
                    y1 = v1.y + other.position.y
                    x2 = -(other.verticies[(i+1) % 4].x + other.position.x)
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
                            pt = Vector()
                            pt.x = x1 + t * (x2 - x1)
                            pt.y = y1 + t * (y2 - y1)
                            Scene.canvas.create_oval(pt.x * Vector.unit - 5 + Scene.width//2, -pt.y * Vector.unit - 5 + Scene.height//2, pt.x * Vector.unit + 5 + Scene.width//2, -pt.y * Vector.unit + 5 + Scene.height//2, fill = 'yellow')
                            
                            return True
            elif other.collider_shape == 'circle':
                return Entity.circle_polygon_collision(other, self)
        if self.collider_shape == 'circle':
            if other.collider_shape == 'circle':
                dist = hypot(other.position.x - self.position.x, other.position.y - self.position.y)
                if dist <= other.radius + self.radius:
                    return True
            elif other.collider_shape == 'rectangle':
                return Entity.circle_polygon_collision(self, other)
class Rectangle(Entity):
    def __init__(self, pos = copy(Vector(0, 0)), rot = 0, scale = None, color: str = WHITE, tag = None, mass = 5, drawable = True):
        super().__init__(pos, rot, color, tag, mass, drawable)
        if not scale:
            scale = Vector(1, 1)
        elif type(scale) == tuple:
            scale = Vector(scale[0], scale[1])
        self.scale = scale
        self.collider_shape = 'rectangle'

        self.verticies = [Vector(x, y) for x in [-scale.x/2, scale.x/2] for y in [-scale.y/2, scale.y/2]]
        self.verticies[2], self.verticies[3] = self.verticies[3], self.verticies[2]
    def draw(self):
        draw_verticies = [pos2 for pos in self.verticies for pos2 in pos.__repr__()]
        for i in range(len(draw_verticies)):
            if i % 2:
                draw_verticies[i] += self.position.y
            else:
                draw_verticies[i] += self.position.x
            draw_verticies[i] *= Vector.unit
            if i % 2:
                draw_verticies[i] += Scene.height//2
            else:
                draw_verticies[i] += Scene.width//2
        Scene.canvas.create_polygon(draw_verticies, fill = self.color)
class Circle(Entity):
    def __init__(self, pos = copy(Vector(0, 0)), rot = 0, radius = 10, color: str = WHITE, tag = None, mass = 5, drawable = True):
        super().__init__(pos, rot, color, tag, mass, drawable)
        self.radius = radius
        self.collider_shape = 'circle'
    def draw(self):
        Scene.canvas.create_oval((self.position.x - self.radius) * Vector.unit + Scene.width//2, (self.position.y - self.radius)  * Vector.unit + Scene.height//2, (self.position.x + self.radius) * Vector.unit + Scene.width//2, (self.position.y + self.radius) * Vector.unit + Scene.height//2, fill = self.color, outline = '')

class Raycast:
    def ray(self, start_point: Vector, dir: Vector, objects = Scene.all_entities):
        '''
        :return: ray hit point
        '''
        dir.normalise()
        x3 = start_point.x
        y3 = start_point.y
        x4 = start_point.x + dir.x
        y4 = start_point.y + dir.y

        last_pt = None

        for other in objects:
            for i, v1 in enumerate(other.verticies):
                x1 = -(v1.x + other.position.x)
                y1 = v1.y + other.position.y
                x2 = -(other.verticies[(i+1) % 4].x + other.position.x)
                y2 = other.verticies[(i+1) % 4].y + other.position.y


                den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if (den == 0):
                    continue

                t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
                u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
                if 1 > t > 0 and u > 0:
                    pt = Vector()
                    pt.x = x1 + t * (x2 - x1)
                    pt.y = y1 + t * (y2 - y1)

                    dist = hypot(pt.x - x3, pt.y - y3)
                    if not last_pt:
                        last_pt = pt
                        last_dist = dist
                    elif dist < last_dist:
                        last_dist = dist
                        last_pt = pt
        
        return last_pt

raycaster = Raycast()

def engine_update(update):
    time1 = time()

    for entity in Scene.all_entities:
        if entity.drawable:
            entity.update()
    
    # pt = raycaster.ray(Vector(0, 1), Vector(0, -1))
    # Scene.canvas.create_oval(pt.x * Vector.unit - 5 + Scene.width//2, -pt.y * Vector.unit - 5 + Scene.height//2, pt.x * Vector.unit + 5 + Scene.width//2, -pt.y * Vector.unit + 5 + Scene.height//2, fill = 'yellow')
    
    update()

    time2 = time()
    Scene.tick(time1, time2, Scene.FPS)
    
    try:
        Scene.refresh()
    except:
        exit(0)