import os
import shutil

from ..config.config import Config
from .experimentalPlans.pydoePlan import PydoePlan
from .experimentalPlans.customPlan import CustomPlan
from .experimentalPlans.customRawPlan import CustomRawPlan

class PreProcessor:

    def __init__(self, config: Config):
        print('\tPreprocessor started')

        self.config = config

        if config.planType == 'custom':
            self.experimentalPlan = CustomPlan(config)
        elif config.planType == 'customRaw':
            self.experimentalPlan = CustomRawPlan(config)
        else:
            self.experimentalPlan = PydoePlan(config)

        self.__createSimulationFolders()

        print('\tPreProcessor done')


    def __createSimulationFolders(self):
        for testNr in range(self.experimentalPlan.nrTests):
            pathToTestNrFolder = self.config.pathToSimulationFolder + '/' + str(testNr)
            os.makedirs(pathToTestNrFolder, exist_ok=True)
            self.__copyTemplatesToSimulationFolders(pathToTestNrFolder)
        print('\t\tFolder created, templates copied and tokens replaced: %s'%self.config.pathToSimulationFolder)

    def __copyTemplatesToSimulationFolders(self, pathToTestNrFolder: str):
        shutil.copytree(self.config.pathToTemplateFolder, pathToTestNrFolder,
                        dirs_exist_ok=True)
        self.__replaceTemplateTokensInSimulationFolder(pathToTestNrFolder)


    def __replaceTemplateTokensInSimulationFolder(self, pathToTestNrFolder: str):
        pass

