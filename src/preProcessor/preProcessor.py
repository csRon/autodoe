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
            self.__copyTemplatesToSimulationFolders(pathToTestNrFolder, testNr)
        print('\t\tFolder created, templates copied and tokens replaced: %s'%self.config.pathToSimulationFolder)

    def __copyTemplatesToSimulationFolders(self, pathToTestNrFolder: str, testNr:int):
        shutil.copytree(self.config.pathToTemplateFolder, pathToTestNrFolder,
                        dirs_exist_ok=True)
        self.__replaceTemplateTokensInSimulationFolder(pathToTestNrFolder, testNr)

    def __replaceTemplateTokensInSimulationFolder(self, pathToTestNrFolder: str, testNr:int):
        # loop through all files in sim folder
        for file in os.listdir(pathToTestNrFolder):
            # replace all tokens with factor value of current test nr
            if '.tmpl' in file:
                pathToTemplateFile = pathToTestNrFolder + '/' + file
                with open(pathToTemplateFile, 'r') as templateFile:
                    templateFileString = templateFile.read()
                    for factor in self.experimentalPlan.factorList:
                        replaceFactorValue = str(self.experimentalPlan.factorPlan.at[testNr, factor])
                        templateFileString = templateFileString.replace('$%s$'%factor, '%s'%replaceFactorValue)

                # write the new string with replaced values to a new file without .tmpl ending
                with open(pathToTemplateFile[:-5], 'w') as valueFile:
                    valueFile.write(templateFileString)

                # delete template file
                os.remove(pathToTemplateFile)




