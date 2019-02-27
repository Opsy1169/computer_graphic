import math

import graphics
import numpy as np


class Point :
    def __init__( self , first: float , second: float , third: float ) :
        self.first = first
        self.second = second
        self.third = third

    def __to_array__( self ) :
        return [ self.first , self.second , self.third ]

    def dot_product( self , another ) -> float :
        return sum( i * j for i , j in zip( self.__to_array__() , another.__to_array__() ) )

    def norm( self ) -> float :
        return math.sqrt( self.dot_product( self ) )

    def angle( self , another ) -> float :
        return self.dot_product( another ) / (self.norm() * another.norm())

    def vector_product( self , another ) :
        cross = np.cross( self.__to_array__() , another.__to_array__() )
        return Point( cross[ 0 ] , cross[ 1 ] , cross[ 2 ] )

    def subtract( self , another ) :
        subtract = np.subtract( self.__to_array__() , another.__to_array__() )
        return Point( subtract[ 0 ] , subtract[ 1 ] , subtract[ 2 ] )

    def projection( self , cam_direction=(0 , 0 , 1) ) -> graphics.Point :
        return graphics.Point( self.first , self.second )


class Triangle :
    def __init__( self , first: Point , second: Point , third: Point ) :
        self.first = first
        self.second = second
        self.third = third

    def direction( self ) -> Point :
        first_vec = self.first.subtract( self.second )
        second_vec = self.first.subtract( self.third )
        return first_vec.vector_product( second_vec )
