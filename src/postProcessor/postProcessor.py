import os
import subprocess

import pandas as pd


from ..config.config import Config

class PostProcessor:

    def __init__(self, config: Config):
        print('\tPostProcessor started')

        self.__createResultsDir()
        self.collectedResults = pd.DataFrame()
        print('\t\tCollect results from simulationFolder')
        self.__extractResultsInSimFolder('simulationFolder', config.extractScript)
        self.__printResultsToCsv()

        print('\tPostProcessor done')

    def __extractResultsInSimFolder(self, pathToSimFolder:str, extractScript:str):
        # loop through all folder in simulationFolder
        for simFolder in list(map(str, sorted([int(folder) for folder in os.listdir(pathToSimFolder)]))):
            pathToWorkDir = pathToSimFolder + '/' + simFolder

            # make current directory new workDir
            os.chdir(pathToWorkDir)
            # run extract script, currently only python possible
            subprocess.run(['python3 %s'%extractScript], shell=True)
            self.__collectResults()

            # go back to base dir
            os.chdir('../..')

            print('\t\t\tCollecting from simulationFolder/%s done'%simFolder)

    def __collectResults(self):
        # reads out the extracted values and writes them to the collectedResults data frame
        filteredResults = pd.read_csv('filteredResults.csv')
        self.collectedResults = pd.concat([self.collectedResults, filteredResults], ignore_index=True)

    def __createResultsDir(self):
        print('\t\tCreated results directory: results')
        os.makedirs('results', exist_ok=True)

    def __printResultsToCsv(self):
        print('\t\tPrinted results file containing all data: results/extractedData.csv')
        self.collectedResults.to_csv('results/extractedData.csv')

