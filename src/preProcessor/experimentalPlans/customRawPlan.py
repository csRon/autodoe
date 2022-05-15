from experimentalPlan import ExperimentalPlan

class CustomRawPlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__readRawPlanFromFile()
        self.convertPlanToRangeZeroOne()
        self.setFactorList(self.factorFile)
        self.checkFactorMatchingToRawPlan(self.factorFile)
        self.convertRawPlanToFactorPlan(self.factorFile)
        self.setNrTests()
        self.printPlanToFile('./plan_Custom-Raw.csv')

    def __readRawPlanFromFile(self):
        rawPlanPath = re.findall(r'\(.*?\)', self.planType)
        self.rawPlan = pd.read_csv(rawPlanPath, index_col=0).to_numpy()