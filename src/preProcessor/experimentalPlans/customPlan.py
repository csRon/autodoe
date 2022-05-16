from .experimentalPlan import ExperimentalPlan

class CustomPlan(ExperimentalPlan):
    def __init__(self, config):
        super().__init__(config)

        self.__readPlanFromFile()
        self.convertPlanToRangeZeroOne()
        self.setNrTests()
        self.printPlanToFile('./plan_Custom.csv')

    def __readPlanFromFile(self):
        planPath = re.findall(r'\(.*?\)', self.planType)
        self.factorPlan = pd.read_csv(planPath, index_col=0).to_numpy()
        self.rawPlan = copy.deepcopy(self.factorPlan)
