#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Frame, StringVar, Label
import tkFont

class ResultsWindow(Frame):

  def __init__(self, parent, results):
    Frame.__init__(self, parent)
    
    self.lettersToDisplay = results
    self.parent = parent
    self.initUI()

    
    
  def initUI(self):
    self.parent.title("Hand Sign Recognition")

    font = tkFont.Font(family="Helvetica", size=100)

    labelStrVar = StringVar()
    label = Label( self.parent, textvariable=labelStrVar, font=font)

    labelStrVar.set("K-Means"+"\n"+self.lettersToDisplay["Kmeans"]+"\n")
    label.pack()

    labelStrVarNN = StringVar()
    labelNN = Label( self.parent, textvariable=labelStrVarNN, font=font)

    labelStrVarNN.set("Neural Nets \n"+self.lettersToDisplay["NN"])
    labelNN.pack()