import pandas as pd

class Cost():
    def __init__(self, treeType, dataframe):
        self.dataframe = dataframe
        self.treeType = treeType

    def getTypeDF (self):
        typeDF = self.dataframe[self.dataframe['type'] == self.treeType].iloc[0]
        return typeDF

    def getManPower (self):
        manPower = self.getTypeDF()["manPower"]
        return manPower

    def getMaintenance(self):
        maintenance = self.getTypeDF()["maintenance"]
        return maintenance

    def getPlanting(self):
        planting = self.getTypeDF()["planting"]
        return planting


    def calculate(self):
        manpower = self.getManPower()
        maintenance = self.getMaintenance()
        planting = self.getPlanting()

        expenses = manpower + maintenance + planting

        result = 'The estimated cost of planting a {} is: {}'.format(self.treeType, expenses)

        return result
