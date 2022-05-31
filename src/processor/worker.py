import os
import subprocess

class Worker:

    def __init__(self, pathToWorkDir: str, startScript: str):
        os.chdir(pathToWorkDir)
        self.__runStartScript(startScript)

    def __runStartScript(self, startScript:str):
        os.chmod(startScript, 0o777)
        subprocess.run(['./%s > simulation.log 2>&1'%startScript], shell=True)
