# -*- coding: utf-8 -*-
import os
import cv2
from ffmpy3 import FFmpeg

img_path = r'D:\testCode\pytest-PG\m695\standard.bmp'

def convert(img_path,H,W,output_path):
	size = '{}x{}'.format(W,H)
	ff = FFmpeg(inputs={img_path:None},
				outputs={output_path:'-s {} -pix_fmt yuv420p'.format(size)})
	print(ff.cmd)
	ff.run()

def main():
	img_bgr = cv2.imread(img_path)
	H,W = img_bgr.shape[1],img_bgr.shape[0]
	convert(img_path,H,W,r'D:\testCode\pytest-PG\m695\test420.yuv')#执行后在指定路径中将生成test.yuv文件


if __name__ == '__main__':
	main()

