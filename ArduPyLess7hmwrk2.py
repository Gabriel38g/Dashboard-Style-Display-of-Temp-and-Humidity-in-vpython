from vpython import *
import numpy as np
import time
import serial
scene= canvas(width=900, height=500, title='Meter Store')
arduinoData=serial.Serial('/dev/ttyACM0', 115200) ##Change to port on your computer!
time.sleep(1)

tempaxle=(-2.5)
voltaxle=2.5
humidaxle=(0)

arrowL=1
arrowT=.02
pntT=.04
bRadius=.1
x=0 # integer to make spheres for seconds, minutes, hours

temparrow=arrow(pos=vector(tempaxle, 1,0),  color=color.red, shaftwidth=arrowT)
tempBall=sphere(radius=bRadius,  color=color.red,  pos=vector(arrowL, 0, 0))
templab = label(text = 'Temp C', pos=vector(tempaxle, 0,0))

humidarrow=arrow(axis=vector(0, 1, 0),  color=color.green, Length=arrowL,  shaftwidth=arrowT)
humidlab = label(text = 'Humidity %', pos = vector(humidaxle,0,0))

voltBall=sphere(radius=bRadius,  color=color.red,  pos=vector(arrowL, 0, 0))
voltlab=label(text='5', pos=vector(voltaxle,0,0))

tempballarray= [x]

for myAngle in np.linspace(0, 1*np.pi, 31):
    if x in [5, 10, 20, 25, 35, 40, 50, 55]:
        # medium balls for minutes
        tempballarray[x]=sphere(radius=.02,  color=color.red,  pos=vector(tempaxle+arrowL*cos(myAngle), arrowL*np.sin(myAngle), 0))
    if x in [0, 15, 30, 45]:
        # lerger radius balls for hours
        tempballarray[x]=sphere(radius=.04,  color=color.red,  pos=vector(tempaxle+arrowL*cos(myAngle), arrowL*np.sin(myAngle), 0))
    else:
        #small balls for seconds
        tempballarray[x]=sphere(radius=.01,  color=color.red,  pos=vector(tempaxle+arrowL*cos(myAngle), arrowL*np.sin(myAngle), 0))
    x = x +1
    tempballarray.append(x)
sleep(5)

x =0

humidballarray= [x]

for newAngle in np.linspace(0, 2*np.pi, 61):
    if x in [5, 10, 20, 25, 35, 40, 50, 55]:
        # medium balls for minutes
        humidballarray[x]=sphere(radius=.03,  color=color.green,  pos=vector(arrowL*cos(newAngle), arrowL*np.sin(newAngle), 0))
    if x in [0, 15, 30, 45]:
        # lerger radius balls for hours
        humidballarray[x]=sphere(radius=.04,  color=color.green,  pos=vector(arrowL*cos(newAngle), arrowL*np.sin(newAngle), 0))
    else:
        #small balls for seconds
        humidballarray[x]=sphere(radius=.02,  color=color.green,  pos=vector(arrowL*cos(newAngle), arrowL*np.sin(newAngle), 0))
    x = x +1
    humidballarray.append(x)
sleep(5)

humidballscount=x

x =0

voltballarray= [x]

for newAngle in np.linspace(0, 1*np.pi, 31):
    if x in [5, 10, 20, 25, 35, 40, 50, 55]:
        # medium balls for minutes
        voltballarray[x]=sphere(radius=.02,  color=color.yellow,  pos=vector(voltaxle+arrowL*cos(newAngle), arrowL*np.sin(newAngle), 0))
    if x in [0, 15, 30, 45]:
        # lerger radius balls for hours
        voltballarray[x]=sphere(radius=.04,  color=color.yellow,  pos=vector(voltaxle+arrowL*cos(newAngle), arrowL*np.sin(newAngle), 0))
    else:
        #small balls for seconds
        voltballarray[x]=sphere(radius=.01,  color=color.yellow,  pos=vector(voltaxle+arrowL*cos(newAngle), arrowL*np.sin(newAngle), 0))
    x = x +1
    voltballarray.append(x)
sleep(5)

slab=label(pos=tempballarray[0].pos, text='30')
olab=label(pos=tempballarray[x-1].pos, text='0')
x=0



point = 0

while True:
    while(arduinoData.inWaiting()==0):
        pass
    dataPacket=arduinoData.readline()
    dataPacket=str(dataPacket,'utf-8')
    dataPacket=dataPacket.strip('\r\s\n')
    if dataPacket!='':
        if dataPacket == 'C':
            tempval = float(arduinoData.readline())
            templab.text = str(tempval) + 'C'
            tpos = int(30-tempval)
            tempBall.pos=(tempballarray[tpos].pos)
            temparrow.axis = vector(templab.pos-tempballarray[tpos].pos)#(tempaxle+arrowL,0,0)
            temparrow.pos=vector(tempballarray[tpos].pos)
        if dataPacket == 'V':
            potVal=int(arduinoData.readline())
            vol=(5./1023.)*potVal
            vol=round(vol,1)
            if vol == 0:
                vol=0.1
            point = int(round(31-(vol*6),0))
            voltlab.text=str(vol)
            voltBall.pos=vector(voltballarray[point].pos)
        if dataPacket == 'H':
            humidval = float(arduinoData.readline())
            hpos = int(60*(humidval/100))
            humidarrow.axis=humidballarray[hpos].pos
            humidlab.text=str(humidval)+ '%'
            #humidlab.text=str(hpos)
            while x < humidballscount:
                if x < hpos:
                    humidballarray[x].color=color.green
                else:
                    humidballarray[x].color=color.magenta
                x=x+1
    else:
        pass

    if point > 22:
        voltBall.color = color.yellow
    if point < 22:
        voltBall.color = color.green
    if point < 10:
        voltBall.color = color.red

