from graphics import *
import numpy as np


def main():
    win = GraphWin('Face', 200, 150) # give title and dimensions
    #win.yUp() # make right side up coordinates!
    head = Circle(Point(40,100), 25) # set center and radius
    head.setFill("yellow")
    head.draw(win)

    eye1 = Circle(Point(30, 105), 5)
    eye1.setFill('blue')
    eye1.draw(win)

    eye2 = Line(Point(45, 105), Point(55, 105)) # set endpoints
    eye2.setWidth(3)
    eye2.draw(win)

    mouth = Oval(Point(30, 90), Point(50, 85)) # set corners of bounding box
    mouth.setFill("red")
    mouth.draw(win)

    label = Text(Point(100, 120), 'A face')
    label.draw(win)

    message = Text(Point(win.getWidth()/2, 20), 'Click anywhere to quit.')
    message.draw(win)
    win.getMouse()
    win.close()


def lineDotByDotFirst(x0, y0, x1, y1, win, color):
    step = 0.01
    arr = np.arange(0, 1, 0.01)
    for i in arr:
        point = Point((x0*(1-i) + i*x1), (y0*(1-i) + i*y1))
        point.setFill(color)
        point.draw(win)


def lineDotByDotSecond(x0, y0, x1, y1, win, color):
    step = 0.01
    arr = np.arange(x0, x1, 1)
    for i in arr:
        t = (i-x0)/(x1-x0)
        point = Point(i, (y0*(1-t) + t*y1))
        point.setFill(color)
        point.draw(win)
def swap(x,y):
    c = x
    x = y
    y = c
    return x,y

def lineDotByDotfour(x0, y0, x1, y1, win, color):
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
            point = Point(i,y)
            point.setFill(color)
            point.draw(win)
        else:
            point = Point(y, i)
            point.setFill(color)
            point.draw(win)
        error+=derror
        if (error>0.5):
            if y1>y0:
                y+=1
            else :
                y+=-1
            error -= 1

def colore(r,g,b):

    return r*0.2126+0.7152*g+b*0.0722


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
    print("derror ", derror)
    error = 0
    y=y0
    sy = 0
    if (y1>y0):
        sy=1
    else:
        sy=-1

    arr = np.arange(x0, x1, 1)
    for i in arr:
        if steeps:
            point = Point(i,y)
            point.setFill(color_rgb(int(255*(1-error)),0,0))
            print(int(255*(1-error)))
            point.draw(win)
            point = Point(i, y+sy)
            point.setFill(color_rgb(int(255*(error)),0,0))
            print(int(255 * (error)))
            point.draw(win)
        else:
            point = Point(y, i)
            point.setFill(color_rgb(int(255*(1-error)),0,0))
            print(int(255 * (1 - error)))
            point.draw(win)
            point = Point(y + sy,i)
            point.setFill(color_rgb(int(255*(error)),0,0))
            print(int(255 * (error)))
            point.draw(win)
        error+=derror
        if (error>1):

            y += sy

            error -= 1

def embeddedLine():
    win = GraphWin('Line', 200, 200)

    rect = Rectangle(Point(0, 0), Point(199, 199))
    rect.setFill("black")
    rect.draw(win)
    line = Point(4, 10.9)
    line.setFill("white")
    line.draw(win)
    line = Line(Point(9.9, 10), Point(190, 11.9))
    line.draw(win)
    win.getMouse()
    win.close()

def preparation(width):
    win = GraphWin('Line', width, width)
    win.setBackground("black")
    center = width/2
    #lineDotByDot(100, 100, 150, 150, win, "green")
    star(center, center, 13, center, win)

def star(x0, y0, rayNumber, radius, win):
    start = np.pi
    arr = np.arange(-np.pi, np.pi, 2*np.pi/rayNumber)
    print(arr)
    for i in arr:
        lineDotByDotBy(x0, y0, (radius*np.cos(i))+x0, (radius*np.sin(i))+y0, win, "white")

    win.getMouse()
    win.close()


preparation(1000)
#embeddedLine()