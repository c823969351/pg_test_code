# -*- coding:utf-8 -*-

from math import e
import cv2
import numpy as np
import os

saveImagePath = 'D:/pattern/'

colorRed = [0, 0, 255]
colorGreen = [0, 255, 0]
colorBlue = [255, 0, 0]
colorWhite = [255, 255, 255]
colorBlack = [0, 0, 0]
colorAqua = [255, 255, 0]
colorFuchsia = [255, 0, 255]
colorYellow = [0, 255, 255]
stardardColors = [
    colorWhite, colorYellow, colorAqua, colorGreen, colorFuchsia, colorRed,
    colorBlue, colorBlack
]


def createImg(x, y, depth=3):
    return np.zeros((x, y, depth), np.uint8)


def saveImageFile(typeName, img):
    save = saveImagePath+'bmp/'
    filename = saveImagePath+'bmp/' + typeName + '.bmp'
    if not os.path.exists(save):
        os.mkdir(save)
    cv2.imwrite(filename, img)
    print(typeName + '.bmp', '\t\t...\tok')
    saveImageFile_JPG(typeName, img)
    saveImageFile_PNG(typeName, img)

def saveImageFile_PNG(typeName, img):
    save = saveImagePath +'png/'
    filename = saveImagePath +'png/' + typeName + '.png'
    if not os.path.exists(save):
        os.mkdir(save)
    cv2.imwrite(filename, img)
    print(typeName + '.png', '\t\t...\tok')

def saveImageFile_JPG(typeName, img):
    save = saveImagePath +'jpg/'
    filename = saveImagePath +'jpg/' + typeName + '.jpg'
    if not os.path.exists(save):
        os.mkdir(save)
    cv2.imwrite(filename, img)
    print(typeName + '.jpg', '\t\t...\tok')



def createOneColorImage(x, y, color):
    img = createImg(x, y)
    b_channel = np.ones((x, y), dtype=np.uint8) * color[0]
    g_channel = np.ones((x, y), dtype=np.uint8) * color[1]
    r_channel = np.ones((x, y), dtype=np.uint8) * color[2]
    img = cv2.merge((b_channel, g_channel, r_channel))
    return img


def createL128GrayImage(x, y):
    img = createImg(x, y, 3)
    img[:] = [128]
    return img


def createL64GrayImage(x, y):
    img = createImg(x, y, 3)
    img[:] = [64]
    return img


def createL32GrayImage(x, y):
    img = createImg(x, y, 3)
    img[:] = [32]
    return img


def create64GrayImage_p(x, y):
    img = createImg(x, y, 3)
    yPos = x / 64
    for i in range(0, 64):
        roi = img[int(i * yPos):int(i * yPos + yPos), 0:y]
        roi[:] = [i * 255 / 63]
        img[int(i * yPos):int(i * yPos + yPos), 0:y] = roi
        #cv2.imshow('image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    return img


def create64GrayImage(x, y):
    img = createImg(x, y, 3)
    xPos = y / 64
    for i in range(0, 64):
        roi = img[0:x, int(i * xPos):int(i * xPos + xPos)]
        roi[:] = [i * 255 / 63]
        img[0:x, int(i * xPos):int(i * xPos + xPos)] = roi
        #cv2.imshow('image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    return img


def create256GrayImage(x, y):
    img = createImg(x, y, 3)
    xPos = y / 256
    for i in range(0, 256):
        roi = img[0:x, int(i * xPos):int(i * xPos + xPos)]
        roi[:] = [i]
        img[0:x, int(i * xPos):int(i * xPos + xPos)] = roi
        #cv2.imshow('image',img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    return img


