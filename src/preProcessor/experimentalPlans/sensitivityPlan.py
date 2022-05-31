import re

import numpy as np
import pandas as pd

from .experimentalPlan import ExperimentalPlan

class SensitivityPlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)
        self.variations = list(map(float, config.planCommand.strip('][').split(',')))

        self.setFactorList()
        self.__setRawPlan()
        self.checkFactorMatchingToRawPlan()
        self.convertRawPlanToFactorPlan('factors.csv')
        self.setNrTests()
        self.printFactorPlanToFile('factorPlan.csv')
        self.printRawPlanToFile('rawPlan.csv')

    def __setRawPlan(self):
        dfFactors = pd.read_csv(self.factorFile, index_col='name')

        testNr = 0
        listRawPlan = []
        listVariationPlan = []
        for factor in self.factorList:
            baseValue = float(dfFactors.loc[factor].at['base'])
            variationMin = min(self.variations)
            factorMin = baseValue*(1+variationMin)
            variationMax = max(self.variations)
            factorMax = baseValue*(1+variationMax)
            self.__modifyFactorMinMax(dfFactors, factor, factorMin, factorMax)

            relBase = (baseValue-factorMin)/(factorMax-factorMin)


            for variation in self.variations:
                relVariation = (baseValue*(1+variation)-factorMin)/(factorMax-factorMin)
                listRawPlan.append(np.ones(len(self.factorList))*relBase)
                listRawPlan[testNr][self.factorList.index(factor)] = relVariation
                listVariationPlan.append(np.zeros(len(self.factorList)))
                listVariationPlan[testNr][self.factorList.index(factor)] = variation
                testNr += 1
        self.rawPlan = np.array(listRawPlan)

        self.__createNewFactorFile(dfFactors)
        self.__printVariationPlanToCsv(pd.DataFrame(np.array(listVariationPlan)))

    def __modifyFactorMinMax(self, dfFactors: pd.DataFrame, factor:str, factorMin:float, factorMax:float):
        dfFactors.loc[factor, 'min'] = factorMin
        dfFactors.loc[factor, 'max'] = factorMax

    def __createNewFactorFile(self, dfFactors:pd.DataFrame):
        dfFactors.to_csv('factors.csv')

    def __printVariationPlanToCsv(self, variationPlan:pd.DataFrame):
        variationPlan.to_csv('variationPlan.csv', header=self.factorList)