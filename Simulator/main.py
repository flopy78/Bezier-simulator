import pygame as pg
from numpy import arange

#SETUP
pg.init()
pg.font.init()

font = pg.font.Font(None,size = 20)

screen = pg.display.set_mode((400,400))
pg.display.set_caption("Bézier curves")

done = False

plotting = False

new_points = []

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

class ControlPoint(Point):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.drag = False
    
class Spline:
    def __init__(self,controls,color = "red",step=0.01):
        self.step = step
        self.controls = controls
        self.color = color
    def get_point(self,t,points = None):
        assert 0<= t <= 1
        if points is None:
            points = self.controls
        if len(points) == 1:
            return points.x
        else:
            new_points = []

            for i in range(len(points)-1):
                A = points[i]
                B = points[i+1]
                dx = B.x-A.x
                dy = B.y-A.y
                C = Point(A.x+t*dx,A.x+t*dy)
                new_points.append(C)
            return self.get_point(t,new_points)
    def plot(self):
        t_list = arange(0,1+self.step,self.step)

        points = []
        for t in t_list:
            points.append(self.get_point(t))

        for point in points:
            pg.draw.rect(screen,self.color,pg.Rect(point.x,point.y,1,1))

        
#INSTANCIATION
button = Button(0,0,"Nouvelle courbe")


#MAIN LOOP
while not done:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                done = True
                break
            case pg.MOUSEBUTTONDOWN:
                    if button.is_pressed():
                        plotting = True
    clock.tick(fps)
    screen.fill("white")

    button.draw()

    pg.display.update()
    

pg.quit()