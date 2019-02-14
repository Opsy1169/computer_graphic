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


def lineDotByDot(x0, y0, x1, y1, win, color):
    step = 0.01
    arr = np.arange(0, 1, 0.1)
    for i in arr:
        point = Point((x0*(1-i) + i*x1), (x0*(1-i) + i*y1));
        point.draw(win)
    win.getMouse()
    win.close()

def embeddedLine():
    win = GraphWin('Line', 200, 200)

    rect = Rectangle(Point(0, 0), Point(199, 199))
    rect.setFill("white")
    rect.draw(win)
    line = Point(4, 10.9)
    line.setFill("red")
    line.draw(win)
    line = Line(Point(9.9, 10), Point(190, 11.9))
    line.draw(win)
    win.getMouse()
    win.close()

def preparation():
    win = GraphWin('Line', 200, 200)
    win.setBackground("white")
    lineDotByDot(100, 100, 150, 150, win, "green")

preparation()
#embeddedLine()