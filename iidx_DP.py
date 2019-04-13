# -*- coding: utf-8 -*-
#!/usr/bin/env python

from Score_DP import Score

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer, QThread, QUrl)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QLinearGradient, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, 
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QSlider, QFileDialog, QSizePolicy)

import os
import re

folderDict = {
    "1":"01_1st_style",
    "s":"01_substream",
    "2":"02_2nd_style",
    "3":"03_3rd_style",
    "4":"04_4th_style",
    "5":"05_5th_style",
    "6":"06_6th_style",
    "7":"07_7th_style",
    "8":"08_8th_style",
    "9":"09_9th_style",
    "10":"10_10th_style",
    "11":"11_IIDX_RED",
    "12":"12_HAPPY_SKY",
    "13":"13_DistorteD",
    "14":"14_GOLD",
    "15":"15_DJ_TROOPERS",
    "16":"16_EMPRESS",
    "17":"17_SIRIUS",
    "18":"18_Resort_Anthem",
    "19":"19_Lincle",
    "20":"20_tricoro",
    "21":"21_SPADA",
    "22":"22_PENDUAL",
    "23":"23_copula",
    "24":"24_SINOBUZ",
    "25":"25_CANNON_BALLERS",
    "26":"26_Rootage",
}
    
class Display(QGraphicsItem):
    def __init__(self, width=822, height=552):
        super(Display, self).__init__()
        self.width = width
        self.height = height
        
        self.score=Score()
        
        self.keybeam = [[0, 0, 0] for _ in range(16)]
        self.notes = [[] for _ in range(16)]
        self.longNotes = [[] for _ in range(16)]
        
        self.yPhase=-512.0
        self.sudden=0.0
        self.hiSpeed=1.0
        self.speed=1.0
        self.fhs=False
        self.green=None
        
        self.isEnd=False
        self.bpm=0.0
        self.isFlip=False
        
        self.isPlaying=False
    
    def switch_isPlaying(self, isPlaying):
        self.isPlaying = isPlaying
    
    def change_style(self, playerSide, style):
        if playerSide==0:
            self.notes[0], self.notes[1:8], self.longNotes[0], self.longNotes[1:8], arrangement1 = self.score.change_style(playerSide, style)
                
        if playerSide==1:
            self.notes[15], self.notes[8:15], self.longNotes[15], self.longNotes[8:15], arrangement2 = self.score.change_style(playerSide, style)
            
        self.update_yPhase(None)
        
    def flip(self, isFlip):
        self.isFlip=isFlip 
        self.update_yPhase(None)
    
    def change_sudden(self,sudden):
        if self.fhs and self.bpm!=0:
            self.hiSpeed=(1000-sudden)/self.green/self.bpm/self.speed
            if self.hiSpeed<0.50:
                self.hiSpeed=0.50
            elif self.hiSpeed>10.00:
                self.hiSpeed=10.00
        self.sudden=sudden
        self.update_yPhase(None)
            
    def change_hiSpeed(self, isMinus):
        if self.fhs:
            if isMinus:
                self.hiSpeed-=0.50
                if self.hiSpeed<0.50:
                    self.hiSpeed=0.50
            else:
                self.hiSpeed+=0.50
                if self.hiSpeed>10.00:
                    self.hiSpeed=10.00
        else:
            if isMinus:
                if self.hiSpeed>2.00:
                    self.hiSpeed-=0.25
                elif self.hiSpeed>1.00:
                    self.hiSpeed-=0.50
            else:
                if self.hiSpeed<2.00:
                    self.hiSpeed+=0.50
                elif self.hiSpeed<4.00:
                    self.hiSpeed+=0.25
        self.update_yPhase(None)
            
    def change_speed(self,speed):
        self.speed=speed
        self.update_yPhase(None)
    
    def switch_fhs(self,isChecked):
        if isChecked:
            self.fhs=True
            if self.bpm!=0:
                self.green=(1000-self.sudden)/self.hiSpeed/self.bpm
        else:
            self.fhs=False
            if self.hiSpeed>=3.875:
                self.hiSpeed=4.00
            elif 3.625<=self.hiSpeed<3.875:
                self.hiSpeed=3.75
            elif 3.375<=self.hiSpeed<3.625:
                self.hiSpeed=3.50
            elif 3.125<=self.hiSpeed<3.375:
                self.hiSpeed=3.25
            elif 2.875<=self.hiSpeed<3.125:
                self.hiSpeed=3.00
            elif 2.625<=self.hiSpeed<2.875:
                self.hiSpeed=2.75
            elif 2.375<=self.hiSpeed<2.625:
                self.hiSpeed=2.50
            elif 2.125<=self.hiSpeed<2.375:
                self.hiSpeed=2.25
            elif 1.75<=self.hiSpeed<2.125:
                self.hiSpeed=2.00
            elif 1.25<=self.hiSpeed<1.75:
                self.hiSpeed=1.50
            elif self.hiSpeed<1.25:
                self.hiSpeed=1.00
            
        self.update_yPhase(None)
    
    def switch_isEnd(self,isEnd):
        self.isEnd=isEnd
    
    def update_yPhase(self,yPhase):
        if yPhase is not None:
            self.yPhase=yPhase
        elif self.isPlaying:
            self.yPhase+=4.0/225*self.bpm*self.speed
            if self.yPhase>=self.score.length: self.switch_isEnd(True)
        if self.score.bpm:
            self.bpm=self.score.bpm[0][1]
            for bpm in self.score.bpm:
                if bpm[0]<=self.yPhase:
                    self.bpm=bpm[1]
                else:
                    break
        
        self.update()
    
    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(63,63,63))
        painter.drawRect(0,0,self.width,self.height)
        painter.setBrush(QColor(0,0,0))
        painter.drawRect(0,0,755,542)
        painter.setBrush(QColor(23,23,23))
        painter.drawRect(70,0,39,536)
        painter.drawRect(142,0,39,536)
        painter.drawRect(214,0,39,536)
        painter.drawRect(286,0,39,536)
        painter.drawRect(430,0,39,536)
        painter.drawRect(502,0,39,536)
        painter.drawRect(574,0,39,536)
        painter.drawRect(646,0,39,536)
        painter.setBrush(QColor(127,127,127))
        painter.drawRect(69,0,1,536)
        painter.drawRect(109,0,1,536)
        painter.drawRect(141,0,1,536)
        painter.drawRect(181,0,1,536)
        painter.drawRect(213,0,1,536)
        painter.drawRect(253,0,1,536)
        painter.drawRect(285,0,1,536)
        
        painter.drawRect(469,0,1,536)
        painter.drawRect(501,0,1,536)
        painter.drawRect(541,0,1,536)
        painter.drawRect(573,0,1,536)
        painter.drawRect(613,0,1,536)
        painter.drawRect(645,0,1,536)
        painter.drawRect(685,0,1,536)
        
        displayMin=self.yPhase
        displayMax=self.yPhase+320*(1-(self.sudden/1000))/self.hiSpeed
        
        for y in self.score.barLine:
            if displayMin<=y<displayMax:
                yn=539-(y-self.yPhase)*self.hiSpeed*27/16
                painter.drawRect(2,yn,323,1)
                painter.drawRect(430,yn,323,1)
        
        painter.setBrush(QColor(255,0,0))
        painter.drawRect(2,536,323,4)
        painter.drawRect(430,536,323,4)
        
        for lane, notesOnLane in enumerate(self.notes):
            color, pos = self.setColorPos(lane)
            
            if self.keybeam[lane][0]>0: self.keybeam[lane][0]-=1
            
            keybeam_ = self.keybeam[lane][1]
            self.keybeam[lane][1] = sum(y<=displayMin for y, status in notesOnLane)
            n = self.keybeam[lane][1] - keybeam_
            keybeam_ = self.keybeam[lane][2]
            self.keybeam[lane][2] = sum(y<=displayMin and status==2 for y, status in notesOnLane)
            cne = self.keybeam[lane][2] - keybeam_
            
            cn = sum(y<=displayMin and status==1 for y, status in notesOnLane) - self.keybeam[lane][2]
            if n>0 and self.isPlaying:
                if lane in {0,15}: self.keybeam[lane][0]=8
                else:              self.keybeam[lane][0]=6
            if lane not in {0,15}:
                if cn and self.keybeam[lane][0]<4:
                    self.keybeam[lane][0]=4
                elif self.keybeam[lane][0]==4 and cne>0:
                    self.keybeam[lane][0]=3
                
            self.drawKeybeam(painter, color, pos, self.keybeam[lane][0])
        
        for lane, notesOnLane in enumerate(self.longNotes):
            color, pos = self.setColorPos(lane)
            
            for y, duration in notesOnLane:
                if displayMin-duration<=y<displayMax:
                    yn=540-(y-self.yPhase+duration)*self.hiSpeed*27/16
                    durationN=duration*self.hiSpeed*27/16
                    self.drawLongNote(painter, color, pos, yn, durationN)
                    
        
        for lane, notesOnLane in enumerate(self.notes):
            color, pos = self.setColorPos(lane)
            
            for y, status in notesOnLane:
                if displayMin<=y<displayMax:
                    yn=532-(y-self.yPhase)*self.hiSpeed*27/16
                    self.drawNote(painter, color, status, pos, yn)
        
        painter.setBrush(QColor(63,63,63))
        painter.drawRect(2,0,323,540*float(self.sudden)/1000-1)
        painter.drawRect(430,0,323,540*float(self.sudden)/1000-1)
        painter.drawRect(327,0,101,542)
        painter.setBrush(QColor(127,127,127))
        painter.drawRect(2,540*float(self.sudden)/1000-1,323,1)
        painter.drawRect(430,540*float(self.sudden)/1000-1,323,1)
        painter.drawRect(331,0,93,542)
        
        painter.setBrush(QColor(255,255,255))
        painter.drawRect(0,0,2,542)
        painter.drawRect(325,0,2,542)
        painter.drawRect(2,540,323,2)
        painter.drawRect(428,0,2,542)
        painter.drawRect(753,0,2,542)
        painter.drawRect(430,540,323,2)
        
        painter.setBrush(QColor(63,63,63))
        painter.drawRect(0,542,755,10)
        painter.setBrush(QColor(0,0,0))
        painter.drawRect(214,546,327,6)
        
        painter.setBrush(QColor(191,95,0))
        painter.drawRect(214+int(315*(512+self.yPhase)/(512+self.score.length)),546,12,6)
        painter.setBrush(QColor(223, 159, 0))
        painter.drawRect(214+int(315*(512+self.yPhase)/(512+self.score.length))+1,547,10,4)
        painter.setBrush(QColor(255,223,127))
        painter.drawRect(214+int(315*(512+self.yPhase)/(512+self.score.length))+4,547,4,4)
    
        font = painter.font()
        font.setPixelSize(24)
        painter.setFont(font)
        painter.setPen(QColor(223,223,223))
        painter.drawText(QRectF(755,512,67,24),Qt.AlignCenter,str(round(self.bpm*self.speed)))
        font.setPixelSize(20)
        painter.setFont(font)
        painter.setPen(QColor(0,223,0))
        painter.drawText(QRectF(755,62,67,20),Qt.AlignCenter,str(round(174800*(1000-self.sudden)/1000/self.bpm/self.hiSpeed/self.speed)) if self.bpm!=0 else "---")
        painter.setPen(QColor(223,223,223))
        painter.drawText(QRectF(755,34,67,20),Qt.AlignCenter,str(self.sudden))
        font.setPixelSize(18)
        painter.setFont(font)
        painter.drawText(QRectF(755,124,67,18),Qt.AlignCenter,str('{:.2f}'.format(round(self.hiSpeed,2))))
        painter.drawText(QRectF(755,450,67,18),Qt.AlignCenter,str('{:+.1f}'.format(round(self.speed*100-100,1))))
        font.setPixelSize(12)
        painter.setFont(font)
        painter.drawText(QRectF(755,492,67,12),Qt.AlignCenter,"BPM")
        font.setPixelSize(10)
        painter.setFont(font)
        painter.drawText(QRectF(755,16,67,10),Qt.AlignCenter,"SUDDEN+")
        painter.drawText(QRectF(755,106,67,10),Qt.AlignCenter,"HI-SPEED")
        painter.drawText(QRectF(755,432,67,10),Qt.AlignCenter,"SPEED")
        painter.setPen(Qt.NoPen)
    
    
    def setColorPos(self, lane_arg):
        color=None
        if lane_arg in {0,15}:                 color='s'
        elif lane_arg in {1,3,5,7,8,10,12,14}: color='w'
        elif lane_arg in {2,4,6,9,11,13}:      color='b'
        lane=None
        if self.isFlip:
            if lane_arg==0: lane=15
            elif 1<=lane_arg<8: lane=lane_arg+7
            elif 8<=lane_arg<15: lane=lane_arg-7
            elif lane_arg==15: lane=0
        else: lane=lane_arg
        pos=lane*36
        if lane>=8: pos+=108
        if lane==15: pos+=36
        return color, pos
    
    def drawKeybeam(self, painter, color, pos, t):
        if   color == 's':
            if   t>6:
                lg = QLinearGradient(0, 540-(9-t)*120, 0, 540)
                lg.setColorAt(0.0, QColor(0, 255, 223, 0))
                lg.setColorAt(1.0, QColor(0, 255, 223, 255))
                painter.setBrush(lg)
                painter.drawRect(2+pos, 540-(9-t)*120, 67, (9-t)*120)
            elif t>3:
                lg = QLinearGradient(0, 180, 0, 540)
                lg.setColorAt(0.0, QColor(0, 255, 223, 0))
                lg.setColorAt(1.0, QColor(0, 255, 223, 255))
                painter.setBrush(lg)
                painter.drawRect(2+pos, 180, 67, 360)
            elif t>0:
                lg = QLinearGradient(0, 180, 0, 540)
                lg.setColorAt(0.0, QColor(0, 255, 223, 0))
                lg.setColorAt(1.0, QColor(0, 255, 223, t*64))
                painter.setBrush(lg)
                painter.drawRect(2+pos+(4-t)*9,180,67-(4-t)*18,360)
        elif color == 'w':
            if   t>3:
                lg = QLinearGradient(0, 180, 0, 540)
                lg.setColorAt(0.0, QColor(63, 127, 255, 0))
                lg.setColorAt(1.0, QColor(63, 127, 255, 255))
                painter.setBrush(lg)
                painter.drawRect(34+pos,180,39,360)
            elif t>0:
                lg = QLinearGradient(0, 180, 0, 540)
                lg.setColorAt(0.0, QColor(63, 127, 255, 0))
                lg.setColorAt(1.0, QColor(63, 127, 255, t*64))
                painter.setBrush(lg)
                painter.drawRect(34+pos+(4-t)*5,180,39-(4-t)*10,360)
        elif color == 'b':
            if   t>3:
                lg = QLinearGradient(0, 180, 0, 540)
                lg.setColorAt(0.0, QColor(127, 223, 255, 0))
                lg.setColorAt(1.0, QColor(127, 223, 255, 255))
                painter.setBrush(lg)
                painter.drawRect(38+pos,180,31,360)
            elif t>0:
                lg = QLinearGradient(0, 180, 0, 540)
                lg.setColorAt(0.0, QColor(127, 223, 255, 0))
                lg.setColorAt(1.0, QColor(127, 223, 255, t*64))
                painter.setBrush(lg)
                painter.drawRect(38+pos+(4-t)*4,180,31-(4-t)*8,360)
    
    def drawLongNote(self, painter, color, pos, yn, durationN):
        if color == 's':
            if not self.score.isHCN:
                color1=QColor(127, 127, 127)
                color2=QColor(191, 191, 191)
                color3=QColor(191, 191, 191)
                color4=QColor(127, 127, 127)
                color5=QColor(223, 223, 223)
                color6=QColor(255, 255, 255)
            else:
                color1=QColor(63, 31, 95)
                color2=QColor(127, 95, 159)
                color3=QColor(127, 127, 127)
                color4=QColor(63, 63, 63)
                color5=QColor(191, 191, 191)
                color6=QColor(223, 223, 223)
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRect(2+pos,yn,67,durationN)
            painter.setBrush(color1)
            painter.drawRect(5+pos,yn+8,4,durationN-24)
            painter.drawRect(62+pos,yn+8,4,durationN-24)
            painter.drawRect(22+pos,yn+8,27,durationN-24)
            painter.setBrush(color2)
            painter.drawRect(32+pos,yn+8,7,durationN-24)
            painter.setBrush(color3)
            painter.drawRect(2+pos,yn+5,67,3)
            painter.drawRect(2+pos,yn+durationN-16,67,3)
            painter.setBrush(color4)
            painter.drawRect(49+pos,yn+5,14,3)
            painter.drawRect(49+pos,yn+durationN-16,14,3)
            painter.setBrush(color5)
            painter.drawRect(2+pos,yn+5,67,1)
            painter.drawRect(2+pos,yn+durationN-16,67,1)
            painter.drawRect(15+pos,yn+5,10,3)
            painter.drawRect(15+pos,yn+durationN-16,10,3)
            painter.setBrush(color6)
            painter.drawRect(19+pos,yn+5,2,3)
            painter.drawRect(19+pos,yn+durationN-16,2,3)
        elif color == 'w':
            if not self.score.isHCN:
                color1=QColor(127, 127, 127)
                color2=QColor(191, 191, 191)
                color3=QColor(191, 191, 191)
                color4=QColor(127, 127, 127)
                color5=QColor(223, 223, 223)
                color6=QColor(255, 255, 255)
            else:
                color1=QColor(127, 95, 63)
                color2=QColor(255, 223, 191)
                color3=QColor(127, 127, 127)
                color4=QColor(63, 63, 63)
                color5=QColor(191, 191, 191)
                color6=QColor(223, 223, 223)
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRect(34+pos,yn,39,durationN)
            painter.setBrush(color1)
            painter.drawRect(36+pos,yn+8,2,durationN-24)
            painter.drawRect(69+pos,yn+8,2,durationN-24)
            painter.drawRect(49+pos,yn+8,9,durationN-24)
            painter.setBrush(color2)
            painter.drawRect(52+pos,yn+8,3,durationN-24)
            painter.setBrush(color3)
            painter.drawRect(34+pos,yn+5,39,3)
            painter.drawRect(34+pos,yn+durationN-16,39,3)
            painter.setBrush(color4)
            painter.drawRect(59+pos,yn+5,10,3)
            painter.drawRect(59+pos,yn+durationN-16,10,3)
            painter.setBrush(color5)
            painter.drawRect(34+pos,yn+5,39,1)
            painter.drawRect(34+pos,yn+durationN-16,39,1)
            painter.drawRect(40+pos,yn+5,10,3)
            painter.drawRect(40+pos,yn+durationN-16,10,3)
            painter.setBrush(color6)
            painter.drawRect(44+pos,yn+5,2,3)
            painter.drawRect(44+pos,yn+durationN-16,2,3)
        elif color == 'b':
            if not self.score.isHCN:
                color1=QColor(63, 63, 191)
                color2=QColor(127, 127, 223)
                color3=QColor(0, 63, 191)
                color4=QColor(0, 0, 127)
                color5=QColor(63, 127, 223)
                color6=QColor(127, 191, 255)
            else:
                color1=QColor(95, 63, 127)
                color2=QColor(223, 191, 255)
                color3=QColor(127, 127, 127)
                color4=QColor(63, 63, 63)
                color5=QColor(191, 191, 191)
                color6=QColor(223, 223, 223)
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRect(38+pos,yn,31,durationN)
            painter.setBrush(color1)
            painter.drawRect(40+pos,yn+8,2,durationN-24)
            painter.drawRect(65+pos,yn+8,2,durationN-24)
            painter.drawRect(49+pos,yn+8,9,durationN-24)
            painter.setBrush(color2)
            painter.drawRect(52+pos,yn+8,3,durationN-24)
            painter.setBrush(color3)
            painter.drawRect(38+pos,yn+5,31,3)
            painter.drawRect(38+pos,yn+durationN-16,31,3)
            painter.setBrush(color4)
            painter.drawRect(57+pos,yn+5,10,3)
            painter.drawRect(57+pos,yn+durationN-16,10,3)
            painter.setBrush(color5)
            painter.drawRect(38+pos,yn+5,31,1)
            painter.drawRect(38+pos,yn+durationN-16,31,1)
            painter.drawRect(42+pos,yn+5,10,3)
            painter.drawRect(42+pos,yn+durationN-16,10,3)
            painter.setBrush(color6)
            painter.drawRect(46+pos,yn+5,2,3)
            painter.drawRect(46+pos,yn+durationN-16,2,3)
    
    def drawNote(self, painter, color, status, pos, yn):
        if color == 's':
            if status==0:
                color1=QColor(255, 0, 0)
                color2=QColor(223, 0, 0)
                color3=QColor(255, 127, 127)
            else:
                if not self.score.isHCN:
                    color1=QColor(255, 191, 0)
                    color2=QColor(255, 127, 0)
                    color3=QColor(255, 223, 0)
                else:
                    color1=QColor(223, 0, 255)
                    color2=QColor(191, 0, 255)
                    color3=QColor(255, 127, 255)
            painter.setBrush(color1)
            painter.drawRect(2+pos,yn,67,8)
            painter.setBrush(color2)
            painter.drawRect(49+pos,yn,14,8)
            painter.setBrush(color3)
            painter.drawRect(2+pos,yn,67,1)
            painter.drawRect(13+pos,yn,14,8)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRect(19+pos,yn,2,8)
        elif color == 'w':
            if status==0:
                color1=QColor(191, 191, 191)
                color2=QColor(127, 127, 127)
                color3=QColor(223, 223, 223)
            else:
                if not self.score.isHCN:
                    color1=QColor(191, 191, 127)
                    color2=QColor(127, 127, 63)
                    color3=QColor(223, 223, 191)
                else:
                    color1=QColor(255, 191, 127)
                    color2=QColor(255, 127, 64)
                    color3=QColor(255, 223, 191)
            painter.setBrush(color1)
            painter.drawRect(34+pos,yn,39,8)
            painter.setBrush(color2)
            painter.drawRect(59+pos,yn,10,8)
            painter.setBrush(color3)
            painter.drawRect(34+pos,yn,39,1)
            painter.drawRect(40+pos,yn,10,8)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRect(44+pos,yn,2,8)
        elif color == 'b':
            if status==0:
                color1=QColor(0, 0, 255)
                color2=QColor(0, 0, 191)
                color3=QColor(127, 127, 255)
            else:
                if not self.score.isHCN:
                    color1=QColor(63, 191, 255)
                    color2=QColor(0, 127, 255)
                    color3=QColor(127, 223, 255)
                else:
                    color1=QColor(191, 159, 255)
                    color2=QColor(159, 127, 223)
                    color3=QColor(223, 191, 255)
            painter.setBrush(color1)
            painter.drawRect(38+pos,yn,31,8)
            painter.setBrush(color2)
            painter.drawRect(57+pos,yn,10,8)
            painter.setBrush(color3)
            painter.drawRect(38+pos,yn,31,1)
            painter.drawRect(42+pos,yn,10,8)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawRect(46+pos,yn,2,8)
    
    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 822, 552)
        self.graphicsView.setScene(scene)
        self.display = Display()
        scene.addItem(self.display)
        self.graphicsView.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.timer = QTimer(self)
        self.timer.setInterval(1000.0/60)
        self.timer.timeout.connect(self.update_yPhase)
        self.timer.start()
        
        style='''
            QPushButton{
                background-color: transparent;
                color:#7F7F7F;
                border:2px solid #7F7F7F;
            }
            QPushButton:checked{
                background-color:transparent;
                color:#3FAFFF;
                border:2px solid #3FAFFF;
            }
            
            QPushButton#playBack{
                font:bold 30px;
                border-radius: 25px;
            }
            QPushButton#normalSpeed{
                background-color: #2F2F2F;
                border:10px solid #3F3F3F;
                border-radius: 15px;
            }
            QPushButton:checked#normalSpeed{
                background-color: #7FDF3F;
            }
            QPushButton#hiSpeed{
                font:bold 24px;
                border:0px;
                padding-bottom:4px;
            }
            QPushButton:pressed#hiSpeed{
                color:#3FAFFF;
            }
            QPushButton#fhs{
                font:bold 14px;
                border-radius: 4px;
            }
            QSlider::groove:vertical#speedBar{
                background-color:#2F2F2F;
                width:6px;
                height:270px;
            }
            QSlider::handle:vertical#speedBar{
                background-color:#DFDFDF;
                border:0px;
                height: 6px;
                margin: 0px -12px;
            }
            QSlider::groove:vertical#suddenBar{
                background-color:#2F2F2F;
                width:6px;
                height:540px;
            }
            QSlider::groove:horizontal#seekBar{
                background-color:#2F2F2F;
                height:6px;
                width:324px;
            }
            QPushButton#style{
                font:bold 16px;
                border-radius: 4px;
            }
            QPushButton#file{
                font:bold 12px;
                border-radius: 4px;
            }
            QLineEdit{
                background-color: transparent;
                border:1px solid #CFCFCF;
                color:#CFCFCF;
            }
            '''
        
        #           name,           label,      objectName,     size,       check,          connect
        self.button('playBack',     '>',        'playBack',     50,  50,    True,  False,   'playBack',     style)
        self.button('normalSpeed',  '',         'normalSpeed',  30,  30,    True,  True,    'normalSpeed',  style)
        self.button('minus',        ' - ',      'hiSpeed',      24,  30,    False, False,   'hiSpeedMinus', style)
        self.button('plus',         ' + ',      'hiSpeed',      24,  30,    False, False,   'hiSpeedPlus',  style)
        self.button('fhs',          'FHS',      'fhs',          60,  24,    True,  False,   'switch_fhs',   style)
        self.button('fileOpen',     'OPEN',     'file',         50,  20,    True,  False,   'fileOpen',     style)
        self.button('flip',         'FLIP',     'style',        60,  24,    True,  False,   'flip',         style)
        self.button('normal1',      'NORMAL',   'style',        120, 24,    True,  True,    'normal1',      style)
        self.button('random1',      'RANDOM',   'style',        120, 24,    True,  False,   'random1',      style)
        self.button('rRandom1',     'R-RANDOM', 'style',        120, 24,    True,  False,   'rRandom1',     style)
        self.button('sRandom1',     'S-RANDOM', 'style',        120, 24,    True,  False,   'sRandom1',     style)
        self.button('mirror1',      'MIRROR',   'style',        120, 24,    True,  False,   'mirror1',      style)
        self.button('normal2',      'NORMAL',   'style',        120, 24,    True,  True,    'normal2',      style)
        self.button('random2',      'RANDOM',   'style',        120, 24,    True,  False,   'random2',      style)
        self.button('rRandom2',     'R-RANDOM', 'style',        120, 24,    True,  False,   'rRandom2',     style)
        self.button('sRandom2',     'S-RANDOM', 'style',        120, 24,    True,  False,   'sRandom2',     style)
        self.button('mirror2',      'MIRROR',   'style',        120, 24,    True,  False,   'mirror2',      style)
        
        #           name,           vertical,   objectName,     invert, range,      value,  pressed,    released,   changed
        self.slider('sudden',       True,       'suddenBar',    True,   0,    999,  0,      'clicked',  'clicked',  'change_sudden',    style)
        self.slider('seek',         False,      'seekBar',      False,  -512, self.display.score.length,
                                                                                    -512,   'pause',    'resume',   'change_yPhase',     style)
        self.slider('speed',        True,       'speedBar',     True,  500,  1500, 1000,   'clicked',  'clicked',  'change_speed',      style)
        
        #           name,           label_,                                                  width,  center
        self.label( 'speed',        '<p><font size="3" color="#CFCFCF">SPEED</font></p>',    None,   True)
        self.label( 'hiSpeed',      '<p><font size="3" color="#CFCFCF">HI-SPEED</font></p>', None,   True)
        self.label( 'url',          '<p><font size="3" color="#CFCFCF">URL:</font></p>',     None,   False)
        self.label( 'file',         '<p><font size="3" color="#CFCFCF">FILE:</font></p>',    None,   False)
        self.label( 'genre',        self.set_genre(),                                        280,    True)
        self.label( 'title',        self.set_title(),                                        280,    True)
        self.label( 'artist',       self.set_artist(),                                       280,    True)
        self.label( 'level',        self.set_level(),                                        280,    True)
        
        #               name,   size,       pressed
        self.lineEdit(  'url',  230, 20,    'analyze_web',   style)
        
        suddenBarLayout = QVBoxLayout()
        suddenBarLayout.setSpacing(0)
        suddenBarLayout.addWidget(self.suddenBar)
        suddenBarLayout.addSpacing(10)
        
        speedLayout = QGridLayout()
        speedLayout.addWidget(self.speedLabel,0,0,1,2)
        speedLayout.addWidget(self.speedBar,1,0,1,1)
        speedLayout.addWidget(self.normalSpeedButton,1,1,1,1)
        speedLayout.setHorizontalSpacing(8)
        speedLayout.setVerticalSpacing(16)
        
        hiSpeedLayout = QGridLayout()
        hiSpeedLayout.addWidget(self.hiSpeedLabel,0,0,1,2)
        hiSpeedLayout.addWidget(self.minusButton,1,0,1,1)
        hiSpeedLayout.addWidget(self.plusButton,1,1,1,1)
        hiSpeedLayout.addWidget(self.fhsButton,2,0,1,2)
        hiSpeedLayout.setHorizontalSpacing(8)
        hiSpeedLayout.setVerticalSpacing(8)
        
        playBackLayout = QVBoxLayout()
        playBackLayout.setSpacing(24)
        playBackLayout.addSpacing(8)
        playBackLayout.addWidget(self.playBackButton)
        playBackLayout.addSpacing(60)
        playBackLayout.addLayout(speedLayout)
        playBackLayout.addLayout(hiSpeedLayout)
        
        seekBarLayout = QHBoxLayout()
        seekBarLayout.setSpacing(0)
        seekBarLayout.addSpacing(214)
        seekBarLayout.addWidget(self.seekBar)
        seekBarLayout.addSpacing(66)
        seekBarLayout.addSpacing(214)
        
        playerLayout=QGridLayout()
        playerLayout.addLayout(suddenBarLayout,0,0)
        playerLayout.addWidget(self.graphicsView,0,1)
        playerLayout.addLayout(playBackLayout,0,2)
        playerLayout.addLayout(seekBarLayout,1,1)
        playerLayout.setColumnStretch(3,1)
        playerLayout.setRowStretch(2,1)
        
        analyzeLayout = QGridLayout()
        analyzeLayout.setHorizontalSpacing(8)
        analyzeLayout.setVerticalSpacing(12)
        analyzeLayout.addWidget(self.urlLabel,0,0)
        analyzeLayout.addWidget(self.urlEdit,0,1)
        analyzeLayout.addWidget(self.fileLabel,1,0)
        analyzeLayout.addWidget(self.fileOpenButton,1,1)
        analyzeLayout.setColumnStretch(2,1)
        
        songInfoLayout=QVBoxLayout()
        songInfoLayout.setSpacing(32)
        songInfoLayout.addSpacing(24)
        songInfoLayout.addWidget(self.genreLabel)
        songInfoLayout.addWidget(self.titleLabel)
        songInfoLayout.addWidget(self.artistLabel)
        songInfoLayout.addWidget(self.levelLabel)
        songInfoLayout.addStretch()
        
        
        styleLayout = QGridLayout()
        styleLayout.setHorizontalSpacing(8)
        styleLayout.setVerticalSpacing(12)
        styleLayout.addWidget(self.flipButton,0,0)
        styleLayout.addWidget(self.normal1Button,1,0)
        styleLayout.addWidget(self.random1Button,2,0)
        styleLayout.addWidget(self.rRandom1Button,3,0)
        styleLayout.addWidget(self.sRandom1Button,4,0)
        styleLayout.addWidget(self.mirror1Button,5,0)
        styleLayout.addWidget(self.normal2Button,1,1)
        styleLayout.addWidget(self.random2Button,2,1)
        styleLayout.addWidget(self.rRandom2Button,3,1)
        styleLayout.addWidget(self.sRandom2Button,4,1)
        styleLayout.addWidget(self.mirror2Button,5,1)
        
        propertyLayout = QVBoxLayout()
        propertyLayout.setSpacing(32)
        propertyLayout.addLayout(analyzeLayout)
        propertyLayout.addLayout(songInfoLayout)
        propertyLayout.addSpacing(32)
        propertyLayout.addLayout(styleLayout)
        propertyLayout.addStretch()
        
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(playerLayout)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("IIDX simulator")
    
    def button(self, name, label, objectName, width, height, checkable, checked, clicked, style):
        exec("self.%sButton = QPushButton('%s', self)"      % (name, label))
        exec("self.%sButton.setObjectName('%s')"            % (name, objectName))
        exec("self.%sButton.setStyleSheet(style)"           % (name))
        exec("self.%sButton.setFixedSize(%d, %d)"           % (name, width, height))
        if checkable:
            exec("self.%sButton.setCheckable(True)"         % (name))
            exec("self.%sButton.setChecked(%r)"             % (name, checked))
        exec("self.%sButton.clicked.connect(self.%s)"       % (name, clicked))
    
    def slider(self, name, vertical, objectName, invert, range_min, range_max, value, pressed, released, changed, style):
        if vertical:
            exec("self.%sBar = QSlider(Qt.Vertical, self)"      % (name))
        else:
            exec("self.%sBar = QSlider(Qt.Horizontal, self)"    % (name))
        exec("self.%sBar.setObjectName('%s')"                   % (name, objectName))
        exec("self.%sBar.setStyleSheet(style)"                  % (name))
        if invert:
            exec("self.%sBar.setInvertedAppearance(True)"       % (name))
        exec("self.%sBar.setRange(%d, %d)"                      % (name, range_min, range_max))
        exec("self.%sBar.setValue(%d)"                          % (name, value))
        exec("self.%sBar.sliderPressed.connect(self.%s)"        % (name, pressed))
        exec("self.%sBar.sliderReleased.connect(self.%s)"       % (name, released))
        exec("self.%sBar.valueChanged.connect(self.%s)"         % (name, changed))
    
    def label(self, name, label_, width, center):
        exec("self.%sLabel = QLabel('%s', self)"                % (name, label_))
        if width:
            exec("self.%sLabel.setFixedWidth(%d)"             % (name, width))
        if center:
            exec("self.%sLabel.setAlignment(Qt.AlignCenter)"    % (name))
    
    def lineEdit(self, name, width, height, pressed, style):
        exec("self.%sEdit = QLineEdit()"                    % (name))
        exec("self.%sEdit.setStyleSheet(style)"             % (name))
        exec("self.%sEdit.setFixedSize(%d, %d)"             % (name, width, height))
        exec("self.%sEdit.returnPressed.connect(self.%s)"   % (name, pressed))
    
    def analyze_web(self):
        if self.urlEdit.text():
            self.playBackButton.setChecked(False)
            self.display.switch_isPlaying(False)
            
            url=re.findall(r'([^/\.\?]+)',self.urlEdit.text())
            if not os.path.exists(os.getcwd()+'/scores/DP/'+folderDict[url[-4]]):
                os.makedirs(os.getcwd()+'/scores/DP/'+folderDict[url[-4]])
            
            fileName=folderDict[url[-4]]+'/'+url[-3]+'_'+re.findall(r'([A-Z1-9])',url[-1])[1]+'.txt'
            if os.path.exists('scores/DP/'+fileName):
                self.analyze_text(os.getcwd()+'/scores/DP/'+fileName)
            else:
                self.display.score.analyze_web(self.urlEdit.text())
                self.display.score.save_text(os.getcwd()+'/scores/DP/'+fileName)
                self.reset()
            self.urlEdit.setText('')
            
    def fileOpen(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', 'scores/DP', filter="Image Files (*.txt)")
        if fileName[0]:
            self.analyze_text(fileName[0])
        self.fileOpenButton.setChecked(False)
            
    def analyze_text(self,filePath):
        self.playBackButton.setChecked(False)
        self.display.switch_isPlaying(False)
        self.display.score.analyze_text(filePath)
        self.reset()
        
    def playBack(self,isChecked):
        self.display.switch_isPlaying(isChecked)
            
    def pause(self):
        self.display.switch_isPlaying(False)
        
    def resume(self):
        if self.playBackButton.isChecked():
            self.display.switch_isPlaying(True)
    
    def clicked(self):
        self.update_yPhase()
            
    def change_sudden(self, sudden):
        self.display.change_sudden(sudden)
            
    def change_yPhase(self,yPhase):
        self.display.update_yPhase(float(yPhase))
    
    def reset(self):
        self.normal1()
        self.normal2()
        self.seekBar.setRange(-512,self.display.score.length)
        self.seekBar.setValue(-512)
        self.change_yPhase(-512)
        self.change_sudden(self.display.sudden)
        self.genreLabel.setText(self.set_genre())
        self.titleLabel.setText(self.set_title())
        self.artistLabel.setText(self.set_artist())
        self.levelLabel.setText(self.set_level())
    
    def change_speed(self,speed):
        self.display.change_speed(float(speed)/1000)
        self.normalSpeedButton.setChecked(False)
        
        self.update_yPhase()
        
    def normalSpeed(self):
        self.display.change_speed(1.0)
        self.speedBar.setValue(1000)
        self.normalSpeedButton.setChecked(True)
        
        self.update_yPhase()
        
    def hiSpeedMinus(self):
        self.display.change_hiSpeed(True)
        
        self.update_yPhase()
        
    def hiSpeedPlus(self):
        self.display.change_hiSpeed(False)
        
        self.update_yPhase()
    
    def switch_fhs(self, isChecked):
        self.display.switch_fhs(isChecked)
        
        self.update_yPhase()
    
    def flip(self, isChecked):
        self.display.flip(isChecked)
    
    def normal1(self):
        self.display.change_style(0, 0)
        self.normal1Button.setChecked(True)
        self.random1Button.setChecked(False)
        self.rRandom1Button.setChecked(False)
        self.sRandom1Button.setChecked(False)
        self.mirror1Button.setChecked(False)
        
        self.update_yPhase()
        
    def random1(self):
        self.display.change_style(0, 1)
        self.normal1Button.setChecked(False)
        self.random1Button.setChecked(True)
        self.rRandom1Button.setChecked(False)
        self.sRandom1Button.setChecked(False)
        self.mirror1Button.setChecked(False)
        
        self.update_yPhase()
        
    def rRandom1(self):
        self.display.change_style(0, 2)
        self.normal1Button.setChecked(False)
        self.random1Button.setChecked(False)
        self.rRandom1Button.setChecked(True)
        self.sRandom1Button.setChecked(False)
        self.mirror1Button.setChecked(False)
        
        self.update_yPhase()
            
    def sRandom1(self):
        self.display.change_style(0, 3)
        self.normal1Button.setChecked(False)
        self.random1Button.setChecked(False)
        self.rRandom1Button.setChecked(False)
        self.sRandom1Button.setChecked(True)
        self.mirror1Button.setChecked(False)
        
        self.update_yPhase()
        
    def mirror1(self):
        self.display.change_style(0, 4)
        self.normal1Button.setChecked(False)
        self.random1Button.setChecked(False)
        self.rRandom1Button.setChecked(False)
        self.sRandom1Button.setChecked(False)
        self.mirror1Button.setChecked(True)
        
        self.update_yPhase()
        
    def normal2(self):
        self.display.change_style(1, 0)
        self.normal2Button.setChecked(True)
        self.random2Button.setChecked(False)
        self.rRandom2Button.setChecked(False)
        self.sRandom2Button.setChecked(False)
        self.mirror2Button.setChecked(False)
        
        self.update_yPhase()
        
    def random2(self):
        self.display.change_style(1, 1)
        self.normal2Button.setChecked(False)
        self.random2Button.setChecked(True)
        self.rRandom2Button.setChecked(False)
        self.sRandom2Button.setChecked(False)
        self.mirror2Button.setChecked(False)
        
        self.update_yPhase()
        
    def rRandom2(self):
        self.display.change_style(1, 2)
        self.normal2Button.setChecked(False)
        self.random2Button.setChecked(False)
        self.rRandom2Button.setChecked(True)
        self.sRandom2Button.setChecked(False)
        self.mirror2Button.setChecked(False)
        
        self.update_yPhase()
            
    def sRandom2(self):
        self.display.change_style(1, 3)
        self.normal2Button.setChecked(False)
        self.random2Button.setChecked(False)
        self.rRandom2Button.setChecked(False)
        self.sRandom2Button.setChecked(True)
        self.mirror2Button.setChecked(False)
        
        self.update_yPhase()
        
    def mirror2(self):
        self.display.change_style(1, 4)
        self.normal2Button.setChecked(False)
        self.random2Button.setChecked(False)
        self.rRandom2Button.setChecked(False)
        self.sRandom2Button.setChecked(False)
        self.mirror2Button.setChecked(True)
        
        self.update_yPhase()
            
    def update_yPhase(self):
        self.display.update_yPhase(None)
        if self.display.isEnd:
            self.playBackButton.setChecked(False)
            self.display.switch_isPlaying(False)
            self.seekBar.setValue(-512)
            self.change_yPhase(-512)
            self.display.switch_isEnd(False)
            
    def set_genre(self):
        return '<p><font size="4" color="#CFCFCF">'+self.display.score.genre+'</font></p>'
    def set_title(self):
        return '<p><font size="7" color="#CFCFCF">'+self.display.score.title+'</font></p>'
    def set_artist(self):
        return '<p><font size="4" color="#CFCFCF">'+self.display.score.artist+'</font></p>'
    def set_level(self):
        if self.display.score.level1=='ANOTHER':
            return '<p><font size="3" color="#CF3F3F">'+self.display.score.level+'</font></p>'
        elif self.display.score.level1=='HYPER':
            return '<p><font size="3" color="#CF7F3F">'+self.display.score.level+'</font></p>'
        elif self.display.score.level1=='NORMAL':
            return '<p><font size="3" color="#6F6FDF">'+self.display.score.level+'</font></p>'
        else:
            return '<p><font size="3" color="#CFCFCF">'+self.display.score.level+'</font></p>'
    
if __name__ == '__main__':
    import sys
    if not os.path.exists(os.getcwd()+'/scores'):
        os.makedirs(os.getcwd()+'/scores')
    if not os.path.exists(os.getcwd()+'/scores/DP'):
        os.makedirs(os.getcwd()+'/scores/DP')
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    pal = mainWindow.palette()
    pal.setColor(mainWindow.backgroundRole(), QColor(63,63,63))
    mainWindow.setPalette(pal)
    mainWindow.show()
    sys.exit(app.exec_())
