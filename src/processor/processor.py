import os
import re
import numpy as np
from multiprocessing import Process
import time

from ..config.config import Config
from .worker import Worker

class Processor:

    def __init__(self, config: Config):
        print('\tProcessor started')

        self.nWorker = config.nWorker
        self.executeTests = self.__parseExecuteTests(config.executeTests, config.pathToSimulationFolder)
        print('\t\tExecuting tests %s'%(','.join(map(str, self.executeTests))))

        self.workerList = []
        self.__organizeWorker(config.pathToSimulationFolder)



    def __parseExecuteTests(self, executeTestString: str, pathToSimulationFolder: str) -> list:
        # 'all' takes all foldes inside the simulation folder regardless how their naming
        if 'all' in executeTestString.lower():
            return sorted(os.listdir(pathToSimulationFolder))

        # list range input (e.g., [0:-5]) is given
        elif re.search(r'[.*:.*]', executeTestString):
            # there are 11 possibilities, but all have
            # a start point: startDigit, an end point: endDigit and a step size: stepDigit
            # when it is not there, it has a default value set in the else case

            # all digits have a special property in the given syntax for range
            # startDigit is always directly behind a left bracket [ (e.g., [4:])
            startDigit = re.findall(r'\[-?\d+', executeTestString)
            if len(startDigit) != 0:
                startDigit = int(re.findall(r'-?\d+', startDigit[0])[0])
            else:
                startDigit = 0

            # endDigit is always behind one left bracket followed by a digit or none and a :
            endDigit = re.findall(r'\[(?:-?\d+)?:-?\d+', executeTestString)
            if len(endDigit) != 0:
                endDigit = int(re.findall(r'-?\d+', endDigit[0])[-1])
            else:
                endDigit = len(os.listdir(pathToSimulationFolder))

            # stepDigit is always in front of a right bracket ] and has two : in front
            stepDigit = re.findall(r':.*:-?\d+', executeTestString)
            if len(stepDigit) != 0:
                stepDigit = int(re.findall(r'-?\d+', stepDigit[0])[-1])
            else:
                stepDigit = 1

            return list(map(str, np.arange(startDigit, endDigit, stepDigit, dtype=int)))

        # elif list input (e.g., [0,3,4,5,12]) is given
        elif re.search(r'[.*,.*]', executeTestString):
            digits = re.findall(r'-?\d+', executeTestString)
            return list(map(str, digits))

        else:
            pass
            # TODO: catch invalid statement


    def __organizeWorker(self, pathToSimFolder:str):
        # prepare list of worker and fill them with None
        for workerNr in range(self.nWorker):
            self.workerList.append(None)

        testNr = 0
        while testNr < len(self.executeTests):
            for workerNr in range(self.nWorker):
                if testNr >= len(self.executeTests):
                    break

                pathToWorkDir = pathToSimFolder + '/' + self.executeTests[testNr]
                time.sleep(1)
                if self.workerList[workerNr] is None:
                    self.workerList[workerNr] = self.__spawnWorker(pathToWorkDir, testNr)
                    testNr += 1
                    continue

                self.workerList[workerNr].join(timeout=0)
                if not self.workerList[workerNr].is_alive():
                    self.workerList[workerNr] = self.__spawnWorker(pathToWorkDir, testNr)
                    testNr += 1
                else:
                    self.workerList[workerNr].kill()

    def __spawnWorker(self, pathToWorkDir:str, testNr:int) -> Process:
        process = Process(target=Worker, args=(pathToWorkDir,testNr,))
        process.start()
        return process
