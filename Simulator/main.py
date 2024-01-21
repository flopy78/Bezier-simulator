import pygame as pg
from numpy import arange
from copy import deepcopy

# SETUP
pg.init()
pg.font.init()

font = pg.font.Font(None, 20)

screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Courbes de Bézier")

colors = ["red", "blue", "green", "purple", "pink", "orange", "brown"]

done = False

plotting = False

new_points = []

control_points = []

splines = []

clock = pg.time.Clock()

fps = 60

# CLASS DEFINITIONS

class Button:
    def __init__(self, x, y, txtoff, txton):
        self.textoff = font.render(txtoff, True, "black")
        self.texton = font.render(txton, True, "black")
        w, h = font.size(txtoff)
        self.rectoff = pg.Rect(x, y, w + 20, h + 20)
        w, h = font.size(txton)
        self.recton = pg.Rect(x, y, w + 20, h + 20)
        self.on = False
    def draw(self):

        if self.on:
            pg.draw.rect(screen, "red", self.recton, border_radius = 10)
            screen.blit(self.texton, (self.recton.left + 10,  self.recton.top + 10))

        else:
            pg.draw.rect(screen, "grey", self.rectoff, border_radius = 10)
            screen.blit(self.textoff, (self.rectoff.left + 10,  self.rectoff.top + 10))

    def is_pressed(self):
        if self.on: return self.recton.collidepoint(pg.mouse.get_pos())
        else: return self.rectoff.collidepoint(pg.mouse.get_pos())   


    
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x};{self.y})"
    
class ControlPoint(Point):
    def __init__(self, x, y, color = "red", radius = 5):
        super().__init__(x, y)
        self.splines = []
        self.color = color
        self.drag = False
        self.select = False
        self.rect = pg.Rect(x - radius, y - radius, 2 * radius, 2 * radius)
        self.radius = radius

    def is_pressed(self):
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def draw(self):
        if self.drag:
            self.x, self.y = pg.mouse.get_pos()
            self.rect.center = (self.x, self.y)
        w = 0
        if self.select: w = 1
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius, width=w)

    def remove(self):
        for spline in self.splines:
            spline.controls.remove(self)
        control_points.remove(self)

        del self

class Spline:
    def __init__(self, controls, color = "red", step = 0.001):
        self.step = step
        self.controls = controls
        self.color = color

        for control in self.controls:
            control.splines.append(self)
            
    def get_point(self, t, points = None):
        assert 0 <= t <= 1
        if points is None:
            points = self.controls
        if len(points) == 1:
            return points[0]
        else:
            new_points = []

            for i in range(len(points) - 1):
                A = points[i]
                B = points[i + 1]
                dx = B.x - A.x
                dy = B.y - A.y
                C = Point(A.x + t * dx, A.y + t * dy)
                new_points.append(C)
            return self.get_point(t, new_points)
        
    def draw(self):
        if len(self.controls) == 0:
            splines.remove(self)
            colors.insert(0, self.color)
            del self
            return
        for i in range(len(self.controls)-1):
            A = self.controls[i]
            B = self.controls[i + 1]
            for point in [self.get_point(t, [A, B]) for t in arange(0, 1 + self.step, self.step)]:
                pg.draw.rect(screen, "grey", pg.Rect(point.x, point.y, 1, 1))
        points = [self.get_point(t) for t in arange(0, 1 + self.step, self.step)]

        for point in points:
            pg.draw.rect(screen, self.color, pg.Rect(point.x, point.y, 1, 1))

        
# INSTANCIATION
button = Button(0, 0, "Nouvelle courbe", "Valider le tracé")


# MAIN LOOP
while not done:
    for event in pg.event.get():
        tp = event.type
        if tp == pg.QUIT:
            done = True
            break
        elif tp == pg.MOUSEBUTTONDOWN:
            if  plotting:
                for control in control_points:
                    if control.is_pressed():
                        new_points.append(control)
                        break
                else:
                    if button.is_pressed():
                        button.on = False
                        splines.append(Spline(new_points, colors[0]))
                        plotting = False
                        colors = colors[1:]
                        new_points = []
                    else:
                        new_point = ControlPoint(*pg.mouse.get_pos(), colors[0])
                        control_points.append(new_point)
                        new_points.append(new_point)
            else:
                if button.is_pressed():
                    plotting = True
                    button.on = True
                else:
                    for control in control_points:
                        if control.is_pressed():
                            control.drag = True
                            control.select = True
                            for c in control_points:
                                if c != control:
                                    c.select = False
                            break
                    else:
                        for control in control_points:
                            control.select = False
        elif tp == pg.MOUSEBUTTONUP:
                for control in control_points:
                    control.drag = False
        elif tp == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                for control in control_points:
                    if control.select:
                        control.remove()
                        break
    
                    

    clock.tick(fps)
    screen.fill("white")
    for spline in splines:
        spline.draw()
    for control in control_points:
        control.draw()
    button.draw()

    pg.display.update()
    

pg.quit()