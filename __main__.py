import time
import threading
from colors import * 
from tkinter import *
from tkinter import ttk
import serial



GUI = Tk()
GUI.title("UART Data Acquisition")
GUI.configure(bg = bg_color) 
GUI.geometry('470x186')
GUI.resizable(width=False, height=False)


connection_status = False
filtered_data = ""
sample_rate = 0.05 # 50 ms

def ConnectionEnd():
    global connection_status
    control_button.config(text = "R U N")
    control_button.config(bg = blue_color)
    connection_status = False

def ConnectionStart():
    global connection_status
    control_button.config(text = "S T O P")
    control_button.config(bg = red_color)
    connection_status = True



def CTRLButton_Handle():
    global connection_status
    global serial_object

    if (connection_status == False):
        Try_Connection()
    else:
        ConnectionEnd()
        serial_object.close()



def Try_Connection():
    global connection_status 
    global serial_object
    port = input_port.get()
    speed = speed_port.get()

    try:
        serial_object = serial.Serial( str(port), baudrate= speed, timeout = 1)
        ConnectionStart()
    except:
        
        print ("Cant Open Specified Port")
        ConnectionEnd()


def SerialDataAcq():
    global connection_status
    global serial_object
    global filtered_data

    while(1):
        time.sleep(0.01) #delay for do not overload the CPU
        while(connection_status):
            try:
                serial_input = serial_object.readline()
                filtered_data = serial_input
            except:
                print("Connection Error")

def UpdateGUI():
    global connection_status
    global filtered_data
    while(1):
        time.sleep(0.01)#delay for do not overload the CPU
        while(connection_status):
            time.sleep(sample_rate/2)
            print(filtered_data)
            
    

myThread1 = threading.Thread(target = UpdateGUI)
myThread1.daemon = True
myThread1.start()   

myThread2 = threading.Thread(target = SerialDataAcq)
myThread2.daemon = True
myThread2.start()   

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
input_port.insert(INSERT,"COM3")
input_port.place(x = 80+155, y= 155,anchor = "center")

speed_port = Entry(widt=12,font =("", 10),justify="center",bg = gray_color,fg = label_color)
speed_port.insert(INSERT,"19200")
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

control_button = Button(text = "R U N",font = ("",7),width = 12,command = CTRLButton_Handle,bg=blue_color,fg =label_color)
control_button.place(x = 80, y = 155,anchor="center")

if __name__ == '__main__':
    
    GUI.mainloop()

    
    