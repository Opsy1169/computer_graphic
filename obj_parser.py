import numpy as np

import triangle as tr


def getPointDraw( filename ) :
    objFile = open( filename , 'r' )
    vertexList = [ ]
    edgesList = [ ]
    textureVertexes = [ ]
    textureСoordinates = [ ]

    for line in objFile :
        split = line.split()
        if not len( split ) :
            continue
        if split[ 0 ] == "v" :
            vertexList.append( split[ 1 : ] )
        if split[ 0 ] == "vt" :
            textureСoordinates.append( readTextureInTriangl( line ) )
        if split[ 0 ] == "f" :
            edgesList.append( readEdgesWithTextures( line ) )

    objFile.close()
    vertexList = np.array( vertexList , dtype=np.float32 )
    vertexList = np.matrix( vertexList )
    vertexList /= vertexList.max()
    return vertexList , edgesList , textureСoordinates


# Переписал метод, чтобы он одновременно считывал и вершины, и информацию про текстуры, я думаю, так удобнее,
# чтобы потом не прихоидлось между собой эти массивы соединять
# В конструкторе для треугольника заданы дефолтные значения для координат текстур, так что можно передавать
# только первые три, если нужен обычный треугольник без текстур
def readEdgesWithTextures( line ) :
    split = line.split()
    vertexes = [ ]
    textures = [ ]
    for i in range( 1 , len( split ) ) :
        indexesBySlash = split[ i ].split( '/' )
        vertexes.append( indexesBySlash[ 0 ] )
        textures.append( indexesBySlash[ 1 ] )
    triangle = tr.Triangle( vertexes[ 0 ] , vertexes[ 1 ] , vertexes[ 2 ] , textures[ 0 ] , textures[ 1 ] , textures[ 2 ] )
    return triangle


def readTexture( line ) :
    split = line.split()
    texture = [ ]
    for i in range( 1 , len( split ) ) :
        texture.append( split[ i ].split( '/' )[ 1 ] )
    triangle = tr.Triangle( texture[ 0 ] , texture[ 1 ] , texture[ 2 ] )
    return triangle


def readTextureInTriangl( line ) :
    split = line.split( ' ' )
    texture = [ ]
    for i in range( 2 , len( split ) ) :
        texture.append( split[ i ] )
    triangle = tr.Triangle( texture[ 0 ] , texture[ 1 ] , texture[ 2 ] )
    return triangle
