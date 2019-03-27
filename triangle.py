import math
import main
import graphics
import numpy as np


class Point:
    """
    Class described 3D point or 3D vector
    """

    def __init__(self, first: float, second: float, third: float):
        self.first = first
        self.second = second
        self.third = third

    def __to_array__(self):
        return [self.first, self.second, self.third]

    def dot_product(self, another) -> float:
        return sum(i * j for i, j in zip(self.__to_array__(), another.__to_array__()))

    def norm(self) -> float:
        return math.sqrt(self.dot_product(self))


    def angle(self, another) -> float:
        """
        Calculate cos of angle with another vector
        :param another: vector to multiply
        :return: cos of angle

        """

        return self.dot_product(another) / (self.norm() * another.norm())

    def vector_product(self, another):
        cross = np.cross(self.__to_array__(), another.__to_array__())
        return Point(cross[0], cross[1], cross[2])

    def subtract(self, another):
        subtract = np.subtract(self.__to_array__(), another.__to_array__())
        return Point(subtract[0], subtract[1], subtract[2])

    def projection(self) -> graphics.Point:
        """
        Convert to 2D point, x and y axis.
        Need rotation method
        :return: 2D Point from graphics module
        """
        # todo Не стоит менять значения self, лучше просто вернуть новый измененный объект

        f_u, f_v, u_0, v_0 = main.setParametersForProjection()
        M = np.array([self.first, self.second, self.third, 1])
        K = np.zeros((3, 4))
        K[0][0] = f_u
        K[1][1] = f_v
        K[2][2] = 1
        K[0][2] = u_0
        K[1][2] = v_0
        m = K.dot(M)
        m /= m[2]
        self.first = m[0]
        self.second = m[1]

        return graphics.Point(self.first, self.second)


class Triangle:
    """
    Describes triangle polygon
    """

    def __init__(self, first: Point, second: Point, third: Point,normalFirst:Point,normalSecond:Point,normalThird:Point ,
                 textureFirst=0, textureSecond=0, textureThird=0):
        self.first = first
        self.second = second
        self.third = third

        self.normalFirst = normalFirst
        self.normalSecond = normalSecond
        self.normalThird = normalThird

        self.textureFirst = textureFirst
        self.textureSecond = textureSecond
        self.textureThird = textureThird

    def direction(self) -> Point:
        """
         Calculate by vector product vector, shows direction of polygon
        :return: 3D direction vector
        """
        first_vec = self.first.subtract(self.second)
        second_vec = self.first.subtract(self.third)
        return first_vec.vector_product(second_vec)

    def tmp_Z(self, barycentric):
        l0, l1, l2 = barycentric
        return self.first.third * l0 + self.second.third * l1 + self.third.third * l2

    @DeprecationWarning
    def bilinear_interpolation(self, point: graphics.Point) -> float:
        # Не используется вместо нее tmp_Z

        """
        Calculate z depth of 2D point projection in 3D triangle polygon. Method recording to surface
        equation http://www.mathprofi.ru/uravnenie_ploskosti.html#ou
        :param point: 2D point inside triangle projection to x-y surface, where need calculate z depth
        :return: z depth
        """
        first, second, third = self.first, self.second, self.third

        x0, y0, z0 = first.first, first.second, first.first
        x1, y1, z1 = second.first, second.second, second.first
        x2, y2, z2 = third.first, third.second, third.first
        x, y = point.x, point.y
        divider = ((x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0))
        return z0 \
               + (x - x0) * (((y2 - y0) * (z1 - z0) - (y1 - y0) * (z2 - z0)) / divider) \
               + (y - y0) * (((x1 - x0) * (z2 - z0) - (x2 - x0) * (z1 - z0)) / divider)

    def is_inside_triangle(self, point: graphics.Point) -> bool:
        """
        Checks, if triangle, specified by 3 points, contains point. Doesn't record to 3D
        :param point: gr.Point to check
        :return: True, if triangle contains point inside
        """
        l0, l1, l2 = self.getBaricenterCordinates(point)
        return l0 >= 0 and l1 >= 0 and l2 >= 0

    # Вынесли в отдельный метод, потому что для текстур нужно не только проверить условие, но и сами координаты
    def getBaricenterCordinates(self, point: graphics.Point):
        first, second, third = self.first, self.second, self.third
        l0 = ((point.y - third.second) * (second.first - third.first) - (point.x - third.first) * (
                second.second - third.second)) / \
             ((first.second - third.second) * (second.first - third.first) - (first.first - third.first) * (
                     second.second - third.second))
        l1 = ((point.y - first.second) * (third.first - first.first) - (point.x - first.first) * (
                third.second - first.second)) / \
             ((second.second - first.second) * (third.first - first.first) - (second.first - first.first) * (
                     third.second - first.second))
        l2 = ((point.y - second.second) * (first.first - second.first) - (point.x - second.first) * (
                first.second - second.second)) / \
             ((third.second - second.second) * (first.first - second.first) - (third.first - second.first) * (
                     first.second - second.second))

        return l0, l1, l2
