from PIL import Image , ImageDraw

import painter as pt
import triangle as tr
from parser import getPointDraw


def get_point( index ) :
    """
    extract 3D point from vertex_list with specified index with scale and center point, recording to main image

    :param index: index of point in vertex_list, starting form 0
    :return: 3D Point from triangle module
    """
    return tr.Point( scale * vertex_list[ index , 0 ] + center ,
                     scale * vertex_list[ index , 1 ] + center ,
                     scale * vertex_list[ index , 2 ] + center )


if __name__ == '__main__' :
    im = Image.new( 'RGB' , (1000 , 1000) , color=(255 , 255 , 255 , 0) )
    draw = ImageDraw.Draw( im )
    scale = - im.width / 2 * .9
    center = im.width / 2
    vertex_list , edges_list = getPointDraw( 'african_head.obj' )

    cam_direction = tr.Point( 0 , 0 , 1 )
    light_direction = tr.Point( 0 , 0 , 1 )
    color = (255 , 255 , 255)

    for triangle in filter( lambda polygon : polygon.direction().angle( cam_direction ) > 0 ,
                            [ tr.Triangle( get_point( int( triangle.first ) - 1 ) ,
                                           get_point( int( triangle.second ) - 1 ) ,
                                           get_point( int( triangle.third ) - 1 ) ) for triangle in edges_list ] ) :
        light_angle = triangle.direction().angle( light_direction )
        pt.paint_triangle( triangle.first.projection() ,
                           triangle.second.projection() ,
                           triangle.third.projection() ,
                           draw ,
                           color=tuple( [ int( i * light_angle ) for i in list( color ) ] ) )
    im.save( 'deer.png' )
