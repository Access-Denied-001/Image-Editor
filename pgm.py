# name: File path of the pgm image file
# Output is a 2D list of integers
from math import *


def readpgm(name):
    image = []
    with open(name) as f:
        lines = list(f.readlines())
        if len(lines) < 3:
            print("Wrong Image Format\n")
            exit(0)

        count = 0
        width = 0
        height = 0
        for line in lines:
            if line[0] == '#':
                continue

            if count == 0:
                if line.strip() != 'P2':
                    print("Wrong Image Type\n")
                    exit(0)
                count += 1
                continue

            if count == 1:
                dimensions = line.strip().split(' ')
                print(dimensions)
                width = dimensions[0]
                height = dimensions[1]
                count += 1
                continue

            if count == 2:
                allowable_max = int(line.strip())
                if allowable_max != 255:
                    print("Wrong max allowable value in the image\n")
                    exit(0)
                count += 1
                continue

            data = line.strip().split()
            data = [int(d) for d in data]
            image.append(data)
    return image


# img is the 2D list of integers
# file is the output file path
def writepgm(img, file):
    with open(file, 'w') as fout:
        if len(img) == 0:
            pgmHeader = 'p2\n0 0\n255\n'
        else:
            pgmHeader = 'P2\n' + str(len(img[0])) + ' ' + str(len(img)) + '\n255\n'
            fout.write(pgmHeader)
            line = ''
            for i in img:
                for j in i:
                    line += str(j) + ' '
            line += '\n'
            fout.write(line)


def averagingfilter(image):
    copy = [[0 for i in range(len(image[1]))] for j in range(len(image))]
    for i in range(1, len(image) - 1):
        for j in range(1, len(image[2]) - 1):
            copy[i][j] = (image[i - 1][j - 1] + image[i - 1][j] + image[i - 1][j + 1] + image[i][j - 1] + image[i][j] +
                          image[i][j + 1] + image[i + 1][j - 1] + image[i + 1][j] + image[i + 1][j + 1]) / 9
    i = 0
    for j in range(len(image[4]) - 1):
        copy[i][j] = image[i][j]
    i = len(image) - 1
    for j in range(len(image[3]) - 1):
        copy[i][j] = image[i][j]
    j = 0
    for i in range(len(image) - 1):
        copy[i][j] = image[i][j]
    j = len(image) - 1
    for i in range(len(image) - 1):
        copy[i][j] = image[i][j]
    return copy


def edgedetection(image):
    imageo = [[0 for i in range(len(image[1]) + 2)] for j in range(len(image) + 2)]
    for i in range(len(image)):
        for j in range(len(image[2])):
            imageo[i + 1][j + 1] = image[i][j]
    edge1 = [[0 for i in range(len(image[1]))] for j in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[2])):
            hdif = (imageo[i][j] - imageo[i][j + 2]) + 2 * (imageo[i + 1][j] - imageo[i + 1][j + 2]) + (
                        imageo[i + 2][j] - imageo[i + 2][j + 2])
            vdif = (imageo[i][j] - imageo[i + 2][j]) + 2 * (imageo[i][j + 1] - imageo[i + 2][j + 1]) + (
                        imageo[i][j + 2] - imageo[i + 2][j + 2])
            edge1[i][j] = int((sqrt(hdif ** 2 + vdif ** 2)) / 6)
    return edge1


def edgedetection1(image):
    imageo = [[0 for i in range(len(image[1]) + 2)] for j in range(len(image) + 2)]
    for i in range(len(image)):
        for j in range(len(image[2])):
            imageo[i + 1][j + 1] = image[i][j]
    edge = [[0 for i in range(len(image[1]))] for j in range(len(image))]
    for i in range(len(image)):
        for j in range(len(image[2])):
            hdif = (imageo[i][j] - imageo[i][j + 2]) + 2 * (imageo[i + 1][j] - imageo[i + 1][j + 2]) + (
                        imageo[i + 2][j] - imageo[i + 2][j + 2])
            vdif = (imageo[i][j] - imageo[i + 2][j]) + 2 * (imageo[i][j + 1] - imageo[i + 2][j + 1]) + (
                        imageo[i][j + 2] - imageo[i + 2][j + 2])
            edge[i][j] = sqrt(hdif ** 2 + vdif ** 2)
    return edge


def Minenergy(image):
    edge = edgedetection1(image)
    Minenergy = [[0 for i in range(len(edge[1]))] for j in range(len(edge))]
    for j in range(len(edge[1])):
        Minenergy[0][j] = edge[0][j]
    for i in range(1, len(edge)):
        for j in range(1, len(edge[2]) - 1):
            Minenergy[i][j] = edge[i][j] + min(Minenergy[i - 1][j - 1], Minenergy[i - 1][j], Minenergy[i - 1][j + 1])
        j = 0
        Minenergy[i][j] = edge[i][j] + min(Minenergy[i - 1][j], Minenergy[i - 1][j + 1])
        j = len(edge[2]) - 1
        Minenergy[i][j] = edge[i][j] + min(Minenergy[i - 1][j - 1], Minenergy[i - 1][j])
    arr = [[0 for i in range(len(edge[2]))] for j in range(len(edge))]
    mn = min(Minenergy[len(edge) - 1])
    for j in range(len(edge[1])):
        if Minenergy[len(edge) - 1][j] == mn:
            arr[len(edge) - 1][j] = 1
    for i in range(len(arr) - 1, 0, -1):
        for j in range(len(arr[0])):
            if arr[i][j] == 1:
                if j == 0:
                    z = min(Minenergy[i - 1][0], Minenergy[i - 1][1])
                    if Minenergy[i - 1][0] == z:
                        arr[i - 1][0] = 1
                    if Minenergy[i - 1][1] == z:
                        arr[i - 1][1] = 1

                elif j == len(edge[0]) - 1:
                    z = min(Minenergy[i - 1][len(edge[0]) - 1], Minenergy[i - 1][len(edge[0]) - 2])
                    if Minenergy[i - 1][len(edge[0]) - 1] == z:
                        arr[i - 1][len(edge[0]) - 1] = 1
                    if Minenergy[i - 1][len(edge[0]) - 2] == z:
                        arr[i - 1][len(edge[0]) - 2] = 1
                else:
                    z = min(Minenergy[i - 1][j], Minenergy[i - 1][j + 1], Minenergy[i - 1][j - 1])
                    if Minenergy[i - 1][j] == z:
                        arr[i - 1][j] = 1
                    if Minenergy[i - 1][j + 1] == z:
                        arr[i - 1][j + 1] = 1
                    if Minenergy[i - 1][j - 1] == z:
                        arr[i - 1][j - 1] = 1
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if arr[i][j] == 1:
                image[i][j] = 255
    return image


########## Function Calls ##########
x = readpgm('test.pgm')
y = averagingfilter(x)
w = edgedetection(x)
i = Minenergy(x)
# test.pgm is the image present in the same working directory
writepgm(x, 'test_o.pgm')
writepgm(y, 'average.pgm')
writepgm(w, 'edge.pgm')
writepgm(i, 'Min.pgm')
# x is the image to output and test_o.pgm is the image output in the same working directory
###################################
