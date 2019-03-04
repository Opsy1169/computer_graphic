import numpy as np
from graphics import *

from obj_parser import getPointDraw


def lineDotByDotFirst(x0, y0, x1, y1, win, color):
    step = 0.01
    arr = np.arange(0, 1, 0.01)
    for i in arr:
        point = Point((x0 * (1 - i) + i * x1), (y0 * (1 - i) + i * y1))
        point.setFill(color)
        point.draw(win)



def lineDotByDotSecond(x0, y0, x1, y1, win, color):
    step = 0.01
    arr = np.arange(x0, x1, 1)
    for i in arr:
        t = (i - x0) / (x1 - x0)
        point = Point(i, (y0 * (1 - t) + t * y1))
        point.setFill(color)
        point.draw(win)


def swap(x, y):
    c = x
    x = y
    y = c
    return x, y


def lineDotByDotfour(x0, y0, x1, y1, win, color):
    steeps = False
    if np.abs(x0 - x1) < np.abs(y0 - y1):
        x0, y0 = swap(x0, y0)
        x1, y1 = swap(x1, y1)
        steeps = True
    if (x0 > x1):
        x0, x1 = swap(x0, x1)
        y0, y1 = swap(y0, y1)

    dx = x1 - x0
    dy = y1 - y0
    derror = np.abs(dy / dx)
    error = 0
    y = y0
    arr = np.arange(x0, x1, 1)
    for i in arr:
        if steeps:
            point = Point(y, i)
            point.setFill(color)
            point.draw(win)
        else:
            point = Point(i, y)
            point.setFill(color)
            point.draw(win)
        error += derror
        if (error > 0.5):
            if y1 > y0:
                y += 1
            else:
                y += -1
            error -= 1


def colore(r, g, b):
    return r * 0.2126 + 0.7152 * g + b * 0.0722


def lineDotByDotBy(x0, y0, x1, y1, win, color):
    steeps = False
    if np.abs(x0 - x1) < np.abs(y0 - y1):
        x0, y0 = swap(x0, y0)
        x1, y1 = swap(x1, y1)
        steeps = True
    if (x0 > x1):
        x0, x1 = swap(x0, x1)
        y0, y1 = swap(y0, y1)

    dx = x1 - x0
    dy = y1 - y0
    derror = np.abs(dy / dx)
    error = 0
    y = y0
    sy = 0
    if (y1 > y0):
        sy = 1
    else:
        sy = -1

    arr = np.arange(x0, x1, 1)
    for i in arr:
        if not steeps:
            point = Point(i, y)
            point.setFill(color_rgb(int(255 * (1 - error)), 0, 0))
            point.draw(win)
            point = Point(i, y + sy)
            point.setFill(color_rgb(int(255 * (error)), 0, 0))
            point.draw(win)
        else:
            point = Point(y, i)
            point.setFill(color_rgb(int(255 * (1 - error)), 0, 0))
            point.draw(win)
            point = Point(y + sy, i)
            point.setFill(color_rgb(int(255 * (error)), 0, 0))
            point.draw(win)
        error += derror
        if (error > 1):
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
    center = width / 2
    # lineDotByDot(100, 100, 150, 150, win, "green")
    star(center, center, 13, center, win)


def star(x0, y0, rayNumber, radius, win):
    start = np.pi
    arr = np.arange(-np.pi, np.pi, 2 * np.pi / rayNumber)
    print(arr)
    for i in arr:
        lineDotByDotBy(x0, y0, (radius * np.cos(i)) + x0, (radius * np.sin(i)) + y0, win, "white")

    win.getMouse()
    win.close()


# preparation(1000)
# embeddedLine()


def drawPoint(x, y, win, color):
    width = win.width
    center = width / 2
    for i in range(len(x)):
        point = Point(300 * x[i] + center, -300 * y[i] + center)
        point.setFill(color)
        point.draw(win)


def drawEdges(x, y, edges, win, color):
    for i in range(len(edges)):
        triangle = edges[i]
        width = win.width
        center = width / 2
        point1 = Point(-310 * x[int(triangle.first) - 1] + center, -310 * y[int(triangle.first) - 1] + center)
        point2 = Point(-310 * x[int(triangle.second) - 1] + center, -310 * y[int(triangle.second) - 1] + center)
        point3 = Point(-310 * x[int(triangle.third) - 1] + center, -310 * y[int(triangle.third) - 1] + center)
        lineDotByDotfour(point1.x, point1.y, point2.x, point2.y, win, color)
        lineDotByDotfour(point2.x, point2.y, point3.x, point3.y, win, color)
        lineDotByDotfour(point3.x, point3.y, point1.x, point1.y, win, color)


if __name__ == '__main__':
    win = GraphWin('Line', 1000, 1000)
    win.setBackground("black")
    x, y, edges = getPointDraw('x', 'y')
    drawEdges(x, y, edges, win, "green")
    # drawPoint(x, y, win, "green")
    win.getMouse()
    win.close()
