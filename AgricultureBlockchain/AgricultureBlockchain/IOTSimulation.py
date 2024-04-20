import tkinter
from tkinter import *
import math
import random
from threading import Thread 
from collections import defaultdict
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import time
from tkinter import simpledialog
from Block import *
from Blockchain import *
import datetime
import os

global mobile
global labels
global mobile_x
global mobile_y
global text
global canvas
global mobile_list
global filename
global mcen1,mcen2,mcen3
global line1,line2,line3
execution_time = []
option = 0
global root

global crop_growth_details

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def calculateShortestDistance(iot_x,iot_y,x1,y1):
    flag = False
    for i in range(len(iot_x)):
        dist = math.sqrt((iot_x[i] - x1)**2 + (iot_y[i] - y1)**2)  # Calculate the Euclidean distance between (iot_x[i], iot_y[i]) and (x1, y1)
        if dist < 80:  # dist less than 80
            flag = True
            break
    return flag

    
def startDataTransferSimulation(text,canvas,line1,line2,line3,x1,y1,x2,y2,x3,y3):
    class SimulationThread(Thread):
        def __init__(self,text,canvas,line1,line2,line3,x1,y1,x2,y2,x3,y3): 
            Thread.__init__(self) 
            self.canvas = canvas
            self.line1 = line1
            self.line2 = line2
            self.line3 = line3
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.x3 = x3
            self.y3 = y3
            self.text = text
            
 
        def run(self):
            time.sleep(1)
            for i in range(0,3):
                self.canvas.delete(self.line1)
                self.canvas.delete(self.line2)
                self.canvas.delete(self.line3)
                time.sleep(1)
                self.line1 = canvas.create_line(self.x1, self.y1,self.x2, self.y2,fill='black',width=3)
                self.line2 = canvas.create_line(self.x2, self.y2,self.x3, self.y3,fill='black',width=3)
                self.line3 = canvas.create_line(self.x3, self.y3,25, 370,fill='black',width=3)
                time.sleep(1)
            self.canvas.delete(self.line1)
            self.canvas.delete(self.line2)
            self.canvas.delete(self.line3)
            canvas.update()
                
    newthread = SimulationThread(text,canvas,line1,line2,line3,x1,y1,x2,y2,x3,y3) 
    newthread.start()
    
    
def generate():
    global mobile
    global labels
    global mobile_x
    global mobile_y
    mobile = []
    mobile_x = []
    mobile_y = []
    labels = []
    canvas.update()
    x = 5
    y = 350
    mobile_x.append(x)
    mobile_y.append(y)
    name = canvas.create_oval(x,y,x+40,y+40, fill="blue")
    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text="Base Station")
    labels.append(lbl)
    mobile.append(name)

    for i in range(1,20):
        run = True
        while run == True:
            x = random.randint(100, 450)
            y = random.randint(50, 600)
            flag = calculateShortestDistance(mobile_x,mobile_y,x,y)
            if flag == False:
                mobile_x.append(x)
                mobile_y.append(y)
                run = False
                name = canvas.create_oval(x,y,x+40,y+40, fill="red")
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 8 italic bold",text="IOT "+str(i))
                labels.append(lbl)
                mobile.append(name)
    

