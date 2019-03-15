import sys
from itertools import repeat

import numpy as np
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


# завел отдельный метод, потому что чтобы унифицировать с get_point, то надо будет постоянно массив передавать, а это так себе затея
# думаю, и так нормально. Вычитать нужно, потому что он так в каком-то перевернутом виде. Установил просто эмпирически
# texture -- картинка с текстурой, сами значения в обж лежат в диапазоне от 0 до 1, так что надо умножать на размер по каждому измерению
def get_texture_point(index):
    return tr.Point(texture.size[0] * float(texture_coordinates[index].first),
                    texture.size[1] -
                    texture.size[1] * float(texture_coordinates[index].second), 0)


def new3DCoordinates(t, axis, angle):
    if (axis[0] == 1):
        alpha = np.radians(angle[0])  # угол
        R_x = np.array(np.zeros((3, 4)))  # вращение вокруг оси х
        R_x[0, 0] = 1
        R_x[1, 1] = np.cos(alpha)
        R_x[2, 2] = np.cos(alpha)
        R_x[1, 2] = (-1) * np.sin(alpha)
        R_x[2, 1] = np.sin(alpha)
        R_x[:, 3] = t

        for i in range(len(vertex_list)):
            M = np.array([vertex_list[i, 0], vertex_list[i, 1], vertex_list[i, 2], 1])
            tmp = R_x.dot(M)
            vertex_list[i, 0] = tmp[0]
            vertex_list[i, 1] = tmp[1]
            vertex_list[i, 2] = tmp[2]

    if (axis[1] == 1):  # вращение вокруг оси y
        alpha = np.radians(angle[1])
        R_y = np.array(np.zeros((3, 4)))
        R_y[0, 0] = np.cos(alpha)
        R_y[1, 1] = 1
        R_y[2, 2] = np.cos(alpha)
        R_y[0, 2] = np.sin(alpha)
        R_y[2, 0] = (-1) * np.sin(alpha)
        R_y[:, 3] = t

        for i in range(len(vertex_list)):
            M = np.array([vertex_list[i, 0], vertex_list[i, 1], vertex_list[i, 2], 1])
            tmp = R_y.dot(M)
            vertex_list[i, 0] = tmp[0]
            vertex_list[i, 1] = tmp[1]
            vertex_list[i, 2] = tmp[2]

    if (axis[2] == 1):  # вращение вокруг оси z
        alpha = np.radians(angle[2])
        R_z = np.array(np.zeros((3, 4)))
        R_z[0, 0] = np.cos(alpha)
        R_z[1, 1] = np.cos(alpha)
        R_z[2, 2] = 1
        R_z[0, 1] = (-1) * np.sin(alpha)
        R_z[1, 0] = np.sin(alpha)
        R_z[:, 3] = t

        for i in range(len(vertex_list)):
            M = np.array([vertex_list[i, 0], vertex_list[i, 1], vertex_list[i, 2], 1])
            tmp = R_z.dot(M)
            vertex_list[i, 0] = tmp[0]
            vertex_list[i, 1] = tmp[1]
            vertex_list[i, 2] = tmp[2]

    return vertex_list


def setParametrsForProjection():
    camera_offset = 10
    f_u = 1500
    f_v = 1500
    u_0 = 500
    v_0 = 500
    return camera_offset, f_u, f_v, u_0, v_0


if __name__ == '__main__':
    im = Image.new('RGB', (1000, 1000), color=(255, 255, 255, 0))
    texture = Image.open('african_head_diffuse.png')
    texture = texture.convert('RGB')
    width, height = texture.size

    draw = ImageDraw.Draw(im)
    # scale = - im.width / 2 * .9
    # center = im.width / 2
    scale = -1
    center = 0
    vertex_list, edges_list_with_text, texture_coordinates = getPointDraw('african_head.obj')
    vertex_list = new3DCoordinates(t=[0, 0, 4], axis=[0, 1, 0], angle=[0, 45, 0])

    color = (255, 255, 255)
    cam_direction = tr.Point(0, 0, 1)
    light_direction = tr.Point(0, 0, 1)
    z_buffer = np.array(list(repeat(sys.maxsize, im.width * im.height)))
    z_buffer.shape = (im.width, im.height)
    trianglesWithCoords = [tr.Triangle(get_point(int(triangle.first) - 1),
                                       get_point(int(triangle.second) - 1),
                                       get_point(int(triangle.third) - 1),
                                       get_texture_point(int(triangle.textureFirst) - 1),
                                       get_texture_point(int(triangle.textureSecond) - 1),
                                       get_texture_point(int(triangle.textureThird) - 1)) for triangle in
                           edges_list_with_text]

    for triangle in filter(lambda polygon: polygon.direction().angle(cam_direction) > 0,
                           trianglesWithCoords):
        light_angle = triangle.direction().angle(light_direction)

        # Вообще говоря, для отрисовки треугольников color больше не нужен, поскольку цвет берется из файла текстур,
        # но раз уж у нас остается функционал отрисовки линий, то передавать цвет все равно нужно
        pt.paint_triangle(triangle, draw, z_buffer, light_angle, texture,
                          color=tuple([int(i * light_angle) for i in list(color)]),
                          lines=False)

    im.save('african_head.png')
