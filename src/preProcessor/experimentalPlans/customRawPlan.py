import re
import pandas as pd

from .experimentalPlan import ExperimentalPlan

class CustomRawPlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__readRawPlanFromFile(config.planCommand)
        self.convertPlanToRangeZeroOne()
        self.setFactorList()
        self.checkFactorMatchingToRawPlan()
        self.convertRawPlanToFactorPlan()
        self.setNrTests()
        self.printFactorPlanToFile('factorPlan.csv')

    def __readRawPlanFromFile(self, rawPlanPath):
        self.rawPlan = pd.read_csv(rawPlanPath, index_col=0).to_numpy()