#!/usr/bin/python -tt
# -*- codigo: utf-8 -*-

import cv2
import numpy as np
import argparse
import skimage
import skimage.morphology
import skimage.exposure
import skimage.segmentation
import skimage.io as io
import math

#Colores en BGR
RED_HSV=((120,200,94),(180,255,213))
BLUE_HSV=((100,150,0),(140,255,255))
GREEN_HSV=((55, 100, 50),(65, 255, 255))


def getFilter(color):
     if color == "rojo":
         filtro = (RED_HSV[0],RED_HSV[1])
     elif color == "azul":
         filtro = (BLUE_HSV[0],BLUE_HSV[1])
     elif color == "verde":
         filtro = (GREEN_HSV[0],GREEN_HSV[1])
     else:
         if args.hsv:
             filtro = (args.hsv[0],args.hsv[1],args.hsv[2]),(args.hsv[3],args.hsv[4],args.hsv[5])
         if args.rgb:
             lower_filter = cv2.cvtColor(np.uint8([[[args.rgb[0],args.rgb[1],args.rgb[2]]]]),cv2.COLOR_RGB2BGR)
             upper_filter = cv2.cvtColor(np.uint8([[[args.rgb[3],args.rgb[4],args.rgb[5]]]]),cv2.COLOR_RGB2BGR)
             filtro = (lower_filter,upper_filter)
     return filtro

def filterVideo(args):
   cap = cv2.VideoCapture(args.video)
   filtro = getFilter(args.color)
   while(True):
       ret, input_image = cap.read()
       if input_image is not None:
           filter_image=cv2.GaussianBlur(input_image,(5,5),0)
           hsv_image=cv2.cvtColor(filter_image,cv2.COLOR_BGR2HSV)
           mask = cv2.inRange(hsv_image,filtro[0],filtro[1])
           mask = cv2.erode(mask, None, iterations=2)
           mask = cv2.dilate(mask, None, iterations=2)
           detection=np.copy(mask)
           cv2.imshow('FILTRO',detection)
           # cv2.imshow('frame',input_image)
           ret,thresh = cv2.threshold(detection,127,255,0)
           if cv2.waitKey(1) & 0xFF == ord('q'):
               break
           im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
           for rectangulo in contours:
               if rectangulo.any != 0:
                   areas = [cv2.contourArea(rectangulo) for rectangulo in contours]
                   max_index = np.argmax(areas)
                   cnt=contours[max_index]
                   if max(areas) > 0.0:
                       x,y,w,h = cv2.boundingRect(cnt)
                       cv2.rectangle(input_image,(x,y),(x+w,y+h),(0,255,0),2)
                       cv2.imshow('DETECCION',input_image)

   cap.release()
   cv2.destroyAllWindows()

def filterImage(args):
    image = io.imread(args.image)
    filtro = getFilter(args.color)
    # io.imshow('Imagen',image)
    filter_image=cv2.GaussianBlur(image,(5,5),0)
    hsv_image=cv2.cvtColor(filter_image,cv2.COLOR_BGR2HSV)
    io.imsave("hsv.jpg",hsv_image)
    mask = cv2.inRange(hsv_image,filtro[0],filtro[1])
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    ret,thresh = cv2.threshold(mask,127,255,0)
    # cv2.imshow('Mascara',mask)
    io.imshow(mask)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-hsv', '--hsv',type=int, nargs=6, dest ='hsv',help='Valores hsv para los que buscar color')
    parser.add_argument('-r', '--rgb',type=int, nargs=6, dest ='rgb',help='Valores rgb para los que buscar color')
    parser.add_argument('-c', '--color', help= 'Buscar color')
    parser.add_argument('-v', '--video', help = 'Directorio al video')
    parser.add_argument('-i', '--image', help = 'Directorio a la imagen')

    args = parser.parse_args()

    if args.video:
        filterVideo(args)
    if args.image:
        filterImage(args)
    print args
