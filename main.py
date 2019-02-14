from graphics import *


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


def lineDotByDot():
    win = GraphWin('Line', 200, 200)
    for i in range(0, 200):
        point = Point(100, i)
        point.draw(win)
    win.getMouse()
    win.close()

def embeddedLine():
    win = GraphWin('Line', 200, 200)

    rect = Rectangle(Point(0, 0), Point(199, 199))
    rect.setFill("white")
    rect.draw(win)
    line = Line(Point(10, 10), Point(190, 11))
    line.draw(win)
    win.getMouse()
    win.close()

embeddedLine()