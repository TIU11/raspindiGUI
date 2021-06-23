import os
import tkinter as tk
from tkinter.ttk import *
import sys
import time
#----------------------------------------------------------------------------------------------------------------------------
window = tk.Tk()
#window.geometry("400x300")
window.title("Raspberry Pi NDI Streaming")

dpi = window.winfo_fpixels('1i')
factor = dpi / 72

width = window.winfo_screenwidth()
height = window.winfo_screenheight()

#print(width) 2,073,600
#print(height)


ratio_1 = width * height
ratio_2 = 1
r2_width = 4
r2_height = 3

while (ratio_1 / ratio_2) != 17.28:
    r2_height = r2_width / 1.333333333333333333333333333333333333333333333333333333
    ratio_2 = r2_width * r2_height
    r2_width = r2_width + 1

    if (ratio_1/ratio_2) <= 17.28:
        break
    if width + 1 == r2_width:
        break

window.update_idletasks()


window.geometry(str(r2_width) + "x"+ str(int(r2_height)))

starting_frame = tk.Canvas(window)

factor_multiplier = (.40*factor) +.46
factor = factor/factor_multiplier
#1.3333333333333333
factor = 1.3
starting_frame.tk.call('tk', 'scaling', factor)
starting_frame.place(height=int(r2_height), width = r2_width)
background_color = "#0e628f"
starting_frame.configure(background = background_color)
#----------------------------------------------------------------------------------------------------------------------------
euid = os.geteuid()

if euid != 0:
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)


#----------------------------------------------------------------------------------------------------------------------------
all_lines = None
with open("/etc/raspindi.conf", "r") as file:
    all_lines = file.readlines()
all_lines_copy = all_lines[:]
for index, item in enumerate(all_lines):
    if index > 5:
        all_lines[index] = item[1:]
#----------------------------------------------------------------------------------------------------------------------------
def start_normal():
    with open("/etc/raspindi.conf", "w") as file:
        all_lines[6] = 'awb: "{}"; // Options: auto, sunlight, cloudy, shade, tungsten, fluorescent, incadescent, flash, horizon, max, off\n'.format(wb_clicked.get())
        all_lines[7] = 'saturation: {}; // Value in range 0 - 100\n'.format(str(saturation.get()))
        all_lines[8] = 'sharpness: {}; // Value in range 0 - 100\n'.format(str(sharpness.get()))
        all_lines[9] = 'contrast: {}; // Value in range 0 - 100\n'.format(str(contrast.get()))
        all_lines[10] = 'brightness: {}; // Value in range 0 - 100\n'.format(str(brightness.get()))
        all_lines[11] = 'exposuremode: "{}"; // Options: auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks, max, off\n'.format(ex_clicked.get())
        all_lines[12] = 'meteringmode: "{}"; // Options: average, spot, backlit, matrix, max\n'.format(m_clicked.get())
        all_lines[13] = 'rotation: {}; // Options: 0, 90, 180, 270\n'.format(str(ro_clicked.get()))
        all_lines[14] = 'mirror: "{}"; // Options: none, horizontal, vertical, both\n'.format(mr_clicked.get())
        for i in all_lines: file.write(i)


    stream = os.popen('/opt/raspindi/raspindi.sh')
    start['state'] = tk.DISABLED
    stop['state'] = tk.NORMAL


def stop_stream():
    os.popen('killall -9 raspindi')
    start['state'] = tk.NORMAL
    stop['state'] = tk.DISABLED
    for i in all_lines_copy: file.write(i)

start = tk.Button(starting_frame, text="Start streaming",command = start_normal , font= ("Calibri 14"), height = 2, width = 12)
start.place(relx = .5, rely = .68, anchor = tk.CENTER)

stop = tk.Button(starting_frame, text="Stop streaming",command = stop_stream , font= ("Calibri 14"), height = 2, width = 12, state = tk.DISABLED)
stop.place(relx = .5, rely = .89, anchor = tk.CENTER)

white_balance = ["auto", "sunlight", "cloudy", "shade", "tungsten", "fluorescent", "incadescent", "flash", "horizon", "max", "off"]
wb_clicked = tk.StringVar()
wb_clicked.set("auto")
wb_drop = tk.OptionMenu(starting_frame, wb_clicked, *white_balance)
wb_drop.config(width = 11)
wb_drop["highlightthickness"] = 0
wb_drop.place(relx = .18, rely = .15, anchor = tk.CENTER)
wb_text = tk.Label(starting_frame, text = "White Balance", bg = background_color)
wb_text.place(relx = .18, rely = .07, anchor = tk.CENTER)

