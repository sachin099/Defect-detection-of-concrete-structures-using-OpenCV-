
'''Defect detection of concrete structures using OpenCV 
This is a dummy model of how I want to create this application 
using Deep learning algorithms.
Ignore the stitching of images process of which the dummy model
is being developed in case the images are taken through drones.
Ignore the alignment of images and size in GUI template.

Main application would contain real time acquisition of images
'''

import cv2
import numpy as np
import Tkinter
from Tkinter import *
from PIL import ImageTk,Image
import tkFont
import tkFileDialog
import sys
import imutils
from urllib2 import urlopen
import io

top=Tkinter.Tk()
top.geometry('1920x1080')
top.title("Defect detection of concrete structures using OpenCV")
var = StringVar()

T=Text(top, height=4, width=200)
T.pack(side=TOP)
T.tag_configure('big', font=('Verdana', 20, 'bold'))
T.tag_configure('color', foreground='#000000', font=('Tempus Sans ITC', 12, 'bold'))
T.tag_bind('follow', '<1>', lambda e, t=T: t.insert(END, "Not now, maybe later!"))
quote = """Visual Inspection of Concrete Structures using Image Processing Tools"""
T.insert(END, quote , 'big')

top.configure(background='yellow')
path="GUI_BACK.PNG"
img = ImageTk.PhotoImage(Image.open(path))
panel =Tkinter.Label(top, image=img)
panel.pack(side ="bottom", fill="both", expand="yes")

top.configure(background="lightblue")

#function for selecting image
def select_image():
    top.filename = tkFileDialog.askopenfilename(title = "Select file", filetypes = (("jpeg files","*.jpg"), ("all files","*.*")))
    img = ImageTk.PhotoImage(Image.open(top.filename))
    
    panel = Tkinter.Label(top, image = img)
    panel.image = img
    panel.place(height =600, width=900, x=20, y=100)


#function for making crack pattern
def cracks():
    select_image()
    img = cv2.imread(top.filename)    
                     
    kernel =np.ones((5,5),np.uint8)

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(img_grey,5)  #median filter to remove noise
    opening = cv2.morphologyEx(median, cv2.MORPH_OPEN, kernel)

    edges = cv2.Canny(opening,100,200)  #canny edge detection
    cv2.imshow('image1', edges)
    cv2.imwrite('data_set7.jpg', edges)

#function for detecting spalling
def spalling():
    select_image()
    img = cv2.imread(top.filename) 
    kernel = np.ones((5,5),np.uint8)
    
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(img,5)
    closing = cv2.morphologyEx(median, cv2.MORPH_CLOSE, kernel)
    median1 = cv2.medianBlur(closing,5)
    edges = cv2.Canny(median1,100,200)

    #finding contours
    ret,thresh = cv2.threshold(edges,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img_c = cv2.drawContours(img, contours, -1, (0,255,0), 3)

    cv2.imshow('image0', img_c)


#function for detecting voids
def voids():
    radius1 = 0
    cent = ();
    count=0;
    select_image()

    img = cv2.imread(top.filename)
    kernel = np.ones((5,5),np.uint8)

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    median = cv2.medianBlur(img,5)
    dilate = cv2.dilate(median, kernel, iterations=1)
    opening = cv2.morphologyEx(dilate, cv2.MORPH_OPEN, kernel)

    edges = cv2.Canny(opening,100,200)

    ret,thresh = cv2.threshold(edges,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        img = cv2.circle(img,center,radius,(0,255,0),2)
        count = count+1
        if radius > radius1:
           radius1=radius
           cent= center

    print ("Radius of largest Void", radius1)
    print ("Centroid of Largest Void", cent)
    print ("No.of voids in image section:", count)
    
    cv2.imshow('image0', img)
    cv2.putText(img,"Hello World!",(100,100),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2)

#Stitching of multiple continuous images
def stitch():
    novi = Toplevel()
    canvas = Canvas(novi, width = 300, height = 200)
    canvas.pack(expand = YES, fill = BOTH)
    gif1 = PhotoImage(file = 'Final.gif')
    #image not visual
    canvas.create_image(50, 10, image = gif1, anchor = NW)
    #assigned the gif1 to the canvas object
    canvas.gif1 = gif1


w=Tkinter.Button(top, text="Cracks", command=cracks, bd=10)
x=Tkinter.Button(top, text="Voids",command=voids, bd=10)
y=Tkinter.Button(top, text="Spalling", command=spalling, bd=10)
z=Tkinter.Button(top, text="Stitching of samples",command=stitch, bd=10)
btn = Tkinter.Button(top, text="Review an image", command=select_image, bd=10)


w.place(height=50, width=200, x=1000, y=270)
x.place(height=50, width=200, x=1000, y=360)
y.place(height=50, width=200, x=1000, y=450)
z.place(height=50, width=200, x=1000, y=540)
btn.place(height=50, width=200, x=1000, y=630)
top.mainloop()

