# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer, QThread, QUrl)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QLinearGradient, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem, 
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QSlider, QFileDialog, QSizePolicy)

import os
import re

from Display import Display

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
    "27":"27_HEROIC_VERSE"
}
   
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 384, 482)
        self.graphicsView.setScene(scene)
        self.display = Display()
        scene.addItem(self.display)
        self.graphicsView.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.timer = QTimer(self)
        self.timer.setInterval(16)
        self.timer.timeout.connect(self.update_yPhase)
        self.timer.start()
        
        self.fileName = os.getcwd()+'/scores/SP/'
        
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
        
        self.button('fileOpen',     'OPEN',     'file',         50,  20,    True,  False,   'fileOpen',     style)
        self.button('fileNew',      'NEW',      'file',         50,  20,    True,  False,   'fileNew',      style)
        self.button('fileEdit',     'EDIT',     'file',         50,  20,    True,  False,   'fileEdit',     style)
        self.button('fileSave',     'SAVE',     'file',         50,  20,    True,  False,   'fileSave',     style)
        
        self.button('player1',      '1P',       'style',        40,  24,    True,  True,    'player1',      style)
        self.button('player2',      '2P',       'style',        40,  24,    True,  False,   'player2',      style)
        self.button('off',          'OFF',      'style',        180, 24,    True,  True,    'off',          style)
        self.button('random',       'RANDOM',   'style',        180, 24,    True,  False,   'random',       style)
        self.button('rRandom',      'R-RANDOM', 'style',        180, 24,    True,  False,   'rRandom',      style)
        self.button('sRandom',      'S-RANDOM', 'style',        180, 24,    True,  False,   'sRandom',      style)
        self.button('mirror',       'MIRROR',   'style',        180, 24,    True,  False,   'mirror',       style)
        
        self.button('pencil',       '/',        'style',        54,  24,    True,  False,    'pencil',       style)
        self.button('cnPencil',     'CN',       'style',        54,  24,    True,  False,   'cnPencil',     style)
        self.button('barPencil',    '---',      'style',        54,  24,    True,  False,   'barPencil',   style)
        self.button('bpmPencil',    'BPM',      'style',        54,  24,    True,  False,   'bpmPencil',    style)
        
        self.button('grid16',       '-16-',     'style',        60,  24,    True,  True,   'grid16',      style)
        self.button('grid32',       '-32-',     'style',        60,  24,    True,  False,   'grid32',      style)
        self.button('grid64',       '-64-',     'style',        60,  24,    True,  False,   'grid64',      style)
        self.button('grid12',       '-12-',     'style',        60,  24,    True,  False,   'grid12',      style)
        self.button('grid24',       '-24-',     'style',        60,  24,    True,  False,   'grid24',      style)
        self.button('grid48',       '-48-',     'style',        60,  24,    True,  False,   'grid48',      style)
        
        #           name,           label_,                                                  width,  center
        self.label( 'url',          '<p><font size="3" color="#CFCFCF">URL:</font></p>',     None,   False)
        self.label( 'file',         '<p><font size="3" color="#CFCFCF">FILE:</font></p>',    None,   False)
        self.label( 'genre',        self.set_genre(),                                        280,    True)
        self.label( 'title',        self.set_title(),                                        280,    True)
        self.label( 'artist',       self.set_artist(),                                       280,    True)
        self.label( 'level',        self.set_level(),                                        280,    True)
        
        #               name,   size,       pressed
        self.lineEdit(  'url',  230, 20,    'analyze_web',   style)
        
        
        fileLayout = QGridLayout()
        fileLayout.setHorizontalSpacing(8)
        fileLayout.setVerticalSpacing(12)
        fileLayout.addWidget(self.urlLabel,0,0)
        fileLayout.addWidget(self.urlEdit,0,1,1,4)
        fileLayout.addWidget(self.fileLabel,1,0)
        fileLayout.addWidget(self.fileNewButton,1,1)
        fileLayout.addWidget(self.fileOpenButton,1,2)
        fileLayout.addWidget(self.fileEditButton,1,3)
        fileLayout.addWidget(self.fileSaveButton,1,4)
        fileLayout.setColumnStretch(5,1)
        
        songInfoLayout=QVBoxLayout()
        songInfoLayout.setSpacing(24)
        songInfoLayout.addSpacing(20)
        songInfoLayout.addWidget(self.genreLabel)
        songInfoLayout.addWidget(self.titleLabel)
        songInfoLayout.addWidget(self.artistLabel)
        songInfoLayout.addWidget(self.levelLabel)
        songInfoLayout.addStretch()
        
        playerButtonLayout = QHBoxLayout()
        playerButtonLayout.setSpacing(12)
        playerButtonLayout.addWidget(self.player1Button)
        playerButtonLayout.addWidget(self.player2Button)
        playerButtonLayout.addStretch()
        
        styleLayout = QVBoxLayout()
        styleLayout.setSpacing(6)
        styleLayout.addWidget(self.offButton)
        styleLayout.addWidget(self.randomButton)
        styleLayout.addWidget(self.rRandomButton)
        styleLayout.addWidget(self.sRandomButton)
        styleLayout.addWidget(self.mirrorButton)
        
        toolsLayout = QGridLayout()
        toolsLayout.setHorizontalSpacing(12)
        toolsLayout.setVerticalSpacing(8)
        toolsLayout.addWidget(self.pencilButton,0,0)
        toolsLayout.addWidget(self.cnPencilButton,0,1)
        toolsLayout.addWidget(self.barPencilButton,0,2)
        toolsLayout.addWidget(self.bpmPencilButton,0,3)
        toolsLayout.setColumnStretch(4,1)
        
        gridLayout = QGridLayout()
        gridLayout.setHorizontalSpacing(12)
        gridLayout.setVerticalSpacing(8)
        gridLayout.addWidget(self.grid16Button,0,0)
        gridLayout.addWidget(self.grid32Button,0,1)
        gridLayout.addWidget(self.grid64Button,0,2)
        gridLayout.addWidget(self.grid12Button,1,0)
        gridLayout.addWidget(self.grid24Button,1,1)
        gridLayout.addWidget(self.grid48Button,1,2)
        gridLayout.setColumnStretch(3,1)
        
        propertyLayout = QVBoxLayout()
        propertyLayout.addLayout(fileLayout)
        propertyLayout.addSpacing(16)
        propertyLayout.addLayout(songInfoLayout)
        propertyLayout.addSpacing(32)
        propertyLayout.addLayout(playerButtonLayout)
        propertyLayout.addLayout(styleLayout)
        propertyLayout.addLayout(toolsLayout)
        propertyLayout.addLayout(gridLayout)
        propertyLayout.addStretch()
        
        mainLayout = QGridLayout()
        
        mainLayout.addWidget(self.graphicsView,0,0)
        mainLayout.addLayout(propertyLayout,0,1)
        mainLayout.setRowStretch(1,1)
        
        self.update_layout()
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
            self.display.switch_isPlaying(False)
            
            url=re.findall(r'([^/\.\?]+)',self.urlEdit.text())
            if not os.path.exists(os.getcwd()+'/scores/SP/'+folderDict[url[-4]]):
                os.makedirs(os.getcwd()+'/scores/SP/'+folderDict[url[-4]])
            
            self.fileName=os.getcwd()+'/scores/SP/'+folderDict[url[-4]]+'/'+url[-3]+'_'+re.findall(r'([A-Z1-9])',url[-1])[1]+'.txt'
            if os.path.exists(self.fileName):
                self.analyze_text(self.fileName)
            else:
                self.display.score.analyze_web(self.urlEdit.text()+"=24")
                self.display.score.save_text(self.fileName)
                self.reset()
            self.urlEdit.setText('')
            
    def fileNew(self, isChecked):
        self.off()
        self.display.switch_isEditing(True)
        self.fileNewButton.setChecked(True)
        self.fileEditButton.setChecked(True)
        self.update_layout()
    
    def fileOpen(self):
        fileName_ = QFileDialog.getOpenFileName(self, 'Open file', 'scores/SP', filter="Image Files (*.txt)")[0]
        if fileName_:
            self.fileName = fileName_
            self.analyze_text(self.fileName)
            self.display.switch_isEditing(False)
            self.fileNewButton.setChecked(False)
            self.fileEditButton.setChecked(False)
            self.fileSaveButton.setChecked(False)
            self.update_layout()
        self.fileOpenButton.setChecked(False)
        
    def fileEdit(self, isChecked):
        if isChecked:
            self.off()
            self.display.switch_isEditing(True)
            self.update_layout()
        else:
            self.display.switch_isEditing(False)
            self.update_layout()
    
    def fileSave(self):
        fileName_ = QFileDialog.getSaveFileName(self, 'Save file', self.fileName, filter="Image Files (*.txt)")[0]
        if fileName_:
            self.fileName = fileName_
            self.display.score.save_text(self.fileName)
        self.fileSaveButton.setChecked(False)
    
    def update_layout(self):
        if self.display.isEditing:
            self.offButton.hide()
            self.randomButton.hide()
            self.rRandomButton.hide()
            self.sRandomButton.hide()
            self.mirrorButton.hide()
            self.pencilButton.show()
            self.cnPencilButton.show()
            self.barPencilButton.show()
            self.bpmPencilButton.show()
            self.grid16Button.show()
            self.grid32Button.show()
            self.grid64Button.show()
            self.grid12Button.show()
            self.grid24Button.show()
            self.grid48Button.show()
        else:
            self.pencilButton.hide()
            self.cnPencilButton.hide()
            self.barPencilButton.hide()
            self.bpmPencilButton.hide()
            self.grid16Button.hide()
            self.grid32Button.hide()
            self.grid64Button.hide()
            self.grid12Button.hide()
            self.grid24Button.hide()
            self.grid48Button.hide()
            self.offButton.show()
            self.randomButton.show()
            self.rRandomButton.show()
            self.sRandomButton.show()
            self.mirrorButton.show()
        self.update()
            
    def analyze_text(self,filePath):
        self.display.switch_isPlaying(False)
        self.display.score.analyze_text(filePath)
        self.reset()
    
    def reset(self):
        self.off()
        self.display.update_yPhase(-768)
        self.display.change_sudden(None)
        self.genreLabel.setText(self.set_genre())
        self.titleLabel.setText(self.set_title())
        self.artistLabel.setText(self.set_artist())
        self.levelLabel.setText(self.set_level())
        
    def player1(self):
        self.display.switch_player(False)
        self.player1Button.setChecked(True)
        self.player2Button.setChecked(False)
    
    def player2(self):
        self.display.switch_player(True)
        self.player1Button.setChecked(False)
        self.player2Button.setChecked(True)
    
    def off(self):
        self.display.change_style(0)
        self.offButton.setChecked(True)
        self.randomButton.setChecked(False)
        self.rRandomButton.setChecked(False)
        self.sRandomButton.setChecked(False)
        self.mirrorButton.setChecked(False)
        
    def random(self):
        self.display.change_style(1)
        self.offButton.setChecked(False)
        self.randomButton.setChecked(True)
        self.rRandomButton.setChecked(False)
        self.sRandomButton.setChecked(False)
        self.mirrorButton.setChecked(False)
        
    def rRandom(self):
        self.display.change_style(2)
        self.offButton.setChecked(False)
        self.randomButton.setChecked(False)
        self.rRandomButton.setChecked(True)
        self.sRandomButton.setChecked(False)
        self.mirrorButton.setChecked(False)
            
    def sRandom(self):
        self.display.change_style(3)
        self.offButton.setChecked(False)
        self.randomButton.setChecked(False)
        self.rRandomButton.setChecked(False)
        self.sRandomButton.setChecked(True)
        self.mirrorButton.setChecked(False)
        
    def mirror(self):
        self.display.change_style(4)
        self.offButton.setChecked(False)
        self.randomButton.setChecked(False)
        self.rRandomButton.setChecked(False)
        self.sRandomButton.setChecked(False)
        self.mirrorButton.setChecked(True)
        
    def pencil(self, isChecked):
        if isChecked:
            self.display.change_tool(1)
        else:
            self.display.change_tool(0)
            self.cnPencilButton.setChecked(False)
            self.barPencilButton.setChecked(False)
            self.bpmPencilButton.setChecked(False)
            
    def cnPencil(self, isChecked):
        if isChecked:
            self.display.change_tool(2)
            self.pencilButton.setChecked(True)
            self.barPencilButton.setChecked(False)
            self.bpmPencilButton.setChecked(False)
        else:
            self.display.change_tool(1)
            
    def barPencil(self, isChecked):
        if isChecked:
            self.display.change_tool(3)
            self.pencilButton.setChecked(True)
            self.cnPencilButton.setChecked(False)
            self.bpmPencilButton.setChecked(False)
        else:
            self.display.change_tool(1)
            
    def bpmPencil(self, isChecked):
        if isChecked:
            self.display.change_tool(4)
            self.pencilButton.setChecked(True)
            self.cnPencilButton.setChecked(False)
            self.barPencilButton.setChecked(False)
        else:
            self.display.change_tool(1)
            
    def grid16(self):
        self.display.change_grid(1)
        self.grid16Button.setChecked(True)
        self.grid32Button.setChecked(False)
        self.grid64Button.setChecked(False)
        self.grid12Button.setChecked(False)
        self.grid24Button.setChecked(False)
        self.grid48Button.setChecked(False)
            
    def grid32(self):
        self.display.change_grid(2)
        self.grid16Button.setChecked(False)
        self.grid32Button.setChecked(True)
        self.grid64Button.setChecked(False)
        self.grid12Button.setChecked(False)
        self.grid24Button.setChecked(False)
        self.grid48Button.setChecked(False)
            
    def grid64(self):
        self.display.change_grid(3)
        self.grid16Button.setChecked(False)
        self.grid32Button.setChecked(False)
        self.grid64Button.setChecked(True)
        self.grid12Button.setChecked(False)
        self.grid24Button.setChecked(False)
        self.grid48Button.setChecked(False)
            
    def grid12(self):
        self.display.change_grid(4)
        self.grid16Button.setChecked(False)
        self.grid32Button.setChecked(False)
        self.grid64Button.setChecked(False)
        self.grid12Button.setChecked(True)
        self.grid24Button.setChecked(False)
        self.grid48Button.setChecked(False)
            
    def grid24(self):
        self.display.change_grid(5)
        self.grid16Button.setChecked(False)
        self.grid32Button.setChecked(False)
        self.grid64Button.setChecked(False)
        self.grid12Button.setChecked(False)
        self.grid24Button.setChecked(True)
        self.grid48Button.setChecked(False)
            
    def grid48(self):
        self.display.change_grid(6)
        self.grid16Button.setChecked(False)
        self.grid32Button.setChecked(False)
        self.grid64Button.setChecked(False)
        self.grid12Button.setChecked(False)
        self.grid24Button.setChecked(False)
        self.grid48Button.setChecked(True)
            
    def update_yPhase(self):
        self.display.update_yPhase(None)
            
    def keyPressEvent(self, event):
        if self.display.isShift:
            if event.key() in {Qt.Key_Z, Qt.Key_X, Qt.Key_C, Qt.Key_V}:
                self.display.change_hiSpeed(False)
            elif event.key() in {Qt.Key_S, Qt.Key_D, Qt.Key_F}:
                self.display.change_hiSpeed(True)
            elif event.key() == Qt.Key_Q:
                self.display.switch_fhs()
        
        elif event.key() == Qt.Key_Shift:
            self.display.isShift = True
            
        elif event.key() == Qt.Key_Space:
            self.display.switch_isPlaying(True)
            
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.display.isShift = False
            
    def set_genre(self):
        return '<p><font size="3" color="#CFCFCF">'+self.display.score.genre+'</font></p>'
    def set_title(self):
        return '<p><font size="6" color="#CFCFCF">'+self.display.score.title+'</font></p>'
    def set_artist(self):
        return '<p><font size="3" color="#CFCFCF">'+self.display.score.artist+'</font></p>'
    def set_level(self):
        if self.display.score.level1=='LEGGENDARIA':
            return '<p><font size="3" color="#CF3FCF">'+self.display.score.level+'</font></p>'
        elif self.display.score.level1=='ANOTHER':
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
    if not os.path.exists(os.getcwd()+'/scores/SP'):
        os.makedirs(os.getcwd()+'/scores/SP')
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    pal = mainWindow.palette()
    pal.setColor(mainWindow.backgroundRole(), QColor(63,63,63))
    mainWindow.setPalette(pal)
    mainWindow.show()
    sys.exit(app.exec_())
