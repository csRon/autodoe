import pyDOE2 as pydoe

from .experimentalPlan import ExperimentalPlan

class PydoePlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__setRawPlan(config)
        self.convertPlanToRangeZeroOne()
        self.checkFactorMatchingToRawPlan()
        self.convertRawPlanToFactorPlan(self.factorFile)
        self.printPlanToFile('./plan_%s.csv' % self.planType)


    def __setRawPlan(self, config):
        self.rawPlan = eval('pydoe.' + config.planCommand)

