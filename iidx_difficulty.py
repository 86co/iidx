from Score import Score
import os
import re

import numpy
import random
import math

from matplotlib import pyplot

import multiprocessing
import collections

Result = collections.namedtuple("Result", "difficulty, arrangement, guageProcess")
Summary = collections.namedtuple("Summary", "style, times, average, standardDeviation")

pressability0=lambda f: 1/(math.exp(f)+math.exp(-f))
def pressability1(f):
    if f>=math.log(math.sqrt(2)-1):
        return (1-math.exp(f))/(math.exp(f)+math.exp(-f))
    else:
        return 2*(math.sqrt(2)+1)*(1-2*math.exp(f)+math.exp(f*2))/(math.exp(f*2)+math.exp(-f*2)+2)
maxp1 = (math.sqrt(2)-1)/2
recognizability=lambda f: f

folderName={
    'self': '_selfmade',
    '1': '01_1st_style',
    'sub': '01_substream',
    '2': '02_2nd_style',
    '3': '03_3rd_style',
    '4': '04_4th_style',
    '5': '05_5th_style',
    '6': '06_6th_style',
    '7': '07_7th_style',
    '8': '08_8th_style',
    '9': '09_9th_style',
    '10': '10_10th_style',
    '11': '11_IIDX_RED',
    '12': '12_HAPPY_SKY',
    '13': '13_DistorteD',
    '14': '14_GOLD',
    '15': '15_DJ_TROOPERS',
    '16': '16_EMPRESS',
    '17': '17_SIRIUS',
    '18': '18_Resort_Anthem',
    '19': '19_Lincle',
    '20': '20_tricoro',
    '21': '21_SPADA',
    '22': '22_PENDUAL',
    '23': '23_copula',
    '24': '24_SINOBUZ',
    '25': '25_CANNON_BALLERS',
    '26': '26_Rootage',
    '27': '27_HEROIC_VERSE'
}

def main():
    score, guageOption = handle_input()
    totalnotes = 0
    for lane in score.notes_default:
        totalnotes += len(lane)
    snotes = len(score.notes_default[0])
    print(totalnotes, snotes)
    return None
    summary = analyze(score, guageOption)
    summarize(summary)
        
def handle_input():
    score=None
    while score is None:
        fileList=[]
        print('')
        series = input("series: ")
        try: 
            series=folderName[series]
            filePath = os.getcwd()+'/scores/SP/'+series
            fileList = [fileName for fileName in os.listdir(filePath) if re.match(r'[\w]+.txt',fileName)]
            fileList.sort()
        except: continue
        for i, fileName in enumerate(fileList):
            print('{:>3}'.format(str(i+1))+". "+re.findall(r'[\w]+',fileName)[0])
        index = input("  ...: ")
        try:
            index=int(index)
            fileName=fileList[index-1]
        except: continue
        print('')
        print(re.findall(r'[\w]+',fileName)[0])
        input_str = ''
        while input_str not in {'y', 'n'}:
            input_str = input("  (y/n): ")
        if input_str == 'n': continue
        filePath = os.getcwd()+'/scores/SP/'+series+'/'+fileName
        score=Score()
        score.analyze_text(filePath)
        
    guageOption=None
    while guageOption not in {'N','E','H','X'}:
        guageOption=input("guage option([N]ormal, [E]asy, [H]ard, e[X]-hard): ")
        guageOption=guageOption.upper()
        
    return score, guageOption

