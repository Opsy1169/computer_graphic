from PIL import Image
from graphics import Point

import painter as pt
from parser import getPointDraw


def drawEdges( x , y , edges , im: Image , line ) :
    for i in range( len( edges ) ) :
        triangle = edges[ i ]
        scale = - im.width / 2 * .9
        center = im.width / 2
        point1 = Point( scale * x[ int( triangle.first ) - 1 ] + center , scale * y[ int( triangle.first ) - 1 ] + center )
        point2 = Point( scale * x[ int( triangle.second ) - 1 ] + center , scale * y[ int( triangle.second ) - 1 ] + center )
        point3 = Point( scale * x[ int( triangle.third ) - 1 ] + center , scale * y[ int( triangle.third ) - 1 ] + center )
        line( point1.x , point1.y , point2.x , point2.y , im )
        line( point2.x , point2.y , point3.x , point3.y , im )
        line( point3.x , point3.y , point1.x , point1.y , im )


def is_inside_triangle( point: Point , first: Point , second: Point , third: Point ) -> bool :
    # todo слайд 16 из лекция
    return False


if __name__ == '__main__' :
    im = Image.new( 'RGB' , (1000 , 1000) )
    vertexList , edgesList = getPointDraw( 'african_head.obj' )
    drawEdges( vertexList[ : , 0 ] , vertexList[ : , 1 ] , edgesList , im , pt.line_vu )
    im.save( 'african_head.png' )
