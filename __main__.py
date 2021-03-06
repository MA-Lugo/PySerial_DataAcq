import time
import threading
from colors import * 
from tkinter import *
from tkinter import ttk
import serial
import webbrowser

class Channel:
    name = "Variable"
    value = 0
    oneequalto = 1.0
    max  = 1023

ch1 = Channel()
ch2 = Channel()
ch3 = Channel()
ch_def = Channel()
ch_def.name = "My Name"

GUI = Tk()
GUI.title("Serial Data Acquisition")
GUI.configure(bg = bg_color) 
GUI.geometry('470x186')
GUI.resizable(width=False, height=False)
# Gets both half the screen width/height and window width/height
positionRight = int(GUI.winfo_screenwidth()/2 - 470/2)
positionDown = int(GUI.winfo_screenheight()/2 - 186/2)
# Positions the window in the center 
GUI.geometry("+{}+{}".format(positionRight, positionDown))

connection_status = False
refresh_rate = 40 ## 40Hz

def Create_SetWindow():
    settingsWindow = Toplevel(GUI) 
    settingsWindow.title("Settings") 
    settingsWindow.geometry("240x180") 
    settingsWindow.configure(bg = bg_color) 
    settingsWindow.resizable(width=False, height=False)
    # Gets both half the screen width/height and window width/height
    positionRight = int(settingsWindow.winfo_screenwidth()/2 - 240/2)
    positionDown = int(settingsWindow.winfo_screenheight()/2 - 180/2)
    # Positions the window in the center 
    settingsWindow.geometry("+{}+{}".format(positionRight, positionDown))

    
    global ch_option
    #############################RADIO BUTTONS#################################
    ch_option = IntVar()
    Radiobutton(settingsWindow,font=("",11),text = "CH1",width=5, variable = ch_option, value = 1,bg = bg_color,fg = blue_color,
                activebackground= red_color,activeforeground= label_color).place(x = 120-80, y = 10,anchor="center")

    Radiobutton(settingsWindow,font=("",11),text = "CH2",width=5, variable = ch_option, value = 2,bg = bg_color,fg = blue_color,
                activebackground= blue_color,activeforeground= label_color).place(x = 120, y = 10,anchor="center")

    Radiobutton(settingsWindow,font=("",11),text = "CH3",width=5, variable = ch_option, value = 3,bg = bg_color,fg = blue_color,
                activebackground= yellow_color,activeforeground= bg_color).place(x = 120+80, y = 10,anchor="center")

    ###########################LABELS##########################################
    Label(settingsWindow,text = "Name:",font =("",10),justify= "right",bg = bg_color,fg = label_color).place(x = 15, y =30)
    Label(settingsWindow,text = "1 Equal to:",font =("",10),justify= "right",bg = bg_color,fg = label_color).place(x = 15, y =60)
    Label(settingsWindow,text = "Bar max.\nResolution:",font =("",10),justify= "left",bg = bg_color,fg = label_color).place(x = 15, y =90)

    ################################ENTRYS#######################################
    global CH_name
    CH_name = Entry(settingsWindow, width = 15,bg = gray_color, fg = label_color, justify = "center")
    CH_name.insert(INSERT,ch_def.name)
    CH_name.place(x = 120, y = 30)
    global CH_equ
    CH_equ = Entry(settingsWindow, width = 15,bg = gray_color, fg = label_color, justify = "center")
    CH_equ.insert(INSERT,ch_def.oneequalto)
    CH_equ.place(x = 120, y = 60)
    global CH_max
    CH_max = Entry(settingsWindow, width = 15,bg = gray_color, fg = label_color, justify = "center")
    CH_max.insert(INSERT,ch_def.max)
    CH_max.place(x = 120, y = 100)

    ###################################BUTTON###################################
    ok_button = Button(settingsWindow,text = "Apply",width = 8,command = SetCH,bg=blue_color,fg =label_color)
    ok_button.place(x = 120, y = 150,anchor="center")

def SetCH():
    option = ch_option.get()

   
    if(option == 1):
        if(len(CH_name.get()) <=14):
            ch1.name    = CH_name.get()
        ch1.oneequalto = float(CH_equ.get())
        ch1.max     = CH_max.get()
    if(option == 2):
        if(len(CH_name.get()) <=14):
            ch2.name    = CH_name.get()
        ch2.oneequalto = float(CH_equ.get())
        ch2.max     = CH_max.get()
    if(option == 3):
        if(len(CH_name.get()) <=14):
            ch3.name    = CH_name.get()
        ch3.oneequalto = float(CH_equ.get())
        ch3.max     = CH_max.get()

def Go2Info():
     webbrowser.open("https://github.com/MA-Lugo/PySerial_DataAcq")


menubar = Menu (GUI)
GUI.config(menu = menubar)
settingsmenu = Menu(menubar,tearoff=0,activebackground= bg_color,activeforeground = label_color)
menubar.add_cascade(label="Settings", menu=settingsmenu)

