import numpy as np
import triangle as tr

def getPointDraw(x,y):
	objFile = open('african_head.obj', 'r')
	vertexList = []
	edgesList = []
	for line in objFile:
		split = line.split()
		if not len(split):
			continue
		if split[0] == "v":
			vertexList.append(split[1:])
		if split[0] == "f":
			edgesList.append(readEdges(line))

	objFile.close()

	vertexList = np.array(vertexList, dtype=np.float32)
	vertexList = np.matrix(vertexList)

	if (x == 'x') and (y=='y'):
		return vertexList[:,0], vertexList[:,1], edgesList
	if (x == 'y') and (y=='z'):
		return vertexList[:,1],vertexList[:,2], edgesList
	if (x == 'x') and (y=='z'):
		return vertexList[:,0], vertexList[:,2], edgesList


def readEdges(line):
    split = line.split()
    vertexes = []
    for i in range(1, len(split)):
        vertexes.append(split[i].split('/')[0])
    triangle = tr.Triangle(vertexes[0], vertexes[1], vertexes[2])
    # print(triangle.first, triangle.second, triangle.third)
    return triangle
