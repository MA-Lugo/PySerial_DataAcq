from time import time
from colors import * 
from tkinter import *
from tkinter import ttk



GUI = Tk()
GUI.title("UART Data Acquisition")
GUI.configure(bg = bg_color) 
GUI.geometry('470x186')
GUI.resizable(width=False, height=False)

def run():
    pass

#FRAMES
item1  = Frame(height = 130, width = 150, bd = 2, relief = 'groove',bg =bg_color)
item1.place(x = 5, y = 5)

item2  = Frame(height = 130, width = 150, bd = 2, relief = 'groove',bg =bg_color)
item2.place(x = 160, y = 5)

item3  = Frame(height = 130, width = 150, bd = 2, relief = 'groove',bg =bg_color)
item3.place(x = 315, y = 5)

info  = Frame(height = 30, width = 460, bd = 2, relief = 'groove',bg = bg_color)
info.place(x = 5, y = 140)

#LABELS
Label(text = "mario.luggar@gmial.com",font =("",7),bg = bg_color,fg = '#F24C3D').place(x = 235, y =179,anchor="center")

#ENTRY
item_name1 = Entry(width = 15,bg = bg_color, fg = label_color, justify = "center")
item_name1.insert(INSERT,"ADC1")
item_name1.place(x = 80, y = 20, anchor = "center")

item_name2 = Entry(width = 15,bg = bg_color, fg = label_color, justify = "center")
item_name2.insert(INSERT,"ADC2")
item_name2.place(x = 80+155, y = 20, anchor = "center")

item_name3 = Entry(width = 15,bg = bg_color, fg = label_color, justify = "center")
item_name3.insert(INSERT,"ADC3")
item_name3.place(x = 80+155+155, y = 20, anchor = "center")



input_port = Entry(widt=12,font =("", 10),justify= "center",bg = gray_color,fg = label_color)
input_port.insert(INSERT,"COM4")
input_port.place(x = 80+155, y= 155,anchor = "center")

speed_port = Entry(widt=12,font =("", 10),justify="center",bg = gray_color,fg = label_color)
speed_port.insert(INSERT,"9600")
speed_port.place(x = 80+155+155, y= 155,anchor ="center")


#PROGRESS BAR
ProgressBar_style = ttk.Style()
ProgressBar_style.theme_use('clam')
ProgressBar_style.configure("red.Horizontal.TProgressbar", troughcolor=bg_color, background = red_color,bordercolor=red_color, lightcolor=red_color, darkcolor=red_color)
ProgressBar_style.configure("blue.Horizontal.TProgressbar", troughcolor=bg_color, background = blue_color,bordercolor=blue_color, lightcolor=blue_color, darkcolor=blue_color)
ProgressBar_style.configure("yellow.Horizontal.TProgressbar", troughcolor=bg_color, background = yellow_color,bordercolor=yellow_color, lightcolor=yellow_color, darkcolor=yellow_color)


pbar1 = ttk.Progressbar(style = "red.Horizontal.TProgressbar",orient = HORIZONTAL, mode = 'determinate', length = 130, max = 1024)
pbar1.place(x = 80, y = 110, anchor = "center")
pbar1["value"] = 512

pbar2 = ttk.Progressbar(style = "blue.Horizontal.TProgressbar",orient = HORIZONTAL, mode = 'determinate', length = 130, max = 1024)
pbar2.place(x = 80+155, y = 110, anchor = "center")
pbar2["value"] = 612

pbar3 = ttk.Progressbar(style = "yellow.Horizontal.TProgressbar",orient = HORIZONTAL, mode = 'determinate', length = 130, max = 1024)
pbar3.place(x = 80+155+155, y = 110, anchor = "center")
pbar3["value"] = 824

#VARIABLE LABELS
input1   = StringVar()
input1.set("0512")
Label(textvariable = input1,font =("", 25),bg = bg_color,fg = label_color).place(x = 80, y= 65,anchor= "center")

input2   = StringVar()
input2.set("0612")
Label(textvariable = input2,font =("", 25),bg = bg_color,fg = label_color).place(x = 80+155, y= 65,anchor= "center")

input2   = StringVar()
input2.set("0824")
Label(textvariable = input2,font =("", 25),bg = bg_color,fg = label_color).place(x = 80+155+155, y= 65,anchor= "center")


#BUTTONS
Button(text = "R U N",font = ("",7), command = run, width = 12,bg=red_color,fg =label_color).place(x = 80, y = 155,anchor="center")

if __name__ == '__main__':
    
    GUI.mainloop()