def analyze(score, guageOption):
    notes_default=[None for _ in range(8)]
    for i, lane in enumerate(score.notes_default):
        notes_default[i] = lane[:]
    
    noted = [[] for _ in range(8)]
    noted_any = []
    noted_all = []
    charging = 0
    
    notes = []
    charge = []
    scratch = []
    soflan = []
    tateren = []
    
    yPhase=0
    bpm=self.bpm[0][1]
    while any(notes_default):
        is_noted_any = False
        for lane_no, lane in enumerate(notes_default):
            count = 0
            for note in lane:
                if note[0]<=yPhase: count+=1
                else: break
            for _ in range(count):
                note = lane.pop(0)
                if note[1] == 0:
                    noted[lane_no].append(60)
                elif note[1] == 1:
                    noted[lane_no].append(60)
                    charging += 1
                elif note[1] == 2:
                    if lane_no == 0:
                        noted[lane_no].append(60)
                    charging -= 1
                noted_all.append(60)
                is_noted_any = True
        if is_noted_any: noted_any.append(60)
        
        
        
        
        
        
        
        
        noted = [list(map(lambda note: note-1), noted_i) for noted_i in noted]
        noted = [list(filter(lambda note: note>0), noted_i) for noted_i in noted]
        noted_all = list(map(lambda note: note-1), noted_all)
        noted_all = list(filter(lambda note: note>0), noted_all)
        noted_any = list(map(lambda note: note-1), noted_any)
        noted_any = list(filter(lambda note: note>0), noted_any)
                
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
    
    guageProcess=[]
    difficulty=1
    while difficulty<30:
        isGameClear = simulate_guage(guageProcess, guageOption, notesList_with_frame,
                                     score.number_of_notes, difficulty)
        if isGameClear: break
        guageProcess=[]
        difficulty+=1
    return Result(difficulty, arrangement, guageProcess)

def simulate_guage(guageProcess, guageOption, notesList_with_frame, number_of_notes, difficulty):
    guage=10000 if guageOption in {"H","X"} else 2200
    isCN = [0 for _ in range(8)]
    for nwf_i, nwf1 in enumerate(notesList_with_frame):
        for lane1, status1 in nwf1[1:]:
            isGreat = simulate_judge(lane1, status1, nwf_i, nwf1, notesList_with_frame, isCN, difficulty)
            if isGreat:
                if guageOption in {"H","X"}:
                    guage+=16
                else:
                    guage+=int(760.5/(0.01*number_of_notes+6.5))
            else:
                if   guageOption in {"N"}:
                    guage-=600
                elif guageOption in {"E"}:
                    guage-=480
                elif guageOption in {"H"}:
                    guage-=960 if guage>=3000 else 480
                elif guageOption in {"X"}:
                    guage-=1920
        if guage>10000: guage=10000
        if guage<=0:
            if (guageOption in {"H","X"}): return False
            else: guage=0
        guageProcess.append([nwf1[0],guage])
        for lane, status in nwf1[1:]:
            if   status==1: isCN[lane]=1
            elif status==2: isCN[lane]=0
    if (guageOption in {"H","X"}): return True
    else:
        if guage>=8000: return True
        else: return False

