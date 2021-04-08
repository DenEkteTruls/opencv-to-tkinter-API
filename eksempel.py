"""
Author --> Casper Nag
Start ---> 07.04.2021
Release -> ??.04.2021
"""

#
# Eksempelkode her ...
#
# Det er label og button funksjon i API-et for å få en deilig liten oneliner.
#

import tkinter as tk
from new import CameraHandler, Graphics

cameraHandler = CameraHandler((0, "c:/users/caspe/videos/sjakken.m4v"))
graphics = Graphics("Program v.2")

focal_var = "Brennvidde: 500mm | 2.6924060829966665"
graphics.label(focal_var)

focal_entry = tk.Entry(graphics.root)
focal_entry.pack()

graphics.button("UPDATE", lambda e: print("funksjonen din..."))

surface0 = graphics.frame_surface("left")
surface0.bind("<Button-1>", graphics.mouseMotion0)
graphics.show_cam(surface0, cameraHandler, 0)

surface1 = graphics.frame_surface("right")
surface1.bind("<Button-1>", graphics.mouseMotion1)
graphics.show_cam(surface1, cameraHandler, 1)

graphics.mainloop()
cameraHandler.close()
