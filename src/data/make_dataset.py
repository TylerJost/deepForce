# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import pickle
from tqdm import tqdm

from scipy import signal
# import scipy
# %%
# Load bodyweights and convert to newtons in dictionary
# bw = pd.read_csv('../../data/external/bodyweight.csv', index_col = 0)
# bw.columns = ['subjectNums', 'massKg']
# bodyweights = {}
# for subjectNum, massKg in zip(bw['subjectNums'], bw['massKg']):
#     bodyweights[int(subjectNum)] = massKg*9.81

# %%
class forcePlateCapture():
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileName = filePath.parts[-1]
        fParts = self.fileName.split('_')
        self.subjectNum = int(fParts[0][1:])
        self.exercise = '_'.join(fParts[1:4])
        self.trialNum = int(fParts[-1].split('.')[0])

        self.results = pd.read_csv(filePath)
        self.shortenVariables()
        try:
            self.beginFrame, self.endFrame = self.trimResults(plotOn=True)
        except:
            self.beginFrame = 0
            self.endFrame = len(self.cx2)
        self.results = self.results.iloc[self.beginFrame:self.endFrame]
        self.shortenVariables()

    def trimResults(self, plotOn=True):
        plt.plot(self.cx2)
        plate2_0 = np.logical_and(self.cx2 == 0, self.cy2 == 0)
        plate3_0 = np.logical_and(self.cx3 == 0, self.cy3 == 0)

        both_0 = np.where(np.logical_and(plate2_0, plate3_0))[0]

        monoDiff = np.diff(both_0)
        # Check if beginning of sample is compromised
        if len(both_0)>0 and both_0[0] == 0:
            isMono = np.where(monoDiff>1)
            if len(isMono[0])>0:
                beginningIdx = isMono[0][0]
            else:
                beginningIdx = len(monoDiff)
            beginFrame = both_0[beginningIdx]+1
        else:
            beginFrame = 0
        if len(both_0)>0 and both_0[-1] == len(self.cx2)-1:
            changeIdx = np.where(monoDiff>1)[0]
            if len(changeIdx)>0:
                endingIdx = [-1]+1
                endFrame = both_0[endingIdx]-1
            else:
                endFrame = both_0[0]
                print(f'Found one: {self.filePath}')
        else:
            endFrame = len(self.cx2)

        if plotOn == True:
            plt.subplot(121)
            plt.plot(self.cx2, linewidth=1.5)
            plt.plot(self.cx3, linewidth=1.5)

            plt.subplot(122)
            plt.plot(self.cx2[beginFrame:endFrame], linewidth=1.5)
            plt.plot(self.cx3[beginFrame:endFrame], linewidth=1.5)

        return beginFrame, endFrame
    def shortenVariables(self):
        self.fx2 = np.array(self.results['Fx_N-Plate2'])
        self.fy2 = np.array(self.results['Fy_N-Plate2'])
        self.fz2 = np.array(self.results['Fz_N-Plate2'])

        self.mx2 = np.array(self.results['Mx_N_mm-Plate2'])
        self.my2 = np.array(self.results['My_N_mm-Plate2'])
        self.mz2 = np.array(self.results['Mz_N_mm-Plate2'])

        self.cx2 = np.array(self.results['Cx_mm-Plate2'])
        self.cy2 = np.array(self.results['Cy_mm-Plate2'])
        self.cz2 = np.array(self.results['Cz_mm-Plate2'])

        self.fx3 = np.array(self.results['Fx_N-Plate3'])
        self.fy3 = np.array(self.results['Fy_N-Plate3'])
        self.fz3 = np.array(self.results['Fz_N-Plate3'])

        self.mx3 = np.array(self.results['Mx_N_mm-Plate3'])
        self.my3 = np.array(self.results['My_N_mm-Plate3'])
        self.mz3 = np.array(self.results['Mz_N_mm-Plate3'])

        self.cx3 = np.array(self.results['Cx_mm-Plate3'])
        self.cy3 = np.array(self.results['Cy_mm-Plate3'])
        self.cz3 = np.array(self.results['Cz_mm-Plate3'])

    def plotMovement(self):
        plt.scatter(self.cx2, self.cy2, c='gold', label = 'Force Plate 2')
        plt.scatter(self.cx3, self.cy3, c='green', label = 'Force Plate 3')
        plt.legend()

def writeData():
    homePath = Path().parent.absolute().parents[1]
    
    fpFiles = list(Path(homePath / 'data/interim').iterdir())
    assert len(fpFiles) > 0
    fpFiles = [fpFile for fpFile in fpFiles if str(fpFile).endswith('.csv')]

    fpData = []

    for fpFile in tqdm(fpFiles):
        # print(fpFile)
        fpData.append(forcePlateCapture(fpFile))

    pickle.dump(fpData, open(homePath / 'data' / 'processed' / 'fpProcessed.pickle', "wb"))
    
# self.trimResults()
# %%
# if __name__ == "__main__":
#     writeData()
# %%
fpFile = Path('/mnt/s/deepForce/data/interim/S22_STS_NI_SD_04.csv')

x = forcePlateCapture(fpFile)
# %%
fs = 100
fc = 5 # cutoff frequency
w = fc / (fs / 2) # Normalize the frequency
fs = 100
b, a = signal.butter(5, w, 'low')
output = signal.filtfilt(b, a, x.fz2)
plt.plot(output)