def createCheckBoardPattern(x, y, Nx_cor, Ny_cor):
    img = createImg(y, x, 3)  #取反
    Checkerboardx = int(x / Nx_cor)
    Checkerboardy = int(y / Ny_cor)
    black = np.zeros((Checkerboardy, Checkerboardx, 3), np.uint8)
    white = np.zeros((Checkerboardy, Checkerboardx, 3), np.uint8)
    black[:] = [0, 0, 0]  # 纯黑色
    white[:] = [255, 255, 255]  # 纯白色
    chess_x = black

    for i in range(1, Nx_cor):
        if i % 2 == 1:
            chess_x = np.concatenate([chess_x, white], axis=1)
        else:
            chess_x = np.concatenate([chess_x, black], axis=1)

    chess_x1 = 255 - chess_x
    black_white3 = chess_x1

    for i in range(1, Ny_cor):
        # 纵向连接
        if i % 2 == 1:
            black_white3 = np.concatenate(
                (black_white3, chess_x))  # =np.vstack((img1, img2))
        else:
            black_white3 = np.concatenate(
                (black_white3, chess_x1))  # =np.vstack((img1, img2))
    x, y, channel = black_white3.shape
    img[0:x, 0:y] = black_white3

    return img


def createStardardImage(x, y):
    img = createImg(x, y)
    #cv2.imshow('image', img)
    pixs = y / 8
    color = stardardColors[0]
    for i in range(0, 8):
        color = stardardColors[i]
        roiimg = img[0:x, int(i * pixs):int(i * pixs + pixs)]
        roiimg[:] = color
        img[0:x, int(i * pixs):int(i * pixs + pixs)] = roiimg

    return img


def createFlickerImage(x, y):
    img = createOneColorImage(x, y, colorWhite)
    x_v = x / 2
    y_v = y / 2
    xPos = x_v / 256
    lin = y / 256
    #####上三角形
    y_h = 0
    y1 = y
    for i in range(0, 256):
        roi = img[int(float(i * xPos)):int(float(i * xPos + xPos)),
                  int(y_h):int(y1)]
        roi[:] = [i]
        img[int(float(i * xPos)):int(float(i * xPos + xPos)),
            int(y_h):int(y1)] = roi
        '''cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        y1 = y1 - lin / 2
        y_h = y_h + lin / 2
    #####下三角形
    y_h = 0
    y2 = y
    for i in range(0, 256):
        roi = img[(x - int(float(i * xPos + xPos))):(x - int(float(i * xPos))),
                  int(y_h):int(y2)]
        roi[:] = [i]
        img[(x - int(float(i * xPos + xPos))):(x - int(float(i * xPos))),
            int(y_h):int(y2)] = roi
        '''cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        y2 = y2 - lin / 2
        y_h = y_h + lin / 2

    ######左三角形
    x_h = 0
    x1 = x
    yPos = y_v / 256
    lin_x = x/256
    for i in range(0, 256):
        roi = img[(int(x_h)):int(x1), 
                    int(float(i * yPos)):int(float(i * yPos + yPos))]
        roi[:] = [i]
        img[(int(x_h)):int(x1),
            int(float(i * yPos)):int(float(i * yPos + yPos))] = roi
        x1 = x1 - lin_x / 2
        x_h = x_h + lin_x / 2

    #######右三角形
    x_h = 0
    x2 = x
    yPos = y_v / 256
    lin_x = x2/256
    for i in range(0, 256):
        roi = img[(int(x_h)):int(x2), 
                    (y - int(float(i * yPos + yPos))):(y - int(float(i * yPos)))]
        roi[:] = [i]
        img[(int(x_h)):int(x2), 
                    (y - int(float(i * yPos + yPos))):(y - int(float(i * yPos)))] = roi
        x2 = x2 - lin_x / 2
        x_h = x_h + lin_x / 2

    return img

