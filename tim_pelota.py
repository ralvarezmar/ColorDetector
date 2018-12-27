#!/usr/bin/python -tt
# -*- codigo: utf-8 -*-

import cv2
import numpy as np
import argparse
import skimage
import skimage.morphology
import skimage.exposure
import skimage.segmentation

#Colores en BGR
RED_BGR=((120,200,94),(180,255,213))
BLUE_BGR=((100,150,0),(140,255,255))
GREEN_BGR=((55, 100, 50),(65, 255, 255))

def getFilter(color):
     if color == "rojo":
         filtro = (RED_BGR[0],RED_BGR[1])
     elif color == "azul":
         filtro = (BLUE_BGR[0],BLUE_BGR[1])
     elif color == "verde":
         filtro = (GREEN_BGR[0],GREEN_BGR[1])
     else:
        if args.hsv:
            lower_filter = cv2.cvtColor(np.uint8([[[args.rgb[0],args.rgb[1],args.rgb[2]]]]),cv2.COLOR_HSV2BGR)
            upper_filter = cv2.cvtColor(np.uint8([[[args.rgb[3],args.rgb[4],args.rgb[5]]]]),cv2.COLOR_HSV2BGR)
            filtro = (lower_filter,upper_filter)
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
           mask = skimage.morphology.opening(mask)
           detection=np.copy(mask)
           cv2.imshow('FILTRO',detection)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-hsv', '--hsv',type=int, nargs=6, dest ='hsv',help='Valores hsv para los que buscar color')
    parser.add_argument('-r', '--rgb',type=int, nargs=6, dest ='rgb',help='Valores rgb para los que buscar color')
    parser.add_argument('-c', '--color', help= 'Buscar color [rojo azul verde]')
    parser.add_argument('-v', '--video', help = 'Directorio al video')

    args = parser.parse_args()

    if args.video:
        filterVideo(args)
        
    print args
