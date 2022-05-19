import pandas as pd
import numpy as np
import regex as re
import pyDOE2 as pydoe
import sys
#sys.path.insert(0,"../..")

# the usual import horror in python
# https://stackoverflow.com/questions/35166821/valueerror-attempted-relative-import-beyond-top-level-package
from ...config.config import Config

class ExperimentalPlan:
    '''
    Class for creating an experimental Plan based on DoE.

    planType [str]: type of doe plan (e.g. plackett-burrmann, lhs, ...)
    planType [str]: configuration params for the DoE plan (e.g.
                     number of factors, number of levels, ...). Depends
                     on pyDOE2 specs.
    rawPlan [np.array]: raw plan with abstract values (usually -1,0,
                        1 but depends on type)
    factorPlan [pd.DataFrame]: plan with real factor values
    nrTests [int]: number of tests runs of the plan
    '''

    def __init__(self, config: Config):
        self.factorFile = config.pathToFactorFile
        self.planType = config.planType

        self.rawPlan = np.array(0)
        self.factorPlan = pd.DataFrame()

        self.factorList = []
        self.nrTests = 0

        print('\t\tExperimental Plan created: plan_%s.csv'%config.planType )

    def setNrTests(self):
        self.nrTests = len(self.rawPlan)

    def setFactorList(self):
        self.factorList = list(pd.read_csv(self.factorFile, index_col='name').index)

    def convertPlanToRangeZeroOne(self):
        rawPlanRangeZeroOne = np.zeros((len(self.rawPlan[:, 0]), len(self.rawPlan[0, :])))

        # loop through columns of rawPlan
        for j in range(len(self.rawPlan[0, :])):
            factorCol = self.rawPlan[:, j]
            mini = min(factorCol)
            maxi = max(factorCol)

            # loop through rows of rawPlan
            for i in range(len(factorCol)):
                currentCell = float(self.rawPlan[i, j])
                rawPlanRangeZeroOne[i, j] = 0 + (1 - 0) * (currentCell - mini) / (maxi - mini)

        self.rawPlan = rawPlanRangeZeroOne

    def printFactorPlanToFile(self, pathToPlanFile):
        self.factorPlan.to_csv(pathToPlanFile)

    def printRawPlanToFile(self, pathToRawPlanFile):
        pd.DataFrame(self.rawPlan).to_csv(pathToRawPlanFile,
                                          header=self.factorList)

    def getFactorValuesOfTestRun(self, testNr):
        return dict(self.factorPlan.iloc[testNr])

    def checkFactorMatchingToRawPlan(self):
        # checking that numbers of factors in factors.csv matches the
        # configuration parameters from *.conf

        nrFactorsCSV = len(self.factorList)
        nrFactorsRawPlan = len(self.rawPlan[0, :])
        if nrFactorsCSV != nrFactorsRawPlan:
            raise ValueError(
                'The number of factors in factors.csv does not match to the plan created with config.conf.')

    def convertRawPlanToFactorPlan(self, pathToFactorFile):
        dfFactors = pd.read_csv(pathToFactorFile, index_col='name')

        self.factorPlan = pd.DataFrame(self.rawPlan.copy())
        self.factorPlan.columns = self.factorList

        # loop through all factors (columns of rawPlan)
        j = 0
        factorsWithExprList = []
        posOfFactorWithExpr = []
        for factor in self.factorList:
            factorCol = self.rawPlan[:, j].copy()
            factorMin = str(dfFactors.loc[factor].at['min'])
            factorMax = str(dfFactors.loc[factor].at['max'])

            # check if factor min is a number (float or int)
            if re.match('[\-|\+]?[0-9]+[\.]?[0-9]*', factorMin) is None \
                    or re.match('[\-|\+]?[0-9]+[\.]?[0-9]*', factorMax) is None:
                # if true factorMin/Max should be a math expression like 'a+b/2'
                # it is necessary to save these columns for later because they
                # depend on other factors values which need to be calculated first
                factorsWithExprList.append(factor)
                posOfFactorWithExpr.append(j)
                # these are dummy values that no error occurs
                factorMin = 0
                factorMax = 0

            factorMin = float(factorMin)
            factorMax = float(factorMax)

            factorCol *= factorMax - factorMin
            factorCol += factorMin

            # overwrite column of factorPlan
            self.factorPlan[factor] = factorCol

            j += 1

        # loop through the previous saved factor with expression in factorMin/Max
        factorRegex = '|'.join(self.factorList)
        j = 0
        for factorWithExpr in factorsWithExprList:
            factorCol = self.rawPlan[:, posOfFactorWithExpr[j]]

            factorMin = str(dfFactors.loc[factorWithExpr].at['min'])
            factorMax = str(dfFactors.loc[factorWithExpr].at['max'])

            if re.match('[\-|\+]?[0-9]+[\.]?[0-9]*', factorMin) is None:
                factorMin = self.__calcMinMaxForStrExpression(factorCol, factorRegex, factorMin)
            else:
                factorMin = float(factorMin)
            if re.match('[\-|\+]?[0-9]+[\.]?[0-9]*', factorMax) is None:
                factorMax = self.__calcMinMaxForStrExpression(factorCol, factorRegex, factorMax)
            else:
                factorMax = float(factorMax)

            factorCol *= factorMax - factorMin
            factorCol += factorMin

            # overwrite column of factorPlan
            self.factorPlan[factorWithExpr] = factorCol

            j += 1

    def __calcMinMaxForStrExpression(self, factorCol, factorRegex, minMax):
        minMaxCol = np.zeros(len(factorCol))

        # loop through all tests
        i = 0
        for testNr in range(len(factorCol)):
            # get all factors, operators (+-*/) and number (float or int)
            expressionList = re.findall('%s|[+|\-|\*|/]|[[0-9]+[\.]?[0-9]*' % (factorRegex), minMax)

            # extract factors from expressionlist
            factorsInExprList = list(set(expressionList) & set(self.factorList))
            # calculate values for factor with min or max
            for factorInExpr in factorsInExprList:
                factorValue = self.factorPlan.loc[i].at[factorInExpr]
                factorExpr = minMax.replace(factorInExpr, str(factorValue))

            # calculate expression
            minMaxCol[i] = eval(factorExpr)
            i += 1
        return minMaxCol

