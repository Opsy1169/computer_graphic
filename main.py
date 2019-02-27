from PIL import Image

import painter as pt
import triangle as tr
from parser import getPointDraw


def get_point( index ) :
    return tr.Point( scale * vertexList[ index , 0 ] + center ,
                     scale * vertexList[ index , 1 ] + center ,
                     scale * vertexList[ index , 2 ] + center )


if __name__ == '__main__' :
    im = Image.new( 'RGB' , (1000 , 1000) )
    scale = - im.width / 2 * .9
    center = im.width / 2
    vertexList , edgesList = getPointDraw( 'deer.obj' )

    cam_direction = tr.Point( 0 , 0 , 1 )
    light_direction = tr.Point( 0 , 0 , 1 )
    color = (255 , 0 , 0)

    for triangle in filter( lambda polygon : polygon.direction().angle( cam_direction ) > 0 ,
                            [ tr.Triangle( get_point( int( triangle.first ) - 1 ) ,
                                           get_point( int( triangle.second ) - 1 ) ,
                                           get_point( int( triangle.third ) - 1 ) ) for triangle in edgesList ] ) :
        light_angle = triangle.direction().angle( light_direction )
        pt.paint_triangle( triangle.first.projection() ,
                           triangle.second.projection() ,
                           triangle.third.projection() ,
                           im ,
                           color=tuple( [ int( i * light_angle ) for i in list( color ) ] ) )
    im.save( 'deer.png' )
