import pyDOE2 as pydoe

from .experimentalPlan import ExperimentalPlan

class PydoePlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__setRawPlan(config.planCommand)
        self.setFactorList()
        self.setNrTests()
        self.convertPlanToRangeZeroOne()
        self.checkFactorMatchingToRawPlan()
        self.convertRawPlanToFactorPlan(self.factorFile)
        self.printFactorPlanToFile('factorPlan.csv')
        self.printRawPlanToFile('rawPlan.csv')


    def __setRawPlan(self, planCommand:str):
        self.rawPlan = eval('pydoe.' + planCommand)

