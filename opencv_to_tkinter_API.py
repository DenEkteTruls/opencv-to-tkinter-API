"""
Author --> Casper Nag
Start ---> 07.04.2021
Release -> 07.04.2021
"""

import cv2
import math
import threading
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from time import time, sleep
from functools import lru_cache


class CameraHandler():

    def __init__(self, camIndex):

        self.capsize = (640, 480)
        self.cap0 = cv2.VideoCapture(camIndex[0])
        self.cap1 = cv2.VideoCapture(camIndex[1])

        self.frame0 = None
        self.frame1 = None

        self.running = True

        self.frame0line = 0
        self.frame0lineXY = (0, 0)
        self.frame1line = 0
        self.frame1lineXY = (0, 0)

        self.active_mouse = -1
        self.mouse0 = (0, 0)
        self.mouse1 = (0, 0)

        threading._start_new_thread(self.read_cap, (0,))
        threading._start_new_thread(self.read_cap, (1,))


    def read_cap(self, camIndex):

        c = 0
        fps = 0
        aTime = time()

        while self.running:
            
            c += 1
            if time()-aTime >= 1: fps = c; c = 0; aTime = time()

            #print(f"FPS: {fps}")
            if camIndex == 0:
                tmp_img = cv2.resize(cv2.cvtColor(self.cap0.read()[1], cv2.COLOR_BGR2RGB), self.capsize)
                cv2.circle(tmp_img, (int(self.capsize[0]/2), int(self.capsize[1]/2)), 3, (255, 0, 100), 3)
                if self.active_mouse == 0:
                    self.frame0lineXY = (int(self.capsize[0]/2)-self.mouse0[0], int(self.capsize[1]/2)-self.mouse0[1])
                    self.frame0line = np.sqrt(self.frame0lineXY[0]**2+self.frame0lineXY[1]**2)
                    cv2.line(tmp_img, (int(self.capsize[0]/2), int(self.capsize[1]/2)), self.mouse0, (0, 150, 250), 2)    
                    cv2.putText(tmp_img, f"X:{-self.frame0lineXY[0]}, Y:{self.frame0lineXY[1]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                self.frame0 = ImageTk.PhotoImage(image=Image.fromarray(tmp_img))

            elif camIndex == 1:
                tmp_img = cv2.resize(cv2.cvtColor(self.cap1.read()[1], cv2.COLOR_BGR2RGB), self.capsize)
                cv2.circle(tmp_img, (int(self.capsize[0]/2), int(self.capsize[1]/2)), 3, (255, 0, 100), 3)
                if self.active_mouse == 1:
                    self.frame1lineXY = (int(self.capsize[0]/2)-self.mouse1[0], int(self.capsize[1]/2)-self.mouse1[1])
                    self.frame1line = np.sqrt(self.frame1lineXY[0]**2+self.frame1lineXY[1]**2)
                    cv2.line(tmp_img, (int(self.capsize[0]/2), int(self.capsize[1]/2)), self.mouse1, (0, 150, 250), 2)
                    cv2.putText(tmp_img, f"X:{-self.frame1lineXY[0]}, Y:{self.frame1lineXY[1]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA) 
                self.frame1 = ImageTk.PhotoImage(image=Image.fromarray(tmp_img))


    def get_cam(self, camIndex):

        if camIndex == 0:
            return self.frame0

        elif camIndex == 1:
            return self.frame1


    def handle_mouse(self, active_mouse, mouse0, mouse1):
        
        self.active_mouse = active_mouse
        self.mouse0 = mouse0
        self.mouse1 = mouse1

        
    def close(self):

        self.cap0.release()
        self.cap1.release()
        self.running = False


class Graphics():

    def __init__(self, title: str) -> None:

        self.root = tk.Tk()
        self.root.wm_title(title)
        self.root.resizable(False, False)
        
        self.font = ('Helvetica', 12, 'normal')

        self.aTime = 0
        
        self.active_mouse = -1
        self.mouse0 = (0, 0)
        self.mouse1 = (0, 0)

    
    def label(self, text, show=True):

        label = tk.Label(self.root, text=text, font=self.font)
        if show: label.pack()


    def button(self, text, callback, show=True):

        button = tk.Button(self.root, text=text, command=callback)
        if show: button.pack()


    def frame_surface(self, side):

        a = tk.Label(self.root)
        if side == "left":
            a.pack(side=tk.LEFT)
        elif side == "right":
            a.pack(side=tk.RIGHT)
        return a
    

    def show_cam(self, lmain, cam, index):

        #print(int((time()-self.aTime)*1000))
        self.aTime = time()
        cam.handle_mouse(self.active_mouse, self.mouse0, self.mouse1)

        if index == 0:
            frame = cam.frame0
        elif index == 1:
            frame = cam.frame1

        lmain.imgtk = frame
        lmain.configure(image=frame)
        lmain.after(10, self.show_cam, lmain, cam, index)


    def mouseMotion0(self, event):
        
        self.active_mouse = 0
        self.mouse0 = (event.x, event.y)


    def mouseMotion1(self, event):

        self.active_mouse = 1
        self.mouse1 = (event.x, event.y)


    def mainloop(self): self.root.mainloop()
