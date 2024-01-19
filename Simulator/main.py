import pygame as pg
from numpy import arange

#SETUP
pg.init()
pg.font.init()

font = pg.font.Font(None,20)

screen = pg.display.set_mode((400,400))
pg.display.set_caption("Bézier curves")

done = False

plotting = False

new_points = []

control_points = []

splines = []

clock = pg.time.Clock()

fps = 60

#CLASS DEFINITIONS

class Button:
    def __init__(self,x,y,txt):
        self.text = font.render(txt,True,"black")
        w,h = font.size(txt)
        self.rect = pg.Rect(x,y,w+20,h+20)
    def draw(self):
        pg.draw.rect(screen,"grey",self.rect,border_radius = 10)
        screen.blit(self.text,(self.rect.left + 10, self.rect.top +10))
    def is_pressed(self):
        return self.rect.collidepoint(pg.mouse.get_pos())
    
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x};{self.y})"
class ControlPoint(Point):
    def __init__(self,x,y,color = "red",radius = 5):
        super().__init__(x,y)
        self.color = color
        self.drag = False
        self.rect = pg.Rect(x-radius,y-radius,2*radius,2*radius)
        self.radius = radius
    def is_pressed(self):
        return self.rect.collidepoint(pg.mouse.get_pos())
    def draw(self):
        pg.draw.circle(screen,self.color,(self.x,self.y),self.radius)
    
class Spline:
    def __init__(self,controls,color = "red",step=0.1):
        self.step = step
        self.controls = controls
        print(self.controls)
        self.color = color
    def get_point(self,t,points = None):
        assert 0<= t <= 1
        if points is None:
            points = self.controls
        print(points)
        if len(points) == 1:
            return points[0]
        else:
            new_points = []

            for i in range(len(points)-1):
                A = points[i]
                B = points[i+1]
                dx = B.x-A.x
                dy = B.y-A.y
                print("dy",dy)
                C = Point(A.x+t*dx,A.x+t*dy)
                new_points.append(C)
            return self.get_point(t,new_points)
    def draw(self):
        t_list = arange(0,1+self.step,self.step)

        points = []
        for t in t_list:
            points.append(self.get_point(t))

        for point in points:
            pg.draw.rect(screen,self.color,pg.Rect(point.x,point.y,1,1))
        exit()

        
#INSTANCIATION
button = Button(0,0,"Nouvelle courbe")


#MAIN LOOP
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
                        splines.append(Spline(new_points))
                        plotting = False
                    else:
                        new_point = ControlPoint(*pg.mouse.get_pos())
                        control_points.append(new_point)
                        new_points.append(new_point)
            else:
                if button.is_pressed():
                    plotting = True

    clock.tick(fps)
    screen.fill("white")
    for spline in splines:
        spline.draw()
    for control in control_points:
        control.draw()
    button.draw()

    pg.display.update()
    

pg.quit()