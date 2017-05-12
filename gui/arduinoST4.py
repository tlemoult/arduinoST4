#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#python 2.7
# require http://pyserial.sourceforge.net/shortintro.html

import Tkinter
import serial
import time,math,sys

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        
        self.initialize()

    def handler(self):
        print "handler bye"
        print "closing serial port"
        self.ser.close()
        self.quit()

    def initialize(self):
        print "GUI for arduino ST4"

        #grap argument on command line
        nbArgs=len(sys.argv)
        if nbArgs==1:
            print "Syntaxe:"
            print "  python arduinoST4.py COM3"
            exit()
        elif nbArgs!=2:
            print "bad argument count."
            exit()

        # serial port
        print "open serial port: ",
        com=sys.argv[1]
        if com[0:3]=='COM':
            # run on windows
            comName=int(com[3:])-1
            print "  Port COM"+str(comName+1)
        else:
            #run on linux like OS.
            comName=com
            print "  Port Dev: "+comName

        self.ser = serial.Serial(comName,9600,timeout=1)

        #initialize GUI            
        self.protocol("WM_DELETE_WINDOW", self.handler)
        self.grid()

        # boutons deplacement manuel raquette
        buttonAon = Tkinter.Button(self,text=u"North")
        buttonAon.bind("<Button-1>",self.OnButtonClickA)
        buttonAon.bind("<ButtonRelease-1>",self.OffButton)
        buttonAon.grid(column=4,row=0,columnspan=1,sticky='EW')

        buttonBon = Tkinter.Button(self,text=u"East")
        buttonBon.bind("<Button-1>",self.OnButtonClickB)
        buttonBon.bind("<ButtonRelease-1>",self.OffButton)
        buttonBon.grid(column=3,row=1,columnspan=1,sticky='EW')

        buttonCon = Tkinter.Button(self,text=u"West")
        buttonCon.bind("<Button-1>",self.OnButtonClickC)
        buttonCon.bind("<ButtonRelease-1>",self.OffButton)
        buttonCon.grid(column=5,row=1,columnspan=1,sticky='EW')

        buttonDon = Tkinter.Button(self,text=u"South")
        buttonDon.bind("<Button-1>",self.OnButtonClickD)
        buttonDon.bind("<ButtonRelease-1>",self.OffButton)
        buttonDon.grid(column=4,row=2,columnspan=1,sticky='EW')

        buttonReturn = Tkinter.Button(self,text=u"Back",command=self.OnButtonReturn)
        buttonReturn.grid(column=4,row=1,columnspan=1,sticky='EW')
    

        # La colonne de droite avec les reglages
        labelPixelSize = Tkinter.Label(self,text="Taille\nPhotosite\n(µm)",anchor="w",fg="white",bg="black")
        labelPixelSize.grid(column=0,row=4,columnspan=1,sticky='EW')
        self.ePixelSize=Tkinter.Entry(self,width=6)
        self.ePixelSize.insert(0, '9')
        self.ePixelSize.grid(column=2,row=4)

        labelPixelSize = Tkinter.Label(self,text="Focale\n(mm)",anchor="w",fg="black",bg="white")
        labelPixelSize.grid(column=0,row=5,columnspan=1,sticky='EW')
        self.eFocale=Tkinter.Entry(self,width=6)
        self.eFocale.insert(0, '830')
        self.eFocale.grid(column=2,row=5)

        labelPixelSize = Tkinter.Label(self,text="Ratio\nsideral\n(x)",anchor="w",fg="white",bg="black")
        labelPixelSize.grid(column=0,row=6,columnspan=1,sticky='EW')
        self.eSideral=Tkinter.Entry(self,width=6)
        self.eSideral.insert(0, '1')
        self.eSideral.grid(column=2,row=6)

        labelPixelSize = Tkinter.Label(self,text="Dec\n(degre)",anchor="w",fg="black",bg="white")
        labelPixelSize.grid(column=0,row=7,columnspan=1,sticky='EW')
        self.eDec=Tkinter.Entry(self,width=6)
        self.eDec.insert(0, '0')
        self.eDec.grid(column=2,row=7)


        self.decReverse= Tkinter.IntVar()
        decReverseButton= Tkinter.Checkbutton(self,text="Rev\nDec",variable=self.decReverse)
        decReverseButton.grid(column=8,row=1)

        #deplacement en pixel
        labelASSpace = Tkinter.Label(self,text="--------",anchor="w",fg="lightgrey",bg="lightgrey")
        labelASSpace.grid(column=7,row=4,columnspan=1,sticky='EW')
        labelADTitle = Tkinter.Label(self,text="AD(Pixel)",anchor="w",fg="white",bg="grey")
        labelADTitle.grid(column=8,row=4,columnspan=1,sticky='EW')
        labelASSpace = Tkinter.Label(self,text="----",anchor="w",fg="lightgrey",bg="lightgrey")
        labelASSpace.grid(column=9,row=4,columnspan=1,sticky='EW')
        labelDecTitle = Tkinter.Label(self,text="DEC(Pixel)",anchor="w",fg="white",bg="grey")
        labelDecTitle.grid(column=10,row=4,columnspan=1,sticky='EW')

        buttonMoveAlpha = Tkinter.Button(self,text=u"Go",command=self.OnButtonMoveAlpha)
        buttonMoveAlpha.grid(column=8,row=6,columnspan=1,sticky='EW')
        buttonModeDelta = Tkinter.Button(self,text=u"Go",command=self.OnButtonMoveDelta)
        buttonModeDelta.grid(column=10,row=6,columnspan=1,sticky='EW')
        
        self.eMoveAlpha = Tkinter.Entry(self,width=6)
        self.eMoveAlpha.insert(0, '0')
        self.eMoveAlpha.grid(column=8,row=5)

        self.eMoveDelta = Tkinter.Entry(self,width=6)
        self.eMoveDelta.insert(0,'0')
        self.eMoveDelta.grid(column=10,row=5)


        #message information
        self.labelInfo = Tkinter.Label(self,text="",anchor="w")
        self.labelInfo.grid(column=8,row=7,columnspan=3,rowspan=4)

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()

        time.sleep(1)
        self.geometry(self.geometry())       

    def CalcMs(self,D,delta):
        p=float(self.ePixelSize.get())
        f=float(self.eFocale.get())
        R=float(self.eSideral.get())
        return int(1000*206.0*D*p/(15*f*R*math.cos(delta*3.1415/180.0)))

    def OnButtonReturn(self):
        self.logMsg("Return origin")
        self.ser.write("R\n")
        self.ser.flush()

    def OnButtonMoveAlpha(self):
        ms=self.CalcMs(float(self.eMoveAlpha.get()),float(self.eDec.get()))
        self.logMsg('AD move '+str(ms)+' ms')
        if (ms>0):
            self.ser.write("E"+str(abs(ms))+"\n")
        else:
            self.ser.write("W"+str(abs(ms))+"\n")
        self.ser.flush()
        
    def OnButtonMoveDelta(self):
        ms=self.CalcMs(float(self.eMoveDelta.get()),0)
        if (self.decReverse.get()==1):
            ms=-ms
            print "dec Reversed"
        self.logMsg("Dec move "+str(ms)+" ms")
        if (ms>0):
            self.ser.write("N"+str(abs(ms))+"\n")
        else:
            self.ser.write("S"+str(abs(ms))+"\n")
        self.ser.flush()

    def OffButton(self,event):
        self.logMsg("Button release\nMove stop")
        self.ser.write("T\n")
        self.ser.flush()

    def OnButtonClickA(self,event):
        self.logMsg("Moving north")
        if (self.decReverse.get()==1):
            print "dec Reversed"
            self.ser.write("s\n")
        else:
            self.ser.write("n\n")
        self.ser.flush()

    def OnButtonClickD(self,event):
        self.logMsg("Moving south")
        if (self.decReverse.get()==1):
            print "dec Reversed"
            self.ser.write("n\n")
        else:
            self.ser.write("s\n")
        self.ser.flush()

    def OnButtonClickB(self,event):
        self.logMsg("Moving east")
        self.ser.write("e\n")
        self.ser.flush()
    def OnButtonClickC(self,event):
        self.logMsg("Moving west")
        self.ser.write("w\n")
        self.ser.flush()

    def logMsg(self,msg):
        print msg
        self.labelInfo.config(text=msg)
        self.update()

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('arduino ST4, v1.01 2017')
    
    app.mainloop()
    print("main bye")
    app.destroy()
    del app

