from kivy.app import App
from kivy.uix.widget import Widget
from AppManager import *

from switchingScreen import SwitchingScreen

import main2
import NormalDatabase
from switchingScreen import SwitchingScreen
import KMC
import csv
import py_to_r

screenManager = SwitchingScreen.getScreenManager()
appManager = AppManager()

screens = []

class MainScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(MainScreen, self).__init__(**kw)


class KMCInfoScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(KMCInfoScreen, self).__init__(**kw)
        self.pathInput = ""
        self.kInput = 0

    def setPath(self, path):
        self.pathInput = path

    def setK(self, k):
        self.kInput = k

    def prepareDisplay(self):
        appManager.getApp().kmcVisualScreen.setInfo(self.pathInput)

    def eigenizedVector(self, vector, ev1, ev2):
        comp1 = vector.dotProd(ev1)
        comp2 = vector.dotProd(ev2)
        return [comp1, comp2]
        #return "%f, %f" % (comp1, comp2)

    def getKMC(self):
        dataFD, fileType, sAnalysis = main2.checkArgs(["main.py", "sMac", self.pathInput, "csv", "kmc", "-" + str(self.kInput)])
        normDB = NormalDatabase.makeNormalDB(dataFD, fileType)
        normDB.toCSV()
        kMeans = KMC.preformKMC(normDB, sAnalysis[0].flags)
        #screens[0].kMeans = str(kMeans)
        nullVar, altVar, percentExp = KMC.getVarianceInfo(kMeans, normDB)
        screens[0].ids.varianceValue.text = str(percentExp)
        ev1, ev2 = KMC.getEigenVectors()
        with open("pcaTraining.csv", "w") as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerow(["x", "y"])
            for vector in normDB.training.components:
                mywriter.writerow(self.eigenizedVector(vector, ev1, ev2))
        with open("kMeans.csv", "w") as file2:
            mywriter2 = csv.writer(file2, delimiter=',')
            mywriter2.writerow(["x", "y"])
            for vector in kMeans:
                mywriter2.writerow(self.eigenizedVector(vector, ev1, ev2))
        py_to_r.kmc("pcaTraining.csv", "kMeans.csv", "x-Lab", "y-Lab", "Title")
        dataFD.close()

    def refreshImage(self):
        screens[0].ids.display.reload()


class KMCVisualScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(KMCVisualScreen, self).__init__(**kw)

    def setInfo(self, info):
        self.ids.displayPath.text = info


class SLRInfoScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(SLRInfoScreen, self).__init__(**kw)
        self.pathInput = ""
        self.xInput = 0
        self.yInput = 0

    def setPath(self, path):
        self.pathInput = path

    def setX(self, x):
        self.xInput = x

    def setY(self, y):
        self.yInput = y

    def prepareDisplay(self):
        appManager.getApp().slrVisualScreen.setInfo(self.pathInput)

    def refreshImage(self):
        screens[1].ids.display.reload()
        row = ""
        with open("colm.csv", "r") as file:
            myreader = csv.reader(file, delimiter=',')
            for val in myreader:
                row = val
        b0 = row[0:5]
        screens[1].ids.b0.text = "b0: " + b0[1]
        screens[1].ids.b1.text = "b1: " + b0[2]
        screens[1].ids.R2.text = "R2: " + b0[3]

    def getSLR(self):
        dataFD, fileType, sAnalysis = main2.checkArgs(["main.py", "sMac", self.pathInput, "csv", "kmc"])
        normDB = NormalDatabase.makeNormalDB(dataFD, fileType)
        normDB.toCSV()
        py_to_r.linear_m(self.xInput, self.yInput, "X-Lab", "Y-Lab", "Title", "normDB.csv")



class SLRVisualScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(SLRVisualScreen, self).__init__(**kw)

    def setInfo(self, info):
        self.ids.displayPath.text = info


class DTInfoScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(DTInfoScreen, self).__init__(**kw)
        self.pathInput = ""
        self.targetInput = ""

    def setPath(self, path):
        self.pathInput = path

    def setTarget(self, target):
        self.targetInput = target

    def prepareDisplay(self):
        appManager.getApp().dtVisualScreen.setInfo(self.pathInput)

    def refreshImage(self):
        screens[1].ids.display.reload()
        row = ""
        with open("accuracy.csv", "r") as file:
            myreader = csv.reader(file, delimiter=',')
            for val in myreader:
                row = val
        b0 = row[0:5]
        screens[2].ids.accuracy.text = "Accuracy: " + b0[0]

    def getDT(self):
        dataFD, fileType, sAnalysis = main2.checkArgs(["main.py", "sMac", self.pathInput, "csv", "kmc"])
        normDB = NormalDatabase.makeNormalDB(dataFD, fileType)
        normDB.toCSV()
        py_to_r.dec_tree("normDB.csv", self.targetInput)


class DTVisualScreen(SwitchingScreen):
    def __init__(self, **kw):
        super(DTVisualScreen, self).__init__(**kw)

    def setInfo(self, info):
        self.ids.displayPath.text = info




class StatsApp(App):
    def __init__(self):
        super(StatsApp, self).__init__()
        self.mainScreen = None
        self.kmcInfoScreen = None
        self.kmcVisualScreen = None
        self.slrInfoScreen = None
        self.slrVisualScreen = None
        self.dtInfoScreen = None
        self.dtVisualScreen = None

    def build(self):
        self.mainScreen = MainScreen(name="main")
        self.kmcInfoScreen = KMCInfoScreen(name="kmcInfo")
        self.kmcVisualScreen = KMCVisualScreen(name="kmcVisual")
        self.slrInfoScreen = SLRInfoScreen(name="slrInfo")
        self.slrVisualScreen = SLRVisualScreen(name="slrVisual")
        self.dtInfoScreen = DTInfoScreen(name="dtInfo")
        self.dtVisualScreen = DTVisualScreen(name="dtVisual")

        screens.append(self.kmcVisualScreen)
        screens.append(self.slrVisualScreen)
        screens.append(self.dtVisualScreen)

        screenManager.add_widget(self.mainScreen)
        screenManager.add_widget(self.kmcInfoScreen)
        screenManager.add_widget(self.kmcVisualScreen)
        screenManager.add_widget(self.slrInfoScreen)
        screenManager.add_widget(self.slrVisualScreen)
        screenManager.add_widget(self.dtInfoScreen)
        screenManager.add_widget(self.dtVisualScreen)
        return screenManager


def main():
    statsApp = StatsApp()
    appManager.setApp(statsApp)
    statsApp.run()


if __name__ == "__main__":
    main()

