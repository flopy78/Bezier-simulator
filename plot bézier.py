from matplotlib import pyplot as plt
from numpy import arange

def get_bezier(t,points):
    assert 0<= t <= 1
    if len(points) == 1:
        return points[0]
    else:
        new_points = []

        for i in range(len(points)-1):
            A = points[i]
            B = points[i+1]
            dx = B[0]-A[0]
            dy = B[1]-A[1]
            C = (A[0]+t*dx,A[1]+t*dy)
            new_points.append(C)
        return get_bezier(t,new_points)

def plot_bezier(control,step):

    t_list = arange(0,1+step,step)

    points = []
    for t in t_list:
        points.append(get_bezier(t,control))

    x = [p[0] for p in points]
    y = [p[1] for p in points]


    plt.plot(x,y,color = "green", label = "bézier curve")

    plt.scatter([p[0] for p in control],[p[1] for p in control], marker = "*",color = "red",label = "control points")


    plt.grid()
    
    plt.legend()

    plt.show()

plot_bezier([(1,2),(2,3),(4,6),(6,3)],0.01) # example