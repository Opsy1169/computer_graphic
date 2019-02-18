from graphics import *
import numpy as np
from parser_my import getPointDraw

from PIL import Image, ImageDraw



def swap(x,y):
    c = x
    x = y
    y = c
    return x,y

def lineDotByDotfour(x0, y0, x1, y1, win, color,im):
    xy = []
    xy.append(x0)
    xy.append(y0)

    steeps = False
    if np.abs(x0 - x1)<np.abs(y0-y1):
        x0,y0 = swap(x0,y0)
        x1,y1 = swap(x1,y1)
        steeps=True
    if (x0>x1):
        x0, x1 = swap(x0, x1)
        y0, y1 = swap(y0, y1)

    dx = x1-x0
    dy = y1-y0
    derror = np.abs(dy/dx)
    error = 0
    y=y0
    arr = np.arange(x0, x1, 1)
    for i in arr:
        if steeps:
            d = ImageDraw.Draw(im)
            d.point([y,i])

        else:
            d = ImageDraw.Draw(im)
            d.point([i, y])
        error+=derror
        if (error>0.5):
            if y1>y0:
                y+=1
            else :
                y+=-1
            error -= 1


def lineDotByDotBy(x0, y0, x1, y1, win, color):
    steeps = False
    if np.abs(x0 - x1)<np.abs(y0-y1):
        x0,y0 = swap(x0,y0)
        x1,y1 = swap(x1,y1)
        steeps=True
    if (x0>x1):
        x0, x1 = swap(x0, x1)
        y0, y1 = swap(y0, y1)

    dx = x1-x0
    dy = y1-y0
    derror = np.abs(dy/dx)
    error = 0
    y=y0
    sy = 0
    if (y1>y0):
        sy=1
    else:
        sy=-1

    arr = np.arange(x0, x1, 1)
    for i in arr:
        if not steeps:
            d = ImageDraw.Draw(im)
            d.point([i, y],fill=((int(255*(1-error)),0,0)))
            d = ImageDraw.Draw(im)
            d.point([i, y+sy], fill=((int(255 * (error)), 0, 0)))

        else:
            d = ImageDraw.Draw(im)
            d.point([y,i], fill=((int(255 * (1 - error)), 0, 0)))
            d = ImageDraw.Draw(im)
            d.point([y + sy,i], fill=((int(255 * (error)), 0, 0)))
        error+=derror
        if (error>1):

            y += sy

            error -= 1

def drawEdges(x, y, edges, win, color,im):

    for i in range(len(edges)):
        triangle = edges[i]
        width = win.width
        center = width/2
        point1 = Point(-310*x[int(triangle.first)-1]+center, -310*y[int(triangle.first)-1]+center)
        point2 = Point(-310*x[int(triangle.second) - 1]+center, -310*y[int(triangle.second) - 1]+center)
        point3 = Point(-310*x[int(triangle.third) - 1]+center, -310*y[int(triangle.third) - 1]+center)
        lineDotByDotBy(point1.x, point1.y, point2.x, point2.y, win, color)
        lineDotByDotBy(point2.x, point2.y, point3.x, point3.y, win, color)
        lineDotByDotBy(point3.x, point3.y, point1.x, point1.y, win, color)
    im.save('res.png')


if __name__ == '__main__':

    win = GraphWin('Line', 1000, 1000)
    win.setBackground("black")

    im = Image.new('RGB',(1000,1000),'black')

    im.save('test.png')

    x, y, edges = getPointDraw('x', 'y')
    drawEdges(x, y, edges, win, "green",im)
    # drawPoint(x, y, win, "green")