settingsmenu.add_command(label="Channels",command =Create_SetWindow)
settingsmenu.add_separator()
settingsmenu.add_command(label="Salir", command=GUI.quit)

helpmenu = Menu(menubar,tearoff=0,activebackground= red_color,activeforeground = label_color)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About",command =Go2Info)

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

    while(1):
        time.sleep(0.1) #delay for do not overload the CPU
        while(connection_status):
            try:
                serial_input = serial_object.readline()
                if(len(serial_input) == 12 and serial_input[0] == 0x24 ): #12bytes and "$" Start frame
                    if(serial_input[1] == 0x44 and serial_input[2] == 0x41 and serial_input[3] == 0x51):##header req "DAQ"

                        v1 = [serial_input[5], serial_input[4]]
                        ch1.value = int.from_bytes(v1,byteorder = 'big')

                        v2 = [serial_input[7], serial_input[6]]
                        ch2.value = int.from_bytes(v2,byteorder = 'big')
                        
                        v3 = [serial_input[9], serial_input[8]]
                        ch3.value = int.from_bytes(v3,byteorder = 'big')
                
                
            except:
                print("Connection Error")
                ConnectionEnd()

def UpdateGUI():
    global connection_status

    while(1):
        time.sleep(1/refresh_rate)



        while(connection_status):
            time.sleep(1/refresh_rate)
            
            item_name1.set(ch1.name)
            item_name2.set(ch2.name)
            item_name3.set(ch3.name)

            pbar1.config(max = ch1.max)
            pbar2.config(max = ch2.max)
            pbar3.config(max = ch3.max)


            if(ch1.oneequalto == 1.0):
                input1.set(str(ch1.value))
                pbar1["value"] = ch1.value
            else:
                input1.set(str(round(ch1.value*ch1.oneequalto,2)))
                pbar1["value"] = ch1.value


            if(ch2.oneequalto == 1.0):
                input2.set(str(ch2.value))
                pbar2["value"] = ch2.value
            else:
                input2.set(str(round(ch2.value*ch2.oneequalto,2)))
                pbar2["value"] = ch2.value

            if(ch3.oneequalto == 1.0):
                input3.set(str(ch3.value))
                pbar3["value"] = ch3.value
            else:
                input3.set(str(round(ch3.value*ch3.oneequalto,2)))
                pbar3["value"] = ch3.value







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


pbar1 = ttk.Progressbar(style = "red.Horizontal.TProgressbar",orient = HORIZONTAL, mode = 'determinate', length = 130, max = ch1.max)
pbar1.place(x = 80, y = 110, anchor = "center")
pbar1["value"] = ch1.value

pbar2 = ttk.Progressbar(style = "blue.Horizontal.TProgressbar",orient = HORIZONTAL, mode = 'determinate', length = 130, max = ch2.max)
pbar2.place(x = 80+155, y = 110, anchor = "center")
pbar2["value"] = ch2.value

pbar3 = ttk.Progressbar(style = "yellow.Horizontal.TProgressbar",orient = HORIZONTAL, mode = 'determinate', length = 130, max = ch3.max)
pbar3.place(x = 80+155+155, y = 110, anchor = "center")
pbar3["value"] = ch3.value

#VARIABLE LABELS
item_name1   = StringVar()
item_name1.set(ch1.name)
Label(textvariable = item_name1,font =("", 11),bg = bg_color,fg = label_color).place(x = 80, y= 20,anchor= "center")

item_name2   = StringVar()
item_name2.set(ch2.name)
Label(textvariable = item_name2,font =("", 11),bg = bg_color,fg = label_color).place(x = 80+155, y= 20,anchor= "center")

item_name3   = StringVar()
item_name3.set(ch3.name)
Label(textvariable = item_name3,font =("", 11),bg = bg_color,fg = label_color).place(x = 80+155+155, y= 20,anchor= "center")


input1   = StringVar()
input1.set(str(ch1.value))
Label(textvariable = input1,font =("", 25),bg = bg_color,fg = label_color).place(x = 80, y= 65,anchor= "center")

input2   = StringVar()
input2.set(str(ch2.value))
Label(textvariable = input2,font =("", 25),bg = bg_color,fg = label_color).place(x = 80+155, y= 65,anchor= "center")

input3   = StringVar()
input3.set(str(ch3.value))
Label(textvariable = input3,font =("", 25),bg = bg_color,fg = label_color).place(x = 80+155+155, y= 65,anchor= "center")


#BUTTONS

control_button = Button(text = "R U N",font = ("",7),width = 12,command = CTRLButton_Handle,bg=blue_color,fg =label_color)
control_button.place(x = 80, y = 155,anchor="center")

myThread1 = threading.Thread(target = UpdateGUI)
myThread1.daemon = True
myThread1.start()   

myThread2 = threading.Thread(target = SerialDataAcq)
myThread2.daemon = True
myThread2.start()   

if __name__ == '__main__':
    
    GUI.mainloop()

    
    