def simulate_judge(lane1, status1, nwf_i, nwf1, notesList_with_frame, isCN, difficulty):
    d_both=0
    d_one =0
    d_both_tate=0
    d_one_tate =0
    
    #pressability
    for i in range(nwf_i):
        nwf2 = notesList_with_frame[nwf_i-(i+1)]
        df = nwf2[0] - nwf1[0]
        if df<-30:
            break
        
        for lane2, status2 in nwf2[1:]:
            dd_both=0
            dd_one =0
            dd_both_tate=0
            dd_one_tate =0
            if lane1==0 or lane2==0:
                if   abs(lane2-lane1)==0:
                    dd_both=40*pressability0(df/4)
                    dd_one =40*pressability0(df/4)
                elif abs(lane2-lane1)==1:
                    dd_both=40*pressability1(df/6)
                elif abs(lane2-lane1)==2:
                    dd_both=40*pressability1(df/6)
                elif abs(lane2-lane1)==3:
                    dd_both=24*pressability1(df/6)
            else:
                if   abs(lane2-lane1)==0:
                    dd_both_tate=40*pressability0(df/6)
                    dd_one_tate =40*pressability0(df/6)
                elif abs(lane2-lane1)==1:
                    if   lane1+lane2==13:
                        dd_both=36*pressability1(df/6)
                        dd_one =36*pressability1(df/6)
                    elif lane1+lane2==11:
                        dd_both=18*pressability1(df/6)
                        dd_one =48*pressability1(df/6)
                    elif lane1+lane2== 9:
                        dd_both=18*pressability1(df/6)
                        dd_one =36*pressability1(df/6)
                    elif lane1+lane2== 7:
                        dd_one =18*pressability1(df/6)
                    elif lane1+lane2== 5:
                        dd_both=18*pressability1(df/6)
                        dd_one =24*pressability1(df/6)
                    elif lane1+lane2==3:
                        dd_both=18*pressability1(df/6)
                        dd_one =18*pressability1(df/6)
                elif abs(lane2-lane1)==2:
                    if   lane1+lane2 in {10, 12}:
                        dd_both=18*pressability1(df/6)
                        dd_one =36*pressability1(df/6)
                    elif lane1+lane2 in {6,8}:
                        dd_one =18*pressability1(df/6)
                    elif lane1+lane2==4:
                        dd_both=18*pressability1(df/6)
                        dd_one =18*pressability1(df/6)
                elif abs(lane2-lane1)==3:
                    if   lane1+lane2==11:
                        dd_both=24*pressability1(df/6)
                        dd_one =24*pressability1(df/6)
                    elif lane1+lane2==7:
                        dd_one =24*pressability1(df/6)
                    elif lane1+lane2 in {5,9}:
                        dd_one =18*pressability1(df/6)
                elif abs(lane2-lane1) in {4, 5, 6}:
                    dd_one =18*pressability1(df/6)
                if status1==2:
                    dd_both/=2
                    dd_one /=2
                    dd_both_tate/=2
                    dd_one_tate /=2
                if status2==2:
                    dd_both/=2
                    dd_one /=2
                    dd_both_tate/=2
                    dd_one_tate /=2
            d_both+=dd_both
            d_one +=dd_one
            d_both_tate+=dd_both_tate
            d_one_tate +=dd_one_tate
        for lane2, status2 in enumerate(isCN):
            if status1!=2 and status2==1:
                dd_both=0
                dd_one =0
                if lane1==0 or lane2==0:
                    if   abs(lane2-lane1)==1:
                        dd_both=40*maxp1
                    elif abs(lane2-lane1)==2:
                        dd_both=40*maxp1
                    elif abs(lane2-lane1)==3:
                        dd_both=24*maxp1
                else:
                    if   abs(lane2-lane1)==1:
                        if   lane1+lane2==13:
                            dd_both=36*maxp1
                            dd_one =36*maxp1
                        elif lane1+lane2==11:
                            dd_both=18*maxp1
                            dd_one =48*maxp1
                        elif lane1+lane2== 9:
                            dd_both=18*maxp1
                            dd_one =36*maxp1
                        elif lane1+lane2== 7:
                            dd_one =18*maxp1
                        elif lane1+lane2== 5:
                            dd_both=18*maxp1
                            dd_one =24*maxp1
                        elif lane1+lane2==3:
                            dd_both=18*maxp1
                            dd_one =18*maxp1
                    elif abs(lane2-lane1)==2:
                        if   lane1+lane2 in {10, 12}:
                            dd_both=18*maxp1
                            dd_one =36*maxp1
                        elif lane1+lane2 in {6,8}:
                            dd_one =18*maxp1
                        elif lane1+lane2==4:
                            dd_both=18*maxp1
                            dd_one =18*maxp1
                    elif abs(lane2-lane1)==3:
                        if   lane1+lane2==11:
                            dd_both=24*maxp1
                            dd_one =24*maxp1
                        elif lane1+lane2==7:
                            dd_one =24*maxp1
                        elif lane1+lane2 in {5,9}:
                            dd_one =18*maxp1
                    elif abs(lane2-lane1) in {4, 5, 6}:
                        dd_one =18*maxp1
                    dd_both/=4
                    dd_one /=4
                d_both+=dd_both
                d_one +=dd_one
            
    #recognizability
#    for i in range(len(notesList_with_frame)-nwf_i-1):
#        nwf2 = notesList_with_frame[nwf_i+(i+1)]
#        df = nwf2[0] - nwf1[0]
#        if df>30:
#            break
#        for lane2, status2 in nwf2[1:]:
#            pass
    
    d = min(max(d_both, d_both_tate), max(d_one, d_one_tate))
#    d=d_one
#    d=d_both
    
    sigma=3.6
    isGreat = numpy.random.normal(difficulty,sigma)>=d
    return isGreat

def report(result):
    pyplot.plot([li[0] for li in result.guageProcess], [-(-li[1]//100) for li in result.guageProcess],
                label="{} ({})".format(result.difficulty, result.arrangement))
    print("difficulty: {} ({})".format(result.difficulty, result.arrangement))

def summarize(summary):
    pass

if __name__ == "__main__":
    main()