def CHSelection():
    text.delete('1.0', END)
    global mcen1,mcen2,mcen3
    distance = 10000
    for i in range(1,20):
        x1 = mobile_x[i]
        y1 = mobile_y[i]
        energy_consumption = math.sqrt((x1 - 5)**2 + (y1 - 350)**2)
        if energy_consumption < distance and y1 > 5 and y1 < 200:
            distance = energy_consumption
            mcen1 = i
    print(distance)        
    distance = 10000
    for i in range(1,20):
        x1 = mobile_x[i]
        y1 = mobile_y[i]
        energy_consumption = math.sqrt((x1 - 5)**2 + (y1 - 350)**2)  #Euclidean distance from a base station at (5, 350)
        if energy_consumption < distance and i != mcen1 and y1 > 250 and y1 <= 350 :
            distance = energy_consumption
            mcen2 = i
    print(distance)
    distance = 10000
    for i in range(1,20):
        x1 = mobile_x[i]
        y1 = mobile_y[i]
        energy_consumption = math.sqrt((x1 - 5)**2 + (y1 - 350)**2)
        if energy_consumption < distance and i != mcen1 and i != mcen2 and y1 > 450 and y1 < 650:
            distance = energy_consumption
            mcen3 = i
    print(distance)
    #calculations to select three cluster heads (mcen1, mcen2, mcen3) based on their proximity to a base station located at coordinates (5, 350) on a canvas. It then updates the appearance of the selected cluster heads on the canvas by changing their color to green and updating their labels.            
    text.insert(END,"Selected CH 1 is : "+str(mcen1)+"\n")
    text.insert(END,"Selected CH 2 is : "+str(mcen2)+"\n")
    text.insert(END,"Selected CH 3 is : "+str(mcen3)+"\n")
    canvas.delete(mobile[mcen1])
    canvas.delete(mobile[mcen2])
    canvas.delete(mobile[mcen3])
    canvas.delete(labels[mcen1])
    canvas.delete(labels[mcen2])
    canvas.delete(labels[mcen3])
    # Create green circles for the selected cluster heads
    name = canvas.create_oval(mobile_x[mcen1],mobile_y[mcen1],mobile_x[mcen1]+40,mobile_y[mcen1]+40, fill="green")
    mobile[mcen1] = name
    name = canvas.create_oval(mobile_x[mcen2],mobile_y[mcen2],mobile_x[mcen2]+40,mobile_y[mcen2]+40, fill="green")
    mobile[mcen2] = name
    name = canvas.create_oval(mobile_x[mcen3],mobile_y[mcen3],mobile_x[mcen3]+40,mobile_y[mcen3]+40, fill="green")
    # Create labels for the selected cluster heads
    mobile[mcen3] = name
    lbl = canvas.create_text(mobile_x[mcen1]+20,mobile_y[mcen1]-10,fill="green",font="Times 10 italic bold",text="CH1-"+str(mcen1))
    labels[mcen1] = lbl
    lbl = canvas.create_text(mobile_x[mcen2]+20,mobile_y[mcen2]-10,fill="green",font="Times 10 italic bold",text="CH2-"+str(mcen2))
    labels[mcen2] = lbl
    lbl = canvas.create_text(mobile_x[mcen3]+20,mobile_y[mcen3]-10,fill="green",font="Times 10 italic bold",text="CH3-"+str(mcen3))
    labels[mcen3] = lbl

    canvas.create_oval(50,5,500,245)
    canvas.create_oval(50,240,500,450)
    canvas.create_oval(50,430,500,670)
    
    canvas.update()

def collectData():
    global crop_growth_details
    crop_growth_details = simpledialog.askstring("Please Enter Crop Growth Details", "Please Enter Crop Growth Details")