mirror_opt = ["none", "horizontal", "vertical", "both"]
mr_clicked = tk.StringVar()
mr_clicked.set("none")
mr_drop = tk.OptionMenu(starting_frame, mr_clicked, *mirror_opt)
mr_drop.config(width = 11)
mr_drop["highlightthickness"] = 0
mr_drop.place(relx = .5, rely = .15, anchor = tk.CENTER)
mr_text = tk.Label(starting_frame, text = "Mirroring", bg = background_color)
mr_text.place(relx = .5, rely = .07, anchor = tk.CENTER)

exposures = ["auto", "night", "nightpreview", "backlight", "spotlight", "sports", "snow", "beach", "verylong", "fixedfps", "antishake", "fireworks", "max", "off"]
ex_clicked = tk.StringVar()
ex_clicked.set("auto")
ex_drop = tk.OptionMenu(starting_frame, ex_clicked, *exposures)
ex_drop.config(width = 11)
ex_drop["highlightthickness"] = 0
ex_drop.place(relx = .82, rely = .15, anchor = tk.CENTER)
ex_text = tk.Label(starting_frame, text = "Exposure", bg = background_color)
ex_text.place(relx = .82, rely = .07, anchor = tk.CENTER)


metering = ["average", "spot", "backlit", "matrix", "max"]
m_clicked = tk.StringVar()
m_clicked.set("average")
m_drop = tk.OptionMenu(starting_frame, m_clicked, *metering)
m_drop.config(width = 7)
m_drop["highlightthickness"] = 0
m_drop.place(relx = .85, rely = .68, anchor = tk.CENTER)
m_text = tk.Label(starting_frame, text = "Metering Mode", bg = background_color)
m_text.place(relx = .85, rely = .60, anchor = tk.CENTER)

rotation = ["0", "90", "180", "270"]
ro_clicked = tk.StringVar()
ro_clicked.set("0")
ro_drop = tk.OptionMenu(starting_frame, ro_clicked, *rotation)
ro_drop.config(width = 7)
ro_drop["highlightthickness"] = 0
ro_drop.place(relx = .15, rely = .68, anchor = tk.CENTER)
ro_text = tk.Label(starting_frame, text = "Orientation", bg = background_color)
ro_text.place(relx = .15, rely = .60, anchor = tk.CENTER)

saturation = tk.Scale(starting_frame, from_=0, to=100,length = 100, orient= tk.HORIZONTAL, bg = background_color)
saturation["highlightthickness"] = 0
saturation.place(relx = .65, rely = .47, anchor = tk.CENTER)
saturation_text = tk.Label(starting_frame, text = "Saturation", bg = background_color)
saturation_text.place(relx = .87, rely = .50, anchor = tk.CENTER)

contrast = tk.Scale(starting_frame, from_=0, to=100,length = 100, orient= tk.HORIZONTAL, bg = background_color)
contrast["highlightthickness"] = 0
contrast.place(relx = .35, rely = .47, anchor = tk.CENTER)
contrast_text = tk.Label(starting_frame, text = "Contrast", bg = background_color)
contrast_text.place(relx = .14, rely = .50, anchor = tk.CENTER)

sharpness = tk.Scale(starting_frame, from_=0, to=100,length = 100, orient= tk.HORIZONTAL, bg = background_color)
sharpness["highlightthickness"] = 0
sharpness.place(relx = .65, rely = .27, anchor = tk.CENTER)
sharpness_text = tk.Label(starting_frame, text = "Sharpness", bg = background_color)
sharpness_text.place(relx = .87, rely = .30, anchor = tk.CENTER)

brightness = tk.Scale(starting_frame, from_=0, to=100,length = 100, orient= tk.HORIZONTAL, bg = background_color)
brightness["highlightthickness"] = 0
brightness.place(relx = .35, rely = .27, anchor = tk.CENTER)
brightness.set(50)
brightness_text = tk.Label(starting_frame, text = "Brightness", bg = background_color)
brightness_text.place(relx = .13, rely = .30, anchor = tk.CENTER)


window.mainloop()
