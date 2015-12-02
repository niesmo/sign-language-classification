#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import Frame, StringVar, Label
import tkFont

class ResultsWindow(Frame):

  def __init__(self, parent, letter):
    Frame.__init__(self, parent)
    
    self.letterToDisplay = letter
    self.parent = parent
    self.initUI()

    
    
  def initUI(self):
    self.parent.title("Hand Sign Recognition")

    font = tkFont.Font(family="Helvetica", size=200)

    self.labelStrVar = StringVar()
    self.label = Label( self.parent, textvariable=self.labelStrVar, font=font)

    self.labelStrVar.set(self.letterToDisplay)
    self.label.pack()