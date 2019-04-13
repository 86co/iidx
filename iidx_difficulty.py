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
    '26': '26_Rootage'
}

def main():
    score, styleOption, guageOption, times = handle_input()
    summary = analyze(score, styleOption, guageOption, times)
    summarize(summary)
        
def handle_input():
    score=None
    while score is None:
        #fileName = input("input fileName(.txt): /scores/SP/ ")
        print('')
        series = input("series: ")
        try: series=folderName[series]
        except: continue
        filePath = os.getcwd()+'/scores/SP/'+series
        fileList = os.listdir(filePath)
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
    
    print('')
    styleOption=None
    while styleOption not in {'N','A','R','S'}:
        styleOption=input("style option([N]ormal-mirror, r[A]ndom, [R]-random, [S]-random): ")
        styleOption=styleOption.upper()
        
    guageOption=None
    while guageOption not in {'N','E','H','X'}:
        guageOption=input("guage option([N]ormal, [E]asy, [H]ard, e[X]-hard): ")
        guageOption=guageOption.upper()
        
    if styleOption in {'A','R','S'}:
        times=None
        while times is None or times<1:
            times=input("number of times(1~): ")
            try: times=int(times)
            except ValueError: times=None
                
    else: times=2
        
    return score, styleOption, guageOption, times

def analyze(score, styleOption, guageOption, times):
    canceled = False
    jobs = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    concurrency=multiprocessing.cpu_count()
    create_processes(score, guageOption, jobs, results, concurrency)
    add_jobs(styleOption, times, jobs)
    try:
        jobs.join()
    except KeyboardInterrupt:
        canceled = True
    print("""
    GENRE  {}
    TITLE  {}
    ARTIST {}
    LEVEL  {} ({} notes)
    """.format(score.genre, score.title, score.artist, score.level, score.number_of_notes))
    while not results.empty():
        result=results.get_nowait()
        report(result)
    pyplot.title("{} ({})".format(score.title, score.level))
    pyplot.tick_params(labelbottom=False)
    pyplot.legend()
    pyplot.show()
    #return Summary()
        
def create_processes(score, guageOption, jobs, results, concurrency):
    for _ in range(concurrency):
        process = multiprocessing.Process(target=worker, args=(score, guageOption, jobs, results))
        process.daemon = True
        process.start()    
    
def worker(score, guageOption, jobs, results):
    while True:
        try:
            styleNumber = jobs.get()
            result = analyze_one(score, styleNumber, guageOption)
            results.put(result)
        finally:
            jobs.task_done()

def add_jobs(styleOption, times, jobs):
    for i in range(times):
        if   styleOption=='N': jobs.put(0 if i==0 else 4)
        elif styleOption=='A': jobs.put(1)
        elif styleOption=='R': jobs.put(2)
        elif styleOption=='S': jobs.put(3)

def analyze_one(score, styleNumber, guageOption):
    notes, longNotes, arrangement = score.change_style(styleNumber)
    notesList_with_frame=[]
    for frame in score.frameList:
        notesList_with_frame.append([frame])
    for yIndex, y in enumerate(score.yList):
        for laneIndex, lane in enumerate(notes):
            for note in lane:
                if note[0]==y:
                    notesList_with_frame[yIndex].append([laneIndex, note[1]])
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
                    dd_both=48*pressability0(df/4)
                    dd_one =48*pressability0(df/4)
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
