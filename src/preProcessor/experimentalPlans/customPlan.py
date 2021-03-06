import pandas as pd

from .experimentalPlan import ExperimentalPlan

class CustomPlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__readPlanFromFile(config.planCommand)
        self.convertPlanToRangeZeroOne()
        self.setFactorList()
        self.setNrTests()
        self.__printFactorsToFile('factors.csv')
        self.printRawPlanToFile('rawPlan.csv')

    def __readPlanFromFile(self, planPath:str):
        self.factorPlan = pd.read_csv(planPath, index_col=0)
        self.rawPlan = self.factorPlan.to_numpy()

    def __printFactorsToFile(self, pathToFactorFile:str):
        #TODO
        pass
