"""
Author --> Casper Nag
Start ---> 07.04.2021
Release -> ??.04.2021
"""

import tkinter as tk
from PIL import Image, ImageTk
import cv2, math
import threading

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

root = tk.Tk()
focal_init = tk.StringVar()
focal_init.set("Brennvidde: 500mm | 2.6924060829966665")

focal_label = tk.Label(root, textvariable = focal_init)
focal_label.pack()
focal_entry = tk.Entry(root)
focal_entry.pack()
h_sensor = 23.5 #horisontal bredde på d500 sensor
focal_lenght = 500
_, frame = cap.read()
h_angle = 2 * math.atan(float(h_sensor) / (2 * int(focal_lenght))) * (360 / (2 * math.pi))

def angle(h_sensor, focal_lenght):
    global h_angle
    h_angle = 2 * math.atan(float(h_sensor) / (2 * int(focal_lenght))) * (360 / (2 * math.pi))

angle(h_sensor, focal_lenght)
degrees_per_pixel = h_angle/frame.shape[1]

centerFrame = int(frame.shape[1]/2), int(frame.shape[0]/2)
posList = centerFrame
def onMouse(event, x, y, flags, param):
    global posList
    if event == cv2.EVENT_LBUTTONDOWN:
        posList = (x, y)
        print(posList)
        degrees_to_mouse(posList)

def degrees_to_mouse(posList):
    h_angle_to_mouse = degrees_per_pixel*(posList[0]-centerFrame[0])
    v_angle_to_mouse = degrees_per_pixel*(posList[1]-centerFrame[1])
    print(h_angle_to_mouse)
    print(v_angle_to_mouse)


def update_focal():
    inn = focal_entry.get()
    print(inn)
    angle(h_sensor, inn)
    global degrees_per_pixel
    degrees_per_pixel = h_angle/frame.shape[1]
    print(h_angle)
    focal_init.set("Brennvidde: " + inn + "mm | " + str(h_angle) + "°")

def show_frame():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    #cv2.setMouseCallback(frame, onMouse)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)
def show_frame2():
    _, frame2 = cap2.read()
    cv2image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
    img2 = Image.fromarray(cv2image2)
    imgtk2 = ImageTk.PhotoImage(image=img2)
    lmain2.imgtk = imgtk2
    lmain2.configure(image=imgtk2)
    lmain2.after(10, show_frame2)
update = tk.Button(root, text="Oppdater brennvidde", command=update_focal)
update.pack()

lmain = tk.Label(root)
lmain.pack(side=tk.LEFT)
lmain2 = tk.Label(root)
lmain2.pack(side=tk.RIGHT)
show_frame()
show_frame2()
root.mainloop()

while True:
    _, frame = cap.read()

    cv2.imshow("Dslr video", frame)
    cv2.setMouseCallback("Dslr video", onMouse)
#
    cv2.waitKey(10)