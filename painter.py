import numpy as np
from PIL import ImageDraw , Image
from graphics import Point


def line_brezenhem( start: Point , end: Point , im , color=(255 , 0 , 0) ) :
    x0 , y0 = (start.x , start.y)
    x1 , y1 = (end.x , end.y)

    steeps = False
    if np.abs( x0 - x1 ) < np.abs( y0 - y1 ) :
        x0 , y0 = (y0 , x0)
        x1 , y1 = (y1 , x1)
        steeps = True
    if x0 > x1 :
        x0 , x1 = (x1 , x0)
        y0 , y1 = (y1 , y0)
    dx = x1 - x0
    dy = y1 - y0
    derror = np.abs( dy / dx )
    error = 0
    y = y0
    d = ImageDraw.Draw( im )
    for i in np.arange( x0 , x1 , 1 ) :
        d.point( [ i , y ] if not steeps else [ y , i ] , fill=color )
        error += derror
        if error > 0.5 :
            y += 1 if y1 > y0 else -1
            error -= 1


def line_vu( start: Point , end: Point , im , color=(255 , 0 , 0) ) :
    x0 , y0 = (start.x , start.y)
    x1 , y1 = (end.x , end.y)

    steeps = np.abs( x0 - x1 ) < np.abs( y0 - y1 )
    if steeps :
        x0 , y0 = (y0 , x0)
        x1 , y1 = (y1 , x1)

    dx = x1 - x0
    dy = y1 - y0
    if dx < 0 :
        x0 , x1 = (x1 , x0)
        y0 , y1 = (y1 , y0)

    derror = np.abs( dy / dx )
    error = 0
    y = y0
    sy = 1 if y1 > y0 else -1

    d = ImageDraw.Draw( im )
    for i in np.arange( x0 , x1 , 1 ) :

        base_color = tuple( [ int( i * (1 - error) ) for i in list( color ) ] )
        add_color = tuple( [ int( i * error ) for i in list( color ) ] )

        d.point( [ i , y ] if not steeps else [ y , i ] , fill=base_color )
        d.point( [ i , y + sy ] if not steeps else [ y + sy , i ] , fill=add_color )

        error += derror
        if error > 1 :
            y += sy
            error -= 1


def is_inside_triangle( point: Point , first: Point , second: Point , third: Point ) -> bool :
    l0 = ((point.y - third.y) * (second.x - third.x) - (point.x - third.x) * (second.y - third.y)) / \
         ((first.y - third.y) * (second.x - third.x) - (first.x - third.x) * (second.y - third.y))
    l1 = ((point.y - first.y) * (third.x - first.x) - (point.x - first.x) * (third.y - first.y)) / \
         ((second.y - first.y) * (third.x - first.x) - (second.x - first.x) * (third.y - first.y))
    l2 = ((point.y - second.y) * (first.x - second.x) - (point.x - second.x) * (first.y - second.y)) / \
         ((third.y - second.y) * (first.x - second.x) - (third.x - second.x) * (first.y - second.y))
    return l0 >= 0 and l1 >= 0 and l2 >= 0


def colorize( first: Point , second: Point , third: Point , im: Image , color=(255 , 0 , 0) ) :
    d = ImageDraw.Draw( im )
    for i in np.arange( min( first.x , second.x , third.x ) , max( first.x , second.x , third.x ) + 1 , 1 ) :
        for j in np.arange( min( first.y , second.y , third.y ) , max( first.y , second.y , third.y ) + 1 , 1 ) :
            if is_inside_triangle( Point( i , j ) , first , second , third ) :
                d.point( [ i , j ] , fill=color )


def paint_triangle( point1: Point , point2: Point , point3: Point , image: Image , color=(255 , 0 , 0) , line_func=line_brezenhem ) :
    line_func( point1 , point2 , image , color )
    line_func( point2 , point3 , image , color )
    line_func( point3 , point1 , image , color )
    colorize( point1 , point2 , point3 , image , color )
