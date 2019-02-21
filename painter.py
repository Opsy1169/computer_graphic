import numpy as np
from PIL import ImageDraw


def line_brezenhem( x0 , y0 , x1 , y1 , im ) :
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
        if steeps :
            d.point( [ y , i ] , fill=(255 , 0 , 0) )
        else :
            d.point( [ i , y ] , fill=(255 , 0 , 0) )
        error += derror
        if error > 0.5 :
            y += 1 if y1 > y0 else -1
            error -= 1


def line_vu( x0 , y0 , x1 , y1 , im ) :
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
        if not steeps :
            d.point( [ i , y ] , fill=(int( 255 * (1 - error) ) , 0 , 0) )
            d.point( [ i , y + sy ] , fill=(int( 255 * error ) , 0 , 0) )
        else :
            d.point( [ y , i ] , fill=(int( 255 * (1 - error) ) , 0 , 0) )
            d.point( [ y + sy , i ] , fill=(int( 255 * error ) , 0 , 0) )
        error += derror
        if error > 1 :
            y += sy
            error -= 1
