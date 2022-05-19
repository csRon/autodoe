import pandas as pd

from .experimentalPlan import ExperimentalPlan

class CustomPlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__readPlanFromFile(config.planPath)
        self.convertPlanToRangeZeroOne()
        self.setFactorList()
        self.setNrTests()
        self.__printFactorsToFile(config.pathToFactorFile)
        self.printRawPlanToFile('rawPlan_%s.csv' % self.planType)

    def __readPlanFromFile(self, planPath:str):
        self.factorPlan = pd.read_csv(planPath, index_col=0)
        self.rawPlan = self.factorPlan.to_numpy()

    def __printFactorsToFile(self, pathToFactorFile:str):
        #TODO
        pass
