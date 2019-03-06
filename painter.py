import graphics as gr
import numpy as np
from PIL import Image , ImageDraw

import triangle as tr


def line_brezenhem( start: gr.Point , end: gr.Point , draw: ImageDraw , color=(255 , 0 , 0) ) :
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
        x0 , y0 = y0 , x0
        x1 , y1 = y1 , x1

    if x0 > x1 :
        x0 , x1 = x1 , x0
        y0 , y1 = y1 , y0
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


def line_vu( start: gr.Point , end: gr.Point , draw: ImageDraw , color=(255 , 0 , 0) ) :
    """
         Draws line from start to end 2D Point via Vu algorithm ( with gradient subline )

        :param start: starting line 2D point
        :param end: ending line 2D point
        :param draw: drawing tool from Pillow module
        :param color: base painting color ( optional, red is default )
        """
    # decompose point
    x0 , y0 = start.x , start.y
    x1 , y1 = end.x , end.y

    # reverse coordinates if y axis part of line longer thar x axis
    steeps = np.abs( x0 - x1 ) < np.abs( y0 - y1 )
    if steeps :
        x0 , y0 = y0 , x0
        x1 , y1 = y1 , x1

    dx = x1 - x0
    dy = y1 - y0
    if dx < 0 :
        x0 , x1 = x1 , x0
        y0 , y1 = y1 , y0

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


def draw_pixel( point: tr.Point , z_buffer , draw: ImageDraw , color=(255 , 0 , 0) ) :
    """
    Draws pixel, if it's z depth is lower then previous points
    """
    if point.third < z_buffer[ point.first , point.second ] :
        draw.point( [ point.first , point.second ] , fill=color )
        z_buffer[ point.first , point.second ] = point.third


def colorize( polygon: tr.Triangle , draw: ImageDraw , light_angle , texture: Image , z_buffer , color=(255 , 0 , 0) ) :
    """
    Colorize inner part of triangle with specified color
    """
    first , second , third = polygon.first , polygon.second , polygon.third
    x0 = int( min( first.first , second.first , third.first ) )
    x1 = int( max( first.first , second.first , third.first ) )
    y0 = int( min( first.second , second.second , third.second ) )
    y1 = int( max( first.second , second.second , third.second ) )
    for x in range( x0 , x1 + 1 ) :
        for y in range( y0 , y1 + 1 ) :
            l0 , l1 , l2 = polygon.getBaricenterCordinates( (gr.Point( x , y )) )
            is_inside_triangle = l0 >= 0 and l1 >= 0 and l2 >= 0
            if is_inside_triangle :
                # получаем координаты пикселя, соответствующего отрисовываемому в данный момент, из файла текстур
                coord1 = int( polygon.textureFirst.first * l0 + polygon.textureSecond.first * l1 + polygon.textureThird.first * l2 )
                coord2 = int( polygon.textureFirst.second * l0 + polygon.textureSecond.second * l1 + polygon.textureThird.second * l2 )
                # получаем цвет пикселя из файла текстур по вычисленным координатам
                (r , g , b) = texture.getpixel( (coord1 , coord2) )
                z = polygon.bilinear_interpolation( gr.Point( x , y ) )
                draw_pixel( tr.Point( x , y , z ) , z_buffer , draw , tuple( int( color * light_angle ) for color in (r , g , b) ) )


def paint_triangle( polygon: tr.Triangle , draw: ImageDraw , z_buffer , light_angle , texture , color=(255 , 0 , 0) ,
                    line_func=line_brezenhem , lines=True , fill=True ) :
    if lines :
        line_func( polygon.first.projection() , polygon.second.projection() , draw , color )
        line_func( polygon.second.projection() , polygon.third.projection() , draw , color )
        line_func( polygon.third.projection() , polygon.first.projection() , draw , color )
    if fill :
        colorize( polygon , draw , light_angle , texture , z_buffer , color )
