from experimentalPlan import ExperimentalPlan

class PydoePlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__setRawPlan()
        self.convertPlanToRangeZeroOne()
        self.checkFactorMatchingToRawPlan(self.factorFile)
        self.convertRawPlanToFactorPlan(self.factorFile)
        self.setNrTests()
        self.printPlanToFile('./plan_%s.csv' % self.planType)

    def __setRawPlan(self):
        self.rawPlan = eval('pydoe.' + self.planType)

