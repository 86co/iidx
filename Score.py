import os
import re
import math
from bs4 import BeautifulSoup
from selenium import webdriver

import random

class Score():
    def __init__(self):
        self.genre='---'
        self.title='---'
        self.artist='---'
        self.level1='---'
        self.level2='---'
        self.level='---'
        self.length=0
        
        self.isHCN=False
        
        self.notes_default = [[] for _ in range(8)]
        self.cNotes_default = [[] for _ in range(8)]
        self.barLine = []
        self.bpm = []
        
        self.number_of_notes=0
    
    def analyze_web(self,url):
        self.initialyze()
        
        options = webdriver.chrome.options.Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=os.getcwd()+'/chromedriver',options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(html, "lxml")
        songInfo=soup.nobr
        bpm_tmp = self.set_songInfo_web(songInfo)
        
        score=soup.body.table.tbody.contents
        bars=[]
        for tr in reversed(score):
            tds=tr.find_all('td')
            for td in tds:
                tables=td.find_all('table')
                for table in reversed(tables):
                    bars.append(table)
        
        yPhase=0.0
        for bar in bars:
            self.barLine.append(yPhase)
            barLength=int(bar.get('height'))
            notesOnBar=bar.tbody.tr.td.div.contents
            
            for note in notesOnBar:
                self.set_note_web(note, yPhase, barLength)
                
            yPhase+=barLength
        
        self.sort_bpmList(bpm_tmp)
        self.sort_notes()
        self.combine_cNotes()
        self.calculate_length()
    
    def set_songInfo_web(self, songInfo):
        self.genre  = re.findall(r'([^\"]+)',songInfo.next_element)[0]
        self.title  = songInfo.b.string
        self.artist = ' '.join(re.findall(r'([\S]+)',re.findall(r'(/[\s].+[\s]bpm:[\d\.]+)',songInfo.b.next_sibling)[0])[1:-1])
        self.level1 = re.findall(r'([\w]+)',songInfo.font.next_element)[1]
        self.level2 = int(re.findall(r'([\d]+)',re.findall(r'(★[\d]+)',songInfo.b.next_sibling)[0])[0])
        self.level  = self.level1+' '+str(self.level2)
        bpm_tmp     = float(re.findall(r'([\d\.]+)',re.findall(r'(bpm:[\d\.]+)',songInfo.b.next_sibling)[0])[0])
        return bpm_tmp
    
    def set_note_web(self, note, yPhase, barLength):
        style=re.findall(r'([\d\.-]+)',note.get('style'))
        src = note.get('src')

        if src in {'../s.gif','../r.gif','../w.gif','../b.gif',
                   '../ls.gif','../hs.gif','../lw.gif','../hw.gif','../lb.gif','../hb.gif'}:
            lane, isCNote = self.toLane(note.get('src'),style[1])
            if isCNote==True:
                self.cNotes_default[lane].append([yPhase+(barLength-1-int(style[0])-int(style[2])),int(style[2])])
            elif isCNote==False:
                self.notes_default[lane].append([yPhase+(barLength-5-int(style[0])),0])

        elif src=='../t.gif':
            self.bpm.append([yPhase+(barLength-2-int(style[0])),int(note.next_sibling.string)])

        if not self.isHCN and src in {'../hs.gif','../hw.gif','../hb.gif'}:
            self.isHCN=True
    
    def toLane(self,src,left):
        if   src in {'../s.gif','../r.gif'}:   return 0, False
        elif src in ('../ls.gif','../hs.gif'): return 0, True
        
        if   src in {'../w.gif','../b.gif'}:                           isCNote = False
        elif src in {'../lw.gif','../hw.gif','../lb.gif','../hb.gif'}: isCNote = True
        
        if   left in {"37","38"}:   lane=1
        elif left in {"51","52"}:   lane=2
        elif left in {"65","66"}:   lane=3
        elif left in {"79","80"}:   lane=4
        elif left in {"93","94"}:   lane=5
        elif left in {"107","108"}: lane=6
        elif left in {"121","122"}: lane=7
            
        else: return None, None
        
        return lane, isCNote
    
    def analyze_text(self,filePath):
        self.initialyze()
        
        with open(filePath,'r') as f:
            text=f.read()
        lines=text.split('\n')
        
        mode=0
        songInfo=[]
        score=[]
        
        for line in lines:
            commands=re.findall(r'(#[A-Z\d_]*)',line)
            if not commands: continue
            command=commands[0]
            if mode==0:
                if command=='#SONGINFO':
                    mode=1
                elif command=='#START':
                    mode=2
            
            if mode==1:
                songInfo.append(line)
            elif mode==2:
                score.append(line)
            
            if command=='#END':
                mode=0
        
        bpm_tmp = self.set_songInfo_text(songInfo)
        
        hold=[0,0,0,0,0,0,0,0]
        yPhase=0.0
        barLength=384.0
        
        for line in score:
            command, option, line = self.handle_line(line)
            if command=='#START':
                self.barLine.append(yPhase)
                if option:
                    if option[0]=='$LENGTH':
                        barLength=384.0*option[1]
            elif command=='#':
                yPhase+=barLength
                self.barLine.append(yPhase)
                if option:
                    if option[0]=='$LENGTH':
                        barLength=384.0*option[1]
            elif command=='#END':
                yPhase+=barLength
            else:
                hold = self.set_note_text(command, line, yPhase, barLength, hold)

        self.sort_bpmList(bpm_tmp)
        self.make_cNotesList()
        self.calculate_length()
    
    def handle_line(self, line):
        command=re.findall(r'(#[A-Z\d_]*)',line)[0]
        line=re.sub(r'(.*#[A-Z\d_]*[\s]*)','',line)
        option=[]
        options=re.findall(r'(\$[A-Z\d_]+[\s]*=[\s]*[\d.]+)',line)
        if options:
            option.append(re.sub(r'([\s]*=[\s]*[\d.]+)','',options[0]))
            option.append(float(re.sub(r'(\$[A-Z\d_]+[\s]*=[\s]*)','',options[0])))
            line=re.sub(r'(\$[A-Z\d_]+[\s]*=[\s]*[\d.]+)','',line)
        return command, option, line
    
    def set_songInfo_text(self, songInfo):
        for line in songInfo[1:-1]:
            command=re.findall(r'(#[A-Z\d_]*)',line)[0]
            line=re.sub(r'(.*#[A-Z\d_]*[\s]*)','',line)
            words=re.findall(r'([^\s]+)',line)
            if   command=='#GENRE':  self.genre=' '.join(words)
            elif command=='#TITLE':  self.title=' '.join(words)
            elif command=='#ARTIST': self.artist=' '.join(words)
            elif command=='#LEVEL':
                                     self.level1=words[0]
                                     self.level2=words[1]
                                     self.level=self.level1+' '+self.level2
            elif command=='#BPM':    bpm_tmp=float(re.findall(r'([\d\.]+)',words[0])[0])
            elif command=='#HCN' and words[0]=='TRUE':
                                     self.isHCN=True
        return bpm_tmp
    
    def set_note_text(self, command, line, yPhase, barLength, hold):
        if command in {'#0','#1','#2','#3','#4','#5','#6','#7'}:
            lane=int(re.findall(r'([\d]+)',command)[0])
            notes=[int(x) for x in re.findall(r'(\d)',line)]
            if notes:
                divide=len(notes)
                for index, note in enumerate(notes):
                    if note==1:
                        self.notes_default[lane].append([yPhase+index*barLength/divide,0])
                    elif note==2:
                        self.notes_default[lane].append([yPhase+index*barLength/divide,1+hold[lane]])
                        hold[lane]=1 if hold[lane]==0 else 0
        elif command=='#S':
            line=re.findall(r'([^,]+)',line)
            notes=[int(x) for x in re.findall(r'(\d)',line[0])]
            bpm=[float(re.findall(r'([\d\.]+)',_)[0]) for _ in line[1:]]
            if notes:
                divide=len(notes)
                i=0
                for index, note in enumerate(notes):
                    if note==1:
                        self.bpm.append([yPhase+index*barLength/divide,bpm[i]])
                        i+=1
        return hold
    
    def save_text(self,filePath):
        text=[]
        text.append("#SONGINFO")
        text.append("\t#GENRE  "+self.genre)
        text.append("\t#TITLE  "+self.title)
        text.append("\t#ARTIST "+self.artist)
        text.append("\t#LEVEL  "+self.level)
        if len(self.bpm)==1:
            text.append("\t#BPM    "+str(int(self.bpm[0][1])))
        else:
            maxBpm=self.bpm[0][1]
            minBpm=self.bpm[0][1]
            for bpm in self.bpm:
                if bpm[1]>maxBpm:
                    maxBpm=bpm[1]
                if bpm[1]<minBpm:
                    minBpm=bpm[1]
            text.append("\t#BPM    "+str(int(minBpm))+'~'+str(int(maxBpm)))
        if self.isHCN:
            text.append("\t#HCN    TRUE")
        else:
            text.append("\t#HCN    FALSE")
        text.append("#END")
        text.append("")
        bar=1
        lengthOfBar=384
        barLine=self.barLine[:]
        barLine.append(barLine[-1]*2-barLine[-2])
        while(bar<len(barLine)):
            lob=lengthOfBar
            lengthOfBar=int(barLine[bar]-barLine[bar-1])
            if lengthOfBar==lob:
                if bar==1:
                    text.append(format(bar,'03')+" #START")
                else:
                    text.append(format(bar,'03')+" #")
            else:
                if bar==1:
                    text.append(format(bar,'03')+" #START $LENGTH="+str(float(lengthOfBar)/384))
                else:
                    text.append(format(bar,'03')+" # $LENGTH="+str(float(lengthOfBar)/384))
            for index,lane in enumerate(self.notes_default):
                notes=[]
                for note in lane:
                    if barLine[bar-1]<=note[0]<barLine[bar]:
                        notes.append([int(note[0]-barLine[bar-1]),1 if note[1]==0 else 2])
                    elif note[0]>=barLine[bar]:
                        break
                if notes:
                    gcd=0
                    for note in notes:
                        gcd=math.gcd(gcd,note[0])
                    gcd=math.gcd(gcd,lengthOfBar)
                    line=['0' for _ in range(int(lengthOfBar/gcd))]
                    for note in notes:
                        line[int(note[0]/gcd)]=str(note[1])
                    line="".join(line)
                    text.append("\t#"+str(index)+" "+line)
            if len(self.bpm)>1:
                bpms=[]
                for bpm in self.bpm:
                    if barLine[bar-1]<=bpm[0]<barLine[bar]:
                        bpms.append([int(bpm[0]-barLine[bar-1]),bpm[1]])
                    elif bpm[0]>=barLine[bar]:
                        break
                if bpms:
                    gcd=0
                    for bpm in bpms:
                        gcd=math.gcd(gcd,bpm[0])
                    gcd=math.gcd(gcd,lengthOfBar)
                    line=['0' for _ in range(int(lengthOfBar/gcd))]
                    for bpm in bpms:
                        line[int(bpm[0]/gcd)]='1'
                    line="".join(line)
                    for bpm in bpms:
                        line+=', '+str(int(bpm[1]))
                    text.append("\t#S "+line)
            bar+=1
        text.append("#END")
        
        with open(filePath,'w') as f:
            f.write('\n'.join(text))
    
    def initialyze(self):
        self.genre='---'
        self.title='---'
        self.artist='---'
        self.level1='---'
        self.level2='---'
        self.level='---'
        self.length=0
        
        self.isHCN=False
        
        self.notes_default = [[] for _ in range(8)]
        self.cNotes_default = [[] for _ in range(8)]
        self.barLine = []
        self.bpm = []
        
        self.number_of_notes=0
    
    def calculate_length(self):
        lastNote=0.0
        for lane in self.notes_default:
            if len(lane)>0:
                self.number_of_notes+=len(lane)
                if lastNote<lane[-1][0]:
                    lastNote=lane[-1][0]
        self.length=lastNote+768
        
    def sort_bpmList(self,bpm_tmp):
        if not self.bpm:
            self.bpm.append([0.0,bpm_tmp])
        self.bpm.sort()
        
    def sort_notes(self):
        for lane in self.notes_default:
            lane.sort()
        for lane in self.cNotes_default:
            lane.sort()
            
    def combine_cNotes(self):
        for laneIndex, lane in enumerate(self.cNotes_default):
            lane.sort()
            for index, note in enumerate(lane):
                i=0
                while self.notes_default[laneIndex][i][0]!=note[0]:
                    i+=1
                self.notes_default[laneIndex][i][1]=1
                while index+1<len(lane) and note[0]+note[1]==lane[index+1][0]:
                    note[1]+=lane[index+1][1]
                    del lane[index+1]
                i=0
                while self.notes_default[laneIndex][i][0]!=note[0]+note[1]:
                    i+=1
                self.notes_default[laneIndex][i][1]=2

    def make_cNotesList(self):
        for laneIndex, lane in enumerate(self.notes_default):
            lane.sort()
            for index, note in enumerate(lane):
                if note[1]==1:
                    self.cNotes_default[laneIndex].append([note[0],lane[index+1][0]-note[0]])
                    
    def add_notes(self, lane, notes, cNotes):
        for note in notes:
            self.notes_default[lane].append(note)
        for note in cNotes:
            self.cNotes_default[lane].append(note)
        self.sort_notes()
        
    def del_notes(self, lane, notes, cNotes):
        for note in notes:
            try:
                self.notes_default[lane].remove(note)
            except:
                pass
        for note in cNotes:
            try:
                self.cNotes_default[lane].remove(note)
            except:
                pass
                
    def change_style(self,style):
        notes=[[] for _ in range(8)]
        cNotes=[[] for _ in range(8)]
        notes[0]=self.notes_default[0]
        cNotes[0]=self.cNotes_default[0]
        if style==0:
            notes[1:8]=self.notes_default[1:8]
            cNotes[1:8]=self.cNotes_default[1:8]
        elif style==1:
            index=[1,2,3,4,5,6,7]
            random.shuffle(index)
            for d, r in enumerate(index):
                notes[d+1]=self.notes_default[r]
                cNotes[d+1]=self.cNotes_default[r]
        elif style==2:
            index=[1,2,3,4,5,6,7]
            if random.randint(0,1)==1:
                index.reverse()
            for _ in range(random.randint(0,6)): index.append(index.pop(0))
            for d, r in enumerate(index):
                notes[d+1]=self.notes_default[r]
                cNotes[d+1]=self.cNotes_default[r]
        elif style==3:
            DF_MIN = 4
            
            notes_sRandom=[[] for _ in range(7)]
            cNotes_sRandom=[[] for _ in range(7)]
            notes_default=[None for _ in range(7)]
            for i, lane in enumerate(self.notes_default[1:]):
                notes_default[i] = lane[:]
            
            noted=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
            
            yPhase=0
            try:
                bpm=self.bpm[0][1]
            except:
                pass
            
            while any(notes_default):
                for i_lane, lane in enumerate(notes_default):
                    count = 0
                    for note in lane:
                        if note[0]<=yPhase: count+=1
                        else: break
                    for _ in range(count):
                        note = lane.pop(0)
                        if note[1] in {0,1}:
                            unnoted=[i for i, x in enumerate(noted) if x == [0,0]]
                            r=random.choice(unnoted)
                            notes_sRandom[r].append(note)
                            if note[1]==0:
                                noted[r][1]=DF_MIN
                            elif note[1]==1:
                                notes_sRandom[r].append(lane[0])
                                cNotes_sRandom[r].append([note[0],lane[0][0]-note[0]])
                                noted[r]=[1,i_lane]
                        elif note[1] == 2:
                            for i in range(7):
                                if noted[i]==[1,i_lane]:
                                    noted[i]=[0,DF_MIN]
                for i in range(7):
                    if noted[i][0]==0 and noted[i][1]>0:
                        noted[i][1]-=1
                    
                yPhase+=2.0/75*bpm
                
                try:
                    bpm=self.bpm[0][1]
                except:
                    pass
                for bpm_ in self.bpm:
                    if bpm_[0]<=yPhase:
                        bpm=bpm_[1]
                    else:
                        break
                
            notes[1:8]=notes_sRandom[0:7]
            cNotes[1:8]=cNotes_sRandom[0:7]
        elif style==4:
            notes[1:8]=self.notes_default[1:8][::-1]
            cNotes[1:8]=self.cNotes_default[1:8][::-1]
        return notes, cNotes