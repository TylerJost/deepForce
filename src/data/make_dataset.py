# %%
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import scipy
# %%
# Load bodyweights and convert to newtons in dictionary
bw = pd.read_csv('../../data/external/bodyweight.csv', index_col = 0)
bw.columns = ['subjectNums', 'massKg']
bodyweights = {}
for subjectNum, massKg in zip(bw['subjectNums'], bw['massKg']):
    bodyweights[int(subjectNum)] = massKg*9.81

# %%
fpFiles = list(Path('../../data/interim').iterdir())
fpFiles = [fpFile for fpFile in fpFiles if str(fpFile).endswith('.csv')]
fp = pd.read_csv(fpFiles[0])
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

        self.beginFrame, self.endFrame = self.trimResults(plot=False)

        self.results = self.results.iloc[self.beginFrame, self.endFrame]
        self.shortenVariables()

    def trimResults(self, plotOn=True):
        plate2_0 = np.logical_and(fp.cx2 == 0, fp.cy2 == 0)
        plate3_0 = np.logical_and(fp.cx3 == 0, fp.cy3 == 0)

        both_0 = np.where(np.logical_and(plate2_0, plate3_0))[0]

        monoDiff = np.diff(both_0)
        # Check if beginning of sample is compromised
        if len(both_0)>0 and both_0[0] == 0:
            isMono = np.where(monoDiff>1)
            if len(isMono[0])>0:
                beginningIdx = isMono[0][0]
            else:
                beginningIdx = len(fp.monoDiff)
            beginFrame = fp.both_0[beginningIdx]+1
        else:
            beginFrame = 0
        if len(both_0)>0 and both_0[-1] == len(fp.cx2)-1:
            endingIdx = np.where(monoDiff>1)[0][-1]+1
            endFrame = fp.both_0[endingIdx]-1
        else:
            endFrame = len(fp.cx2)
        if plotOn == True:
            plt.subplot(121)
            plt.plot(fp.cx2, linewidth=1.5)
            plt.plot(fp.cx3, linewidth=1.5)

            plt.subplot(122)
            plt.plot(fp.cx2[beginFrame:endFrame], linewidth=1.5)
            plt.plot(fp.cx3[beginFrame:endFrame], linewidth=1.5)

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
        plt.scatter(self.cx2, self.cy2, c='gold')
        plt.scatter(self.cx3, self.cy3, c='green')
# %%
fp = forcePlateCapture(fpFiles[7])
fp.trimResults()
# %%
