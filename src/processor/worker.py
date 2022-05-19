import os
import subprocess

class Worker:

    def __init__(self, pathToWorkDir: str, startScript: str):
        print('\t\t\t Simulation started: %s'%pathToWorkDir)

        os.chdir(pathToWorkDir)
        self.__runStartScript(startScript)

    def __runStartScript(self, startScript:str):
        os.chmod(startScript, 0o777)
        subprocess.run(['./%s > simulation.log'%startScript], shell=True)
