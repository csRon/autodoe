import os
import shutil

from .experimentalPlans.experimentalPlan import ExperimentalPlan
from ..config.config import Config

class PreProcessor:

    def __init__(self, config: Config):
        self.config = config
        self.experimentalPlan = ExperimentalPlan(config)

        self.__createSimulationFolders()

    def __createSimulationFolders(self):
        for testNr in range(self.experimentalPlan.nrTests):
            pathToTestNrFolder = self.config.pathToSimulationFolder + '/' + str(testNr)
            os.makedirs(pathToTestNrFolder, exist_ok=True)

            self.__copyTemplatesToSimulationFolders(testNr)

    def __copyTemplatesToSimulationFolders(self, pathToTestNrFolder: str):
        shutil.copytree(self.config.pathToTemplateFolder, pathToTestNrFolder,
                        dirs_exist_ok=True)
        self.__replaceTemplateTokensInSimulationFolder(pathToTestNrFolder)

    def __replaceTemplateTokensInSimulationFolder(self, pathToTestNrFolder: str):
        pass