def dataTansmission():   #The dataTansmission function appears to simulate data transmission in a network of IoT devices. It selects a source node (src) and finds the shortest path to a specific destination node (hop). Additionally, it determines a gateway node (gateway) based on the distance to three cluster heads (mcen1, mcen2, mcen3). The function then updates a text widget (text) with information and draws lines on a canvas (canvas) to represent the transmission path.
    global crop_growth_details
    global option
    global line1,line2,line3
    text.delete('1.0', END)
    src = int(mobile_list.get())
    now = datetime.datetime.now()    
    if option == 1:
        canvas.delete(line1)
        canvas.delete(line2)
        canvas.delete(line3)
        canvas.update()
    src_x = mobile_x[src]
    src_y = mobile_y[src]
    distance = 10000
    #If a shortest path (hop) is found, selects a gateway node based on its distance to the three cluster heads (mcen1, mcen2, mcen3).
    hop = 0
    gateway = 0
    for i in range(1,20):
        temp_x = mobile_x[i]
        temp_y = mobile_y[i]
        if i != src and i != mcen1 and i != mcen2 and i != mcen3 and temp_x < src_x:
            dist = math.sqrt((src_x - temp_x)**2 + (src_y - temp_y)**2)
            if dist < distance:
                distance = dist
                hop = i
    if hop != 0:
        hop_x = mobile_x[hop]
        hop_y = mobile_y[hop]
        distance1 = math.sqrt((hop_x - mobile_x[mcen1])**2 + (hop_y - mobile_y[mcen1])**2)
        distance2 = math.sqrt((hop_x - mobile_x[mcen2])**2 + (hop_y - mobile_y[mcen2])**2)
        distance3 = math.sqrt((hop_x - mobile_x[mcen3])**2 + (hop_y - mobile_y[mcen3])**2)
        if distance1 <= distance2 and distance1 <= distance3:
            gateway = mcen1
        elif distance2 <= distance1 and distance2 <= distance3:
            gateway = mcen2
        else:
            gateway = mcen3
    #If both a gateway and a shortest path are found, updates the text widget with information and draws lines on the canvas.
    if gateway != 0 and hop != 0:
        text.insert(END,"Selected Source Node is : "+str(src)+"\n")
        text.insert(END,"Selected Shortest Path Node with less energy Consumption is : "+str(hop)+"\n")
        text.insert(END,"Selected Nearest CH is : "+str(gateway)+"\n")
        line1 = canvas.create_line(mobile_x[src]+20, mobile_y[src]+20,mobile_x[hop]+20, mobile_y[hop]+20,fill='black',width=3)
        line2 = canvas.create_line(mobile_x[hop]+20, mobile_y[hop]+20,mobile_x[gateway]+20, mobile_y[gateway]+20,fill='black',width=3)
        line3 = canvas.create_line(mobile_x[gateway]+20, mobile_y[gateway]+20,mobile_x[0]+20, mobile_y[0]+20,fill='black',width=3)
        startDataTransferSimulation(text,canvas,line1,line2,line3,(mobile_x[src]+20),(mobile_y[src]+20),(mobile_x[hop]+20),(mobile_y[hop]+20),(mobile_x[gateway]+20),(mobile_y[gateway]+20))
        option = 1
        data = "IOT_ID : "+str(src)+"#"+crop_growth_details+"#"+str(now)
        blockchain.add_new_transaction(data)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        text.insert(END,"Blockchain Previous Hash : "+str(b.previous_hash)+"\nBlock No : "+str(b.index)+"\nCurrent Hash : "+str(b.hash)+"\n")
        text.insert(END,"Details saved in blockchain\n\n")
        blockchain.save_object(blockchain,'blockchain_contract.txt')
        
    else:
        text.insert(END,"No shortest path node found. Try another source\n")
            


def viewData():  #he viewData function appears to retrieve and display data from the blockchain related to a specific IoT device
    text.delete('1.0', END)
    #The code then iterates through each block in the blockchain, starting from the second block (genesis block is skipped).
    src = mobile_list.get()
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            temp = arr[0].split(":")
            if temp[1].strip() == src:
                text.insert(END,"IOT ID        : "+temp[1]+"\n")
                text.insert(END,"Crop Details  : "+arr[1]+"\n")
                text.insert(END,"Date Time     : "+arr[2]+"\n")
                text.insert(END,"Blockchain Storage Hashcode     : "+str(b.hash)+"\n\n")
                
    
def Main():
    global root
    global tf1
    global text
    global canvas
    global mobile_list
    root = tkinter.Tk()
    root.geometry("1300x1200")
    root.title("BLOCKCHAIN TECHNOLOGY  FOR AGRICULTURAL SUPPLY CHAIN")
    root.resizable(True,True)
    font1 = ('times', 12, 'bold')

    canvas = Canvas(root, width = 800, height = 700)
    canvas.pack()

    l1 = Label(root, text='IOT ID:')
    l1.config(font=font1)
    l1.place(x=820,y=10)

    mid = []
    for i in range(1,20):
        mid.append(str(i))
    mobile_list = ttk.Combobox(root,values=mid,postcommand=lambda: mobile_list.configure(values=mid))
    mobile_list.place(x=970,y=10)
    mobile_list.current(0)
    mobile_list.config(font=font1)

    createButton = Button(root, text="Generate IOT Network", command=generate)
    createButton.place(x=820,y=60)
    createButton.config(font=font1)

    initButton = Button(root, text="Cluster Head Selection", command=CHSelection)
    initButton.place(x=820,y=110)
    initButton.config(font=font1)

    algButton = Button(root, text="Collect Data", command=collectData)
    algButton.place(x=820,y=160)
    algButton.config(font=font1)

    graphButton = Button(root, text="Data Transmission Routing Phase", command=dataTansmission)
    graphButton.place(x=820,y=210)
    graphButton.config(font=font1)

    exitButton = Button(root, text="View Blockchain Data", command=viewData)
    exitButton.place(x=820,y=260)
    exitButton.config(font=font1)

    text=Text(root,height=20,width=60)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=820,y=310)
    
    
    root.mainloop()
   
 
if __name__== '__main__' :
    Main ()
    