def createFlickerImage_w(x, y):
    img = createOneColorImage(x, y, colorBlack)
    x_v = x / 2
    y_v = y / 2
    xPos = x_v / 256
    lin = y / 256
    #####上三角形
    y_h = 0
    y1 = y
    for i in range(0, 256):
        roi = img[int(float(i * xPos)):int(float(i * xPos + xPos)),
                  int(y_h):int(y1)]
        roi[:] = [255-i]
        img[int(float(i * xPos)):int(float(i * xPos + xPos)),
            int(y_h):int(y1)] = roi
        '''cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        y1 = y1 - lin / 2
        y_h = y_h + lin / 2
    #####下三角形
    y_h = 0
    y2 = y
    for i in range(0, 256):
        roi = img[(x - int(float(i * xPos + xPos))):(x - int(float(i * xPos))),
                  int(y_h):int(y2)]
        roi[:] = [255-i]
        img[(x - int(float(i * xPos + xPos))):(x - int(float(i * xPos))),
            int(y_h):int(y2)] = roi
        '''cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''
        y2 = y2 - lin / 2
        y_h = y_h + lin / 2

    ######左三角形
    x_h = 0
    x1 = x
    yPos = y_v / 256
    lin_x = x/256
    for i in range(0, 256):
        roi = img[(int(x_h)):int(x1), 
                    int(float(i * yPos)):int(float(i * yPos + yPos))]
        roi[:] = [255-i]
        img[(int(x_h)):int(x1),
            int(float(i * yPos)):int(float(i * yPos + yPos))] = roi
        x1 = x1 - lin_x / 2
        x_h = x_h + lin_x / 2

    #######右三角形
    x_h = 0
    x2 = x
    yPos = y_v / 256
    lin_x = x2/256
    for i in range(0, 256):
        roi = img[(int(x_h)):int(x2), 
                    (y - int(float(i * yPos + yPos))):(y - int(float(i * yPos)))]
        roi[:] = [255-i]
        img[(int(x_h)):int(x2), 
                    (y - int(float(i * yPos + yPos))):(y - int(float(i * yPos)))] = roi
        x2 = x2 - lin_x / 2
        x_h = x_h + lin_x / 2

    return img


def draw(inp_x,inp_y):
    if not os.path.exists(saveImagePath):
        os.mkdir(saveImagePath)
    try:
        x = int(inp_y)  #1080 1024 2160
        y = int(inp_x)  #1920 1280 3840
    except ValueError:
        return 1

    print('Start Gen Test Screen Files ...')
    saveImageFile('red', createOneColorImage(x, y, colorRed))
    saveImageFile('green', createOneColorImage(x, y, colorGreen))
    saveImageFile('blue', createOneColorImage(x, y, colorBlue))
    saveImageFile('white', createOneColorImage(x, y, colorWhite))
    saveImageFile('black', createOneColorImage(x, y, colorBlack))
    saveImageFile('L32gray', createL32GrayImage(x, y))
    saveImageFile('L64gray', createL64GrayImage(x, y))
    saveImageFile('L128gray', createL128GrayImage(x, y))
    saveImageFile('64gray', create64GrayImage(x, y))
    saveImageFile('256gray', create256GrayImage(x, y))
    saveImageFile('64gray_p', create64GrayImage_p(x, y))

    Nx_cor = 8
    Ny_cor = 8

    saveImageFile('checkboard_Pattern',
                  createCheckBoardPattern(y, x, Ny_cor, Nx_cor))  #分辨率参数等取反
    saveImageFile('standard', createStardardImage(x, y))
    saveImageFile('Flicker', createFlickerImage(x, y))
    saveImageFile('Flicker_w',createFlickerImage_w(x,y))
    print('Generate Success!')



if __name__ == '__main__':
    y = int(input('请输入x :'))
    x = int(input('请输入y :'))
    print('Start Gen Test Screen Files ...')
    saveImageFile('red', createOneColorImage(x, y, colorRed))
    saveImageFile('green', createOneColorImage(x, y, colorGreen))
    saveImageFile('blue', createOneColorImage(x, y, colorBlue))
    saveImageFile('white', createOneColorImage(x, y, colorWhite))
    saveImageFile('black', createOneColorImage(x, y, colorBlack))
    saveImageFile('L32gray', createL32GrayImage(x, y))
    saveImageFile('L64gray', createL64GrayImage(x, y))
    saveImageFile('L128gray', createL128GrayImage(x, y))
    saveImageFile('64gray', create64GrayImage(x, y))
    saveImageFile('256gray', create256GrayImage(x, y))
    saveImageFile('64gray_p', create64GrayImage_p(x, y))
    Nx_cor = 8
    Ny_cor = 8
    saveImageFile('checkboard_Pattern',
                  createCheckBoardPattern(y, x, Ny_cor, Nx_cor))  #分辨率参数等取反
    saveImageFile('standard', createStardardImage(x, y))
    saveImageFile('Flicker', createFlickerImage(x, y))
    saveImageFile('Flicker_w',createFlickerImage_w(x,y))
    print('Generate Success!')
