import numpy as np


def getPointDraw(x,y):
	objFile = open('african_head.obj', 'r')
	vertexList = []
	for line in objFile:
		split = line.split()
		if not len(split):
			continue
		if split[0] == "v":
			vertexList.append(split[1:])
	objFile.close()

	vertexList = np.array(vertexList, dtype=np.float32)
	vertexList = np.matrix(vertexList)

	if (x == 'x') and (y=='y'):
		return vertexList[:,0], vertexList[:,1]
	if (x == 'y') and (y=='z'):
		return vertexList[:,1],vertexList[:,2]
	if (x == 'x') and (y=='z'):
		return vertexList[:,0], vertexList[:,2]

