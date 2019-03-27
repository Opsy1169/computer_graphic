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
    P.S. use negative values because object is rotated upside-down
    :param index: index of point in vertex_list, starting form 0
    :return: 3D Point from triangle module
    """
    return tr.Point(-vertex_list[index, 0],-vertex_list[index, 1], -vertex_list[index, 2])


def get_normal_point(index):
    return tr.Point(-vectorNormal[index, 0], -vectorNormal[index, 1], -vectorNormal[index, 2])
# завел отдельный метод, потому что чтобы унифицировать с get_point, то надо будет постоянно массив передавать,
# а это так себе затея думаю, и так нормально. Вычитать нужно, потому что он так в каком-то перевернутом виде.
# Установил просто эмпирически texture -- картинка с текстурой, сами значения в обж лежат в диапазоне от 0 до 1,
# так что надо умножать на размер по каждому измерению
def get_texture_point(index):
    return tr.Point(texture.size[0] * float(texture_coordinates[index].first),
                    texture.size[1] -
                    texture.size[1] * float(texture_coordinates[index].second), 0)


# todo надо объеденить все преобразования в одно
def rotate_object(vertex_list, rotation_angle, cam_position):
    """
    Rotate vertexes on specific angel on each axis
    :param vertex_list: list of model's vertexes
    :param rotation_angle: tuple, contains rotation angles on x,y and z axis
    :return: rotated vertexes list
    """
    R = create_rotation_matrix(rotation_angle, cam_position)
    # mutate vertexes
    for i in range(len(vertex_list)):
        M = np.concatenate((np.array(vertex_list[i, :]).reshape(3, 1), np.array(1).reshape(1, 1)))
        vertex_list[i, :] = np.matmul(R, M).reshape(1, 3)
        vertex_list[i,2] = vertex_list[i,2]
    return vertex_list


def create_rotation_matrix(rotation_angle, cam_position):
    # create x rotation matrix
    alpha = np.radians(rotation_angle[0])
    R_x = np.zeros((3, 3))
    R_x[0, 0] = 1
    R_x[1, 1] = np.cos(alpha)
    R_x[2, 2] = np.cos(alpha)
    R_x[1, 2] = -np.sin(alpha)
    R_x[2, 1] = np.sin(alpha)
    # create y rotation matrix
    alpha = np.radians(rotation_angle[1])
    R_y = np.zeros((3, 3))
    R_y[0, 0] = np.cos(alpha)
    R_y[1, 1] = 1
    R_y[2, 2] = np.cos(alpha)
    R_y[0, 2] = np.sin(alpha)
    R_y[2, 0] = -np.sin(alpha)
    # create z rotation matrix
    alpha = np.radians(rotation_angle[2])
    R_z = np.zeros((3, 3))
    R_z[0, 0] = np.cos(alpha)
    R_z[1, 1] = np.cos(alpha)
    R_z[2, 2] = 1
    R_z[0, 1] = -np.sin(alpha)
    R_z[1, 0] = np.sin(alpha)
    additional = np.array(cam_position)
    additional.shape = (3, 1)
    # combine all rotations in one
    return np.column_stack((np.matmul(np.matmul(R_x, R_y), R_z), additional))


def setParametersForProjection():
    f_u = 1500
    f_v = 1500
    u_0 = 500
    v_0 = 500
    return  f_u, f_v, u_0, v_0

def newVectorNormal():
    vectorNormal[:,0]=vectorNormal[:,0]*0
    vectorNormal[:,1]=vectorNormal[:,1]*0
    vectorNormal[:,2]=vectorNormal[:,2]*1
    return vectorNormal

if __name__ == '__main__':
    im = Image.new('RGB', (1000, 1000), color=(255, 255, 255, 0))
    texture = Image.open('african_head_diffuse.png')
    texture = texture.convert('RGB')
    width, height = texture.size

    draw = ImageDraw.Draw(im)
    cam_position = (0, 0, -5)
    cam_direction = tr.Point(0, 0, 1)

    z_buffer = np.array(list(repeat(float(sys.maxsize), im.width * im.height)))

    z_buffer.shape = (im.width, im.height)

    vertex_list, edges_list_with_text, texture_coordinates,vectorNormal = getPointDraw('african_head.obj')
    vertex_list = rotate_object(vertex_list, (0,0, 0), cam_position)
    vectorNormal = newVectorNormal()

    trianglesWithCoords = [tr.Triangle(get_point(int(triangle.first) - 1),
                                       get_point(int(triangle.second) - 1),
                                       get_point(int(triangle.third) - 1),
                                       get_normal_point(int(triangle.normalFirst) - 1),
                                       get_normal_point(int(triangle.normalSecond) - 1),
                                       get_normal_point(int(triangle.normalThird) - 1),
                                       get_texture_point(int(triangle.textureFirst) - 1),
                                       get_texture_point(int(triangle.textureSecond) - 1),
                                       get_texture_point(int(triangle.textureThird) - 1)) for triangle in
                           edges_list_with_text]

    for triangle in filter(lambda polygon: polygon.direction().angle(cam_direction) > 0,
                           trianglesWithCoords):
        pt.paint_polygon(triangle, draw, texture, z_buffer)

    im.save('african_head.png')
