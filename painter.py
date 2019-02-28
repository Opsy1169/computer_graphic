import numpy as np
from PIL import ImageDraw
from graphics import Point


def line_brezenhem( start: Point , end: Point , draw: ImageDraw , color=(255 , 0 , 0) ) :
    """
     Draws line from start to end 2D Point via Brezenhem algorithm ( without gradient subline )

    :param start: starting line 2D point
    :param end: ending line 2D point
    :param draw: drawing tool from Pillow module
    :param color: base painting color ( optional, red is default)
    """

    # decompose point
    x0 , y0 = (start.x , start.y)
    x1 , y1 = (end.x , end.y)

    # reverse coordinates if y axis part of line longer thar x axis
    steeps = np.abs( x0 - x1 ) < np.abs( y0 - y1 )
    if steeps :
        x0 , y0 = (y0 , x0)
        x1 , y1 = (y1 , x1)

    if x0 > x1 :
        x0 , x1 = (x1 , x0)
        y0 , y1 = (y1 , y0)
    dx = x1 - x0
    dy = y1 - y0
    derror = np.abs( dy / dx )
    error = 0
    y = y0
    for i in np.arange( x0 , x1 , 1 ) :
        # Draw base line
        draw.point( [ i , y ] if not steeps else [ y , i ] , fill=color )
        error += derror
        if error > 0.5 :
            y += 1 if y1 > y0 else -1
            error -= 1


def line_vu( start: Point , end: Point , draw: ImageDraw , color=(255 , 0 , 0) ) :
    """
         Draws line from start to end 2D Point via Vu algorithm ( with gradient subline )

        :param start: starting line 2D point
        :param end: ending line 2D point
        :param draw: drawing tool from Pillow module
        :param color: base painting color ( optional, red is default )
        """
    # decompose point
    x0 , y0 = (start.x , start.y)
    x1 , y1 = (end.x , end.y)

    # reverse coordinates if y axis part of line longer thar x axis
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

    for i in np.arange( x0 , x1 , 1 ) :

        base_color = tuple( [ int( i * (1 - error) ) for i in list( color ) ] )
        add_color = tuple( [ int( i * error ) for i in list( color ) ] )
        # Draw base line with subline
        draw.point( [ i , y ] if not steeps else [ y , i ] , fill=base_color )
        draw.point( [ i , y + sy ] if not steeps else [ y + sy , i ] , fill=add_color )

        error += derror
        if error > 1 :
            y += sy
            error -= 1


def is_inside_triangle( point: Point , first: Point , second: Point , third: Point ) -> bool :
    """
    Checks, if triangle, specified by 3 points, contains point. Doesn't record to 3D

    :param point: point to check
    :param first, second, third: points to specify 2D triangle
    :return: True, if triangle contains point inside
    """
    l0 = ((point.y - third.y) * (second.x - third.x) - (point.x - third.x) * (second.y - third.y)) / \
         ((first.y - third.y) * (second.x - third.x) - (first.x - third.x) * (second.y - third.y))
    l1 = ((point.y - first.y) * (third.x - first.x) - (point.x - first.x) * (third.y - first.y)) / \
         ((second.y - first.y) * (third.x - first.x) - (second.x - first.x) * (third.y - first.y))
    l2 = ((point.y - second.y) * (first.x - second.x) - (point.x - second.x) * (first.y - second.y)) / \
         ((third.y - second.y) * (first.x - second.x) - (third.x - second.x) * (first.y - second.y))
    return l0 >= 0 and l1 >= 0 and l2 >= 0


def colorize( first: Point , second: Point , third: Point , draw: ImageDraw , color=(255 , 0 , 0) ) :
    """
    Colorize inner part of triangle with specified color

    :param first, second, third: points to specify 2D triangle
    :param draw: drawing tool from Pillow module
    :param color: base painting color ( optional, red is default )
    """
    for i in np.arange( min( first.x , second.x , third.x ) , max( first.x , second.x , third.x ) + 1 , 1 ) :
        for j in np.arange( min( first.y , second.y , third.y ) , max( first.y , second.y , third.y ) + 1 , 1 ) :
            if is_inside_triangle( Point( i , j ) , first , second , third ) :
                draw.point( [ i , j ] , fill=color )


def paint_triangle( first: Point , second: Point , third: Point , draw: ImageDraw , color=(255 , 0 , 0) , line_func=line_brezenhem ) :
    """

    :param first, second, third: points to specify 2D triangle
    :param draw: drawing tool from Pillow module
    :param color: base painting color ( optional, red is default )
    :param line_func: line drawing func
    """
    line_func( first , second , draw , color )
    line_func( second , third , draw , color )
    line_func( third , first , draw , color )
    colorize( first , second , third , draw , color )
