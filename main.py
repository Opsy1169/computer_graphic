import sys
from itertools import repeat

import numpy as np
import random
from PIL import Image, ImageDraw

import painter as pt
import triangle as tr
from obj_parser import getPointDraw


def get_point(index):
    """
    extract 3D point from vertex_list with specified index with scale and center point, recording to main image

    :param index: index of point in vertex_list, starting form 0
    :return: 3D Point from triangle module
    """
    return tr.Point(scale * vertex_list[index, 0] + center,
                    scale * vertex_list[index, 1] + center,
                    scale * vertex_list[index, 2] + center)

#завел отдельный метод, потому что чтобы унифицировать с get_point, то надо будет постоянно массив передавать, а это так себе затея
#думаю, и так нормально. Вычитать нужно, потому что он так в каком-то перевернутом виде. Установил просто эмпирически
#texture -- картинка с текстурой, сами значения в обж лежат в диапазоне от 0 до 1, так что надо умножать на размер по каждому измерению
def get_texture_point(index):
    return tr.Point(texture.size[0]*float(texture_coordinates[index].first), texture.size[1] -
                    texture.size[1]*float(texture_coordinates[index].second), 0)


if __name__ == '__main__':
    im = Image.new('RGB', (1000, 1000), color=(255, 255, 255, 0))
    texture = Image.open('african_head_diffuse.png')
    texture = texture.convert('RGB')
    width, height = texture.size

    draw = ImageDraw.Draw(im)
    scale = - im.width / 2 * .9
    center = im.width / 2
    vertex_list, edges_list_with_text, texture_coordinates = getPointDraw('african_head.obj')
    color = (255, 255, 255)
    cam_direction = tr.Point(0, 0, 1)
    light_direction = tr.Point(0, 0, 1)
    z_buffer = np.array(list(repeat(sys.maxsize, im.width * im.height)))
    z_buffer.shape = (im.width, im.height)
    trianglesWithCoords = [tr.Triangle(get_point(int(triangle.first) - 1),
                                        get_point(int(triangle.second) - 1),
                                        get_point(int(triangle.third) - 1),
                                       get_texture_point(int(triangle.textureFirst) - 1),
                                       get_texture_point(int(triangle.textureSecond)-1),
                                       get_texture_point(int(triangle.textureThird)-1)) for triangle in edges_list_with_text]


    for triangle in filter(lambda polygon: polygon.direction().angle(cam_direction) > 0,
                           trianglesWithCoords):
        light_angle = triangle.direction().angle(light_direction)

        #Вообще говоря, для отрисовки треугольников color больше не нужен, поскольку цвет берется из файла текстур,
        #но раз уж у нас остается функционал отрисовки линий, то передавать цвет все равно нужно
        pt.paint_triangle(triangle, draw, z_buffer, light_angle, texture, color=tuple([int(i * light_angle) for i in list(color)]),
                          lines=False)

    im.save('african_head.png